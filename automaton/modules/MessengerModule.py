import sys
import time
from core.Module import Module
from selenium import webdriver
from utils import LogHelper, LinkedinHelper
from utils.DatabaseHelper import DatabaseHelper
from utils.SeleniumHelper import SeleniumHelper
from modules.Messenger.Messenger import Messenger

class MessengerModule(Module):

	DATABASE_TABLE = 'messages'
	CONTACTS_TABLE = 'contacts'

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		exit = 'result messenger'
		bot_email = params['bots']['email']
		self.db = DatabaseHelper(table=self.DATABASE_TABLE)
		sel = LinkedinHelper.clone_driver(params['bots']['driver'])
		args = {'driver': sel}
		messenger = Messenger(args)
		def messenger_callback(results):
			output = {'conversation': results}
			LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
			self.pop(params, output, callback)
		urls = params['userdata']
		for url in urls:
			params['url'] = url
			params['connId'] = ''
			dbdata = self.db.select_one({'url':url},table=self.CONTACTS_TABLE)
			if dbdata:
				params['connId'] = dbdata['userId']
			messenger.send_message(params, messenger_callback)
		
