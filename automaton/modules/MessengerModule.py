import sys
import time
from core.Module import Module
from selenium import webdriver
from utils import LogHelper, LinkedinHelper
from utils.DatabaseHelper import DatabaseHelper
from utils.SeleniumHelper import SeleniumHelper
from modules.Messenger.Messenger import Messenger

class MessengerModule(Module):

	DATABASE_TABLE = 'contacts'
	CONTACTS_TABLE = 'messages'

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		exit = 'result messenger'
		email = params['bots']['email']
		urls = params['userdata']
		self.db = DatabaseHelper(table=self.DATABASE_TABLE)
		for url in urls:
			contact = self.db.select_one({'email':email, 'url':url})
			if not contact['firstMessageSent']:
				sel = LinkedinHelper.clone_driver(params['bots']['driver'])
				args = {'driver': sel}
				messenger = Messenger(args)
				def messenger_callback(results):
					self.db.update_one({'email':email,'url':url},{'firstMessageSent':True})
					output = {'conversation': results}
					LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
					self.pop(params, output, callback)

				params['url'] = contact['url']
				if 'connId' in contact:
					params['connId'] = contact['connId']
				else:
					params['connId'] = ''
				messenger.send_message(params, messenger_callback)
			else:
				output = {'conversation': [url]}
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.pop(params, output, callback)
		
