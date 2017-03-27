import time
import threading
from utils import LogHelper, TextHelper

class MessengerListener(object):

	URL_MESSAGES = 'https://www.linkedin.com/messaging/conversationsView?includeSent=false&clearUnseen=true&after='

	wait = 5
	callbacks = {}
	sel = None
	stop_order = False


	def __init__(self, params=None):
		self.sel = params['driver']

	def run(self, params, callback=None):
		self.params = params
		self.callback = callback
		self.sel.injectLocalScript('js/MessengerListener.js')			
		self.start()
		message = params['conversation']
		if callback:
			pass
			# callback(message)
		#https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		pass

	def check_messages(self, params, callback):
		email = params['bots']['email']
		while not self.stop_order:
			LogHelper.log('check_messages')
			self.sel.executeScript('tox.requestMessages()')
			time.sleep(2)
			result = self.sel.executeScript('return tox.getMessages()')
			if result:
				LogHelper.log(result)
				if 'conversationsAfter' in result and result['conversationsAfter']:
					for message in result['conversationsAfter']:
						callback(message)
			time.sleep(self.wait - 2)

	def start(self):
		t = threading.Thread(target=self.check_messages, args=[self.params, self.callback])
		t.start()

	def stop(self):
		self.stop_order = True

	def tick(self):
		if self.stop_order:
			self.stop_order = False
			self.start()