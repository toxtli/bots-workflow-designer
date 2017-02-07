from utils import LogHelper, LinkedinHelper

class ConnectionListener(object):

	URL_PENDING_CONNECTIONS = 'https://www.linkedin.com/chrome/global_nav_pymk_invitations?resultType=pymk&location=desktop-global-nav-first-fetch&records=3&count=3'
	URL_CONNECTIONS_ACCEPTED = 'https://www.linkedin.com/chrome/inbox/activity/notifications/v2?rnd='

	callbacks = {}
	sel = None

	def __init__(self, params=None):
		self.sel = LinkedinHelper.get_logged_in_driver(params)

	def run(self, params, callback=None):
		# result['content']['global_nav_pymk_invitations']['inbox_pending_invitations']['people']
		for url in params['accepted']:
			if callback:
				callback(url)
		#https://www.linkedin.com/messaging/conversationsView?includeSent=true&clearUnseen=false&after=1486408991388
		pass
