import sys
from utils import LogHelper, LinkedinHelper

class ConnectionRequester(object):

	SITE_URL = 'https://www.linkedin.com'
	LAYOUT_PROFILE = '.profile-overview'
	USER_ADD_BUTTON_NORMAL = 'a[data-action-name="add-to-network"]'
	LAYOUT_FRIEND = '.iwrite'
	USER_ADD_FRIEND_OPTION = 'input[value="IF"]'
	USER_ADD_BUTTON_INVITE = '#send-invite-button'
	USER_ADD_ALERT = 'div.alert.success'
	USER_ADD_ALTERNATIVE = 'a[data-action-name="add-to-network"]'
	ELEMENT_TOP_BAR = '.header-section'
	ALREADY_FRIEND = '#nprofile-remove-from-network'

	sel = None

	def __init__(self, params=None):
		self.sel = LinkedinHelper.get_logged_in_driver(params)

	def run(self, params, callback=None):
		urls = params['contacts']
		for url in urls:
			LogHelper.log(url)
			self.sel.loadPage(url)
			try:
				# self.sel.waitShowElement(self.LAYOUT_PROFILE)
				if not self.sel.existElement(self.ALREADY_FRIEND):
					if self.sel.existElement(self.USER_ADD_BUTTON_NORMAL):
						LogHelper.log('CLICKING 1')
						if not self.sel.clickAndJavascript(self.USER_ADD_BUTTON_NORMAL):
							LogHelper.log('CLICKING 2')
							if not self.sel.clickAndJavascript(self.USER_ADD_ALTERNATIVE):
								LogHelper.log('CLICKING 3')
						LogHelper.log('CLICKED')
						if self.sel.waitShowElement(self.LAYOUT_FRIEND):
							LogHelper.log('FRIEND LAYOUT')
							friendOption = self.sel.getElement(self.USER_ADD_FRIEND_OPTION)
							if friendOption:
								LogHelper.log('OPTION FOUND')
								self.sel.click(friendOption)
								LogHelper.log('FRIEND OPTION CLICKED')
								inviteButton = self.sel.getElement(self.USER_ADD_BUTTON_INVITE)
								LogHelper.log('BUTTON FOUND')
								# self.click(inviteButton)
								# self.waitShowElement(self.USER_ADD_ALERT)
						else:
							self.sel.saveScreenshoot()
							LogHelper.log('BUTTON NOT FOUND')
			except:
				LogHelper.log(sys.exc_info())
			if callback:
				callback(url)
		self.sel.close()

	def batch(self):
		pass