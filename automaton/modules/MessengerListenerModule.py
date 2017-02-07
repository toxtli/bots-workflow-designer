from core.Module import Module
from utils import LogHelper, LinkedinHelper
from utils.DatabaseHelper import DatabaseHelper
from modules.MessengerListener.MessengerListener import MessengerListener

class MessengerListenerModule(Module):

	DATABASE_TABLE = 'messages'

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		# https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatabaseHelper(table=self.DATABASE_TABLE)
		sel = LinkedinHelper.clone_driver(params['bots']['driver'])
		args = {'driver': sel}
		messenger_listener = MessengerListener(args)
		def messenger_listener_handler(message):
			self.db.insert_one(message)
			output = {'results': message}
			LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
			self.pop(params, output, callback)
		messenger_listener.run(params, messenger_listener_handler)
