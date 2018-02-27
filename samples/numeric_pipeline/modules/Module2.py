from core.Module import Module
from utils import LogHelper

class Module2(Module):

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params), True)
		output = {}
		output["mod2out"] = params["mod1out"] * 2
		self.pop(params, output, callback)