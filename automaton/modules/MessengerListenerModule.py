import time
import threading
from core.Module import Module
from utils import LogHelper, LinkedinHelper, TextHelper, MBFHelper, DatasourceHelper
from modules.MessengerListener.MessengerListener import MessengerListener
from modules.Messenger.Messenger import Messenger

class MessengerListenerModule(Module):

	DATABASE_TABLE = 'messages'
	TABLE_CONTACTS = 'contacts'
	drivers = {}
	listeners = {}
	waiting_list = []

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		# https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatasourceHelper.get_dataset({"table": self.DATABASE_TABLE})
		email = params['bots']['email']
		urls = params['conversation']
		for url in urls:
			contact = self.db.select_one({'email':email, 'url':url})		
			self.waiting_list.append(url)
			self.maybe_init_listener(params, callback)

	def maybe_init_listener(self, params, callback):
		email = params['bots']['email']
		if email not in self.drivers:
			sel = params['bots']['driver']
			listener = LinkedinHelper.clone_driver_wait(params['bots']['driver'])
			self.drivers[email] = sel
			args = {'driver': sel}
			self.listeners[email] = MessengerListener(args)
			def messenger_listener_handler(message):
				message['email'] = email
				message['type'] = 'INCOMING'
				self.db.insert_one(message)
				LogHelper.log('NEW MESSAGE', True)
				LogHelper.log('Listener 01')
				for msg in message['messages']:
					LogHelper.log('Listener 02')
					LogHelper.log(msg)
					LogHelper.log('Listener 03')
					connId = msg['sender']['id']
					LogHelper.log(connId)
					contact = self.db.select_one({'userId': connId}, table=self.TABLE_CONTACTS)
					LogHelper.log(contact)
					if contact:
						LogHelper.log('Listener 04')
						response = MBFHelper.send_and_wait_response(contact['conversationId'], msg['body'])
						if response:
							LogHelper.log('Listener 05')
							msgdata = {
								'email': email,
								'type': 'OUTCOMING',
								'connId': connId,
								'message': response,
								'url': contact['url'],
								'conversationId': contact['conversationId']
							}
							self.db.insert_one(msgdata)
							LogHelper.log('Listener 06')
							LogHelper.log('SENDING MESSAGE', True)
							messenger = Messenger({'driver': listener})
							messenger.send_message(msgdata, keepOpen=True, backToMain=False)
							LogHelper.log('Listener 07')
				output = {'results': message}
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.pop(params, output, callback)
			self.listeners[email].run(params, messenger_listener_handler)
		else:
			self.listeners[email].tick()
