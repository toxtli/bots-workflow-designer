import sys
import time
from utils import LogHelper, LinkedinHelper

class Messenger(object):

	SITE_URL = 'https://www.linkedin.com'
	DATABASE_TABLE = 'messages'
	CHAT_URL = 'https://www.linkedin.com/messaging/compose?connId='
	TEXTBOX_MESSAGE = '#compose-message'
	PROFILE_CONTENT = '#top-card'

	sel = None

	def __init__(self, params=None):
		self.sel = LinkedinHelper.get_logged_in_driver(params)

	def run(self, params, callback):
		pass

	def send_message(self, params, callback=None, keepOpen=False, backToMain=False):
		body = params['message']
		connId = params['connId']
		url = params['url']			
		if not connId:
			self.sel.loadPage(url)
			topcard = self.sel.waitShowElement(self.PROFILE_CONTENT)
			connId = LinkedinHelper.get_conn_id(self.sel.getCode())
		if connId:
			msgUrl = self.CHAT_URL + connId
			self.sel.loadPage(msgUrl)
			textarea = self.sel.waitShowElement(self.TEXTBOX_MESSAGE)
			try:
				textarea.send_keys(body)
				textarea.send_keys('\n\r')
				textarea.send_keys('\n\r')
			except:
				pass
				# LogHelper.log(sys.exc_info())
			time.sleep(0.5)
			exit = 'OK'
		else:
			exit = 'User not found'
		LogHelper.log(exit)
		if callback:
			callback(params)
		if not keepOpen:
			self.sel.close()
		elif backToMain:
			self.sel.loadPage(self.SITE_URL)
