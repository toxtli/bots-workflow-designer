from core.Module import Module
from utils import LogHelper, LinkedinHelper
from utils.DatabaseHelper import DatabaseHelper
from modules.MessengerListener.MessengerListener import MessengerListener

class MessengerListenerModule(Module):

	DATABASE_TABLE = 'messages'

	def run(self, params, callback):
		self.MAX_PROCESSES = 10
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		# https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		output = {'results':[]}
		LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
		self.pop(params, output, callback)
