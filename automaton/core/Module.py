import threading
from utils import LogHelper

class Module(object):

	def __init__(self):
		self.ins, self.outs, self.queues, self.pending = {}, {}, {}, []
		self.values, self.inputs, self.required = {}, {}, {}
		self.running_processes, self.MAX_PROCESSES = 0, 0

	def run(self, params, callback):
		output = self.run_debug(params)
		callback(output, params)

	def run_queue(self, params, callback):
		output = self.run_debug(params)
		self.pop(output, params, callback)

	def run_debug(self, params):
		LogHelper.log('RUNNING ' + self.__class__.__name__)
		LogHelper.log('INPUT ' +  str(params))
		output = {}
		for out in self.outs:
			if self.outs[out]['type'] == 'out':
				output[out] = out + ' value'
		LogHelper.log('OUTPUT ' +  str(output))
		return output

	def call_next(self, params_output, params_input=None):
		if not params_input:
			params_input = self.inputs
		for out in self.outs:
			connections = self.outs[out]['connections']
			if len(connections) > 0:
				for connection in connections:
					value = {}
					if out in params_output:
						value[out] = params_output[out]
					elif out in params_input:
						value[out] = params_input[out]
					connection['target'].set_values(value)

	def prepare_run(self):
		self.inputs = {} 
		for queue in self.queues:
			self.inputs[queue] = self.queues[queue].pop(0)
		for value in self.values:
			self.inputs[value] = self.values[value]
		LogHelper.log("CALLING THREAD " + self.__class__.__name__)
		t = threading.Thread(target=self.run, args=[self.inputs,self.call_next])
		t.start()

	def check_states(self):
		LogHelper.log("STATES " + self.__class__.__name__)
		LogHelper.log("STATES REQUIERED")
		LogHelper.log(self.queues.keys())
		LogHelper.log(self.required.keys())
		LogHelper.log("STATES GIVEN")
		num_elements = len(self.queues.keys()) + len(self.required.keys())
		valid_states = 0
		for queue in self.queues.keys():
			if len(self.queues[queue]) > 0:
				LogHelper.log(queue)
				valid_states += 1
		for field in self.required.keys():
			if self.values[field]:
				LogHelper.log(field)
				valid_states += 1
		LogHelper.log("RECEIVED " + str(valid_states) + " NEEDED " + str(num_elements))
		if valid_states == num_elements:
			self.prepare_run()

	def set_values(self, params):
		check = False
		LogHelper.log("SET VALUE " + self.__class__.__name__ + ' ' + str(params.keys()))
		for index in params:
			if index in self.queues:
				self.queues[index].append(params[index])
				check = True
			elif index in self.values:
				self.values[index] = params[index]
				check = True
		if check:
			self.check_states()

	def add_node(self, params):
		if params['type'] == 'in':
			if params['source'] == 'Linked':
				self.queues[params['name']] = []
			else:
				self.values[params['name']] = ''
				if 'required' in params:
					self.required[params['name']] = params['required']
		self.ins[params['name']] = params.copy()
		self.ins[params['name']]['connections'] = []
		self.outs[params['name']] = params.copy()
		self.outs[params['name']]['connections'] = []

	def connect(self, params):
		if 'targetName' in params:
			target_name = params['targetName']
		else:
			target_name = params['name']
		self.outs[params['name']]['connections'].append({
			'name': target_name,
			'target': params['target']
		})
		params['target'].ins[target_name]['connections'].append({
			'name': params['name'],
			'target': self
		})

	def check_queue(self):
		LogHelper.log("CHECKING QUEUE STEP 1 " + self.__class__.__name__)
		if self.running_processes < self.MAX_PROCESSES:
			LogHelper.log("CHECKING QUEUE STEP 2 " + self.__class__.__name__)
			available = self.MAX_PROCESSES - self.running_processes
			for i in range(available):
				LogHelper.log("CHECKING QUEUE STEP 3 " + self.__class__.__name__)
				if self.pending:
					LogHelper.log("CHECKING QUEUE STEP 4 " + self.__class__.__name__)
					process = self.pending.pop(0)
					self.running_processes += 1
					LogHelper.log("STARTING THREAD")
					t = threading.Thread(target=process['action'], args=[process['params'],process['callback']])
					t.start()
				else:
					LogHelper.log("NOT PENDING " + self.__class__.__name__)
					break

	def pop(self, params, output, callback):
		LogHelper.log("POP " + self.__class__.__name__)
		callback(params, output)
		if self.MAX_PROCESSES > 0:
			self.running_processes -= 1
			self.check_queue()

	def push(self, params, callback, action):
		LogHelper.log("PUSH " + self.__class__.__name__)
		if self.MAX_PROCESSES > 0:
			self.pending.append({'params':params, 'callback':callback, 'action':action})
			self.check_queue()
		else:
			action(params, callback)