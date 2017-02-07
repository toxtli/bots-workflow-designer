from utils import LogHelper, LinkedinHelper

class MessengerListener(object):

	URL_MESSAGES = 'https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after='

	callbacks = {}
	sel = None

	def __init__(self, params=None):
		self.sel = LinkedinHelper.get_logged_in_driver(params)

	def run(self, params, callback=None):
		message = params['conversation']
		if callback:
			callback(message)
		self.sel.close()
		#https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		pass
