class Module(object):

	def __init__(self):
		self.ins, self.outs, self.queues = {}, {}, {}
		self.values, self.inputs, self.required = {}, {}, {}

	def run(self, params, callback):
		print('RUNNING ' + self.__class__.__name__)
		print('INPUT ' +  str(params))
		output = {}
		for out in self.outs:
			if self.outs[out]['type'] == 'out':
				output[out] = out + ' value'
		print('OUTPUT ' +  str(output))
		callback(output, params)

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
		self.run(self.inputs,self.call_next)

	def check_states(self):
		num_elements = len(self.queues.keys()) + len(self.required.keys())
		valid_states = 0
		for queue in self.queues.keys():
			if len(self.queues[queue]) > 0:
				valid_states += 1
		for field in self.required.keys():
			if self.values[field]:
				valid_states += 1
		if valid_states == num_elements:
			self.prepare_run()

	def set_values(self, params):
		check = False
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