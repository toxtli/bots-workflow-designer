from core.Module import Module
from utils import LogHelper, DatasourceHelper
from modules.ConnectionListener.ConnectionListener import ConnectionListener

class ConnectionListenerModule(Module):

	DATABASE_TABLE = 'contacts'
	drivers = {}
	waiting_list = []
	listeners = {}

	def run(self, params, callback):
		self.MAX_PROCESSES = 10
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		# https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatasourceHelper.get_dataset({"table": self.DATABASE_TABLE})
		email = params['bots']['email']
		urls = params['accepted']
		for url in urls:
			contact = self.db.select_one({'email':email, 'url':url})
			if contact['status'] == 'INVITED':
				self.waiting_list.append(url)
				self.maybe_init_listener(params, callback)
			else:
				output = {'added': [url]}
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.pop(params, output, callback)

	
	def maybe_init_listener(self, params, callback):
		email = params['bots']['email']
		if email not in self.drivers:
			sel = params['bots']['driver']
			self.drivers[email] = sel
			args = {'driver': sel}
			self.listeners[email] = ConnectionListener(args)
			def connection_listener_handler(urls):
				LogHelper.log(self.waiting_list, True)
				for url in urls:
					LogHelper.log('EVALUATING INCOMMING ACCEPT', True)
					LogHelper.log(url, True)
					if url in self.waiting_list:
						LogHelper.log('INCOMMING ACCEPT EVALUATED', True)
						self.waiting_list.remove(url)
						if not self.waiting_list:
							self.listeners[email].stop()
						self.db.update({'url': url},{'accepted': True, 'status': 'ACCEPTED'})
						output = {'added': [url]}
						LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
						self.pop(params, output, callback)
			self.listeners[email].run(params, connection_listener_handler)
		else:
			self.listeners[email].tick()