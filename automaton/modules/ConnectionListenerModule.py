import time
import threading
from core.Module import Module
from utils import LogHelper, LinkedinHelper, TextHelper
from utils.DatabaseHelper import DatabaseHelper
from modules.ConnectionListener.ConnectionListener import ConnectionListener

class ConnectionListenerModule(Module):

	DATABASE_TABLE = 'contacts'
	drivers = {}

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
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
			sel.injectLocalScript('js/ConnectionListener.js')
			self.drivers[email] = sel
			t = threading.Thread(target=self.check_connections, args=[params])
			t.start()
		else:
			sel = {}
		args = {'driver': sel}
		connection_listener = ConnectionListener(args)
		def connection_listener_handler(url):
			self.db.update({'url': url},{'accepted': True})
			output = {'added': [url]}
			LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
			self.pop(params, output, callback)
		connection_listener.run(params, connection_listener_handler)

	def check_connections(self, params):
		finish = False
		email = params['bots']['email']
		while not finish:
			LogHelper.log('check_connections')
			self.drivers[email].executeScript('tox.requestNotifications()')
			time.sleep(2)
			result = self.drivers[email].executeScript('return tox.getNotifications()')
			text = TextHelper.text_between(result, '', '')
			LogHelper.log(text)
			time.sleep(5)