from core.Module import Module
from utils import LogHelper
import csv

class Module1(Module):

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params), True)
		filem=open(params["filename"],'r')
		reader=csv.reader(filem)
		for row in reader:
			for value in row:
				self.pop(params, {"mod1out": int(value)}, callback)