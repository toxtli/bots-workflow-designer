import time
import threading
from core.Module import Module
from utils import LogHelper, LinkedinHelper, TextHelper
from utils.DatabaseHelper import DatabaseHelper
from modules.MessengerListener.MessengerListener import MessengerListener

class MessengerListenerModule(Module):

	DATABASE_TABLE = 'messages'
	drivers = {}

	def run(self, params, callback):
		self.MAX_PROCESSES = 10
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		# https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatabaseHelper(table=self.DATABASE_TABLE)
		email = params['bots']['email']
		if email not in self.drivers:
			sel = params['bots']['driver']
			sel.injectLocalScript('js/MessengerListener.js')
			self.drivers[email] = sel
			t = threading.Thread(target=self.check_messages, args=[params])
			t.start()
		else:
			sel = {}
		args = {'driver': sel}
		messenger_listener = MessengerListener(args)
		def messenger_listener_handler(value):
			output = {'results': 'ok'}
			LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
			self.pop(params, output, callback)
		messenger_listener.run(params, messenger_listener_handler)

	def check_messages(self, params):
		finish = False
		email = params['bots']['email']
		while not finish:
			LogHelper.log('check_messages', True)
			self.drivers[email].executeScript('tox.requestMessages()')
			time.sleep(2)
			result = self.drivers[email].executeScript('return tox.getMessages()')
			text = TextHelper.text_between(result, '', '')
			LogHelper.log(text)
			time.sleep(5)
