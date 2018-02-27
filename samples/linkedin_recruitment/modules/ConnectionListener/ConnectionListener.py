import time
import threading
from utils import LogHelper, TextHelper

class ConnectionListener(object):

	URL_PENDING_CONNECTIONS = 'https://www.linkedin.com/chrome/global_nav_pymk_invitations?resultType=pymk&location=desktop-global-nav-first-fetch&records=3&count=3'
	URL_CONNECTIONS_ACCEPTED = 'https://www.linkedin.com/chrome/inbox/activity/notifications/v2?rnd='

	callbacks = {}
	sel = None
	stop_order = False

	def __init__(self, params=None):
		self.sel = params['driver']

	def run(self, params, callback=None):
		self.params = params
		self.callback = callback
		self.sel.injectLocalScript('js/ConnectionListener.js')			
		self.start()
		for url in params['accepted']:
			if callback:
				# callback([url])
				pass

	def check_connections(self, params, callback):
		email = params['bots']['email']
		protocol = 'http'
		while not self.stop_order:
			LogHelper.log('check_connections')
			self.sel.executeScript('tox.requestNotifications()')
			time.sleep(2)
			result = self.sel.executeScript('return tox.getNotifications()')
			if result:
				urls = TextHelper.text_between(result, 'href="' + protocol, '&amp;trk=hb_ntf_ACCEPTED_YOUR_CONNECTION_REQUEST')
				for url in urls:
					url = protocol + url
					callback([url])
				LogHelper.log(urls, True)
			time.sleep(5)

	def start(self):
		t = threading.Thread(target=self.check_connections, args=[self.params, self.callback])
		t.start()

	def stop(self):
		self.stop_order = True

	def tick(self):
		if self.stop_order:
			self.stop_order = False
			self.start()

