import time
from config import Configuration
from utils import LogHelper, NetworkHelper, TextHelper, VoiceHelper, LinkedinHelper
from utils.SeleniumHelper import SeleniumHelper

class BotsCreator(object):

	URL_INIT = 'https://www.linkedin.com/'
	URL_READ_EMAIL_API = 'http://hcilab.ml/api/?method=read&email='
	FIELD_FIRST_NAME = '#reg-firstname'
	FIELD_LAST_NAME = '#reg-lastname'
	FIELD_EMAIL = '#reg-email'
	FIELD_PASSWORD = '#reg-password'
	BUTTON_CREATE = '#registration-submit'
	SELECT_COUNTRY = '#country'
	FIELD_ZIP = '#zip-code'
	BUTTON_SAVE = '.save-profile'
	FIELD_JOB_TITLE = '#job-title'
	FIELD_COMPANY = '#company'
	SELECT_INDUSTRY = '#industry'
	BUTTON_JOB = '.save-profile'
	BUTTON_INTERESTED = 'button[data-goaltype="NONE"]'
	FIELD_CODE = '#challenge-input'
	BUTTON_CODE = '#code-submit'
	BUTTON_SKIP = '#jaso-cta-skip'
	BUTTON_SKIP_CONN = '.btn-skip'
	BUTTON_SKIP_PHOTO = 'input[value="Skip"]'
	BUTTON_SKIP_SMS = 'input[value="Next"]'
	PROFILE_SECTION = '.profile-overview'
	BUTTON_SKIP_EMAIL = '#abk-skip-btn'
	BUTTON_SKIP_EMAIL_CONFIRM = '.abk-hopscotch-skip'
	FIELD_VERIFICATION_PHONE = '#phoneNumber'
	VERIFICATION_DIALOG = '#captcha-dialog'
	ALERT_LOGIN = '#login-callout'
	FRAME_VERIFICATION = '.challenge-iframe'
	VERIFICATION_CODE = '#challenge-input'
	BUTTON_VERIFICATION = '#code-submit'
	FIELD_SMS_CODE = '#challenge-input'
	BUTTON_SMS_CODE = '#submitPage2'

	sel = None

	def __init__(self, params=None):
		self.sel = LinkedinHelper.get_driver(params)

	def run(self):
		self.sel.loadPage(self.URL_INIT)
		record = self.db.select_one({'email':profile['email']})
		if not record['accountCreated']:
			self.createAccount(profile)
			self.db.update({'email':profile['email']}, {'accountCreated':True, 'cookies':self.sel.getCookies()})
		else:
			LinkedinHelper.login(self.sel, profile)

	def createAccount(self, profile):
		self.sel.loadPage(self.URL_INIT)
		if not profile['triedOnce']:
			LogHelper.log('CREATING ACCOUNT')
			self.sel.waitAndWrite(self.FIELD_FIRST_NAME, profile['firstName'])
			self.sel.selectAndWrite(self.FIELD_LAST_NAME, profile['lastName'])
			self.sel.selectAndWrite(self.FIELD_EMAIL, profile['email'])
			self.sel.selectAndWrite(self.FIELD_PASSWORD, profile['password'])
			self.sel.clickSelector(self.BUTTON_CREATE)
			if self.sel.existWaitElement(self.VERIFICATION_DIALOG, 4):
				LogHelper.log('CAPTCHA FOUND')
				self.sel.switchFrame(self.FRAME_VERIFICATION)
				if self.sel.existWaitElement(self.FIELD_VERIFICATION_PHONE, 4):
					self.sel.clickSelector(self.FIELD_VERIFICATION_PHONE)
					self.sel.selectAndWrite(self.FIELD_VERIFICATION_PHONE, Configuration.sms_number)
					self.sel.submitFormSelector(self.FIELD_VERIFICATION_PHONE)
					sms_code = self.get_sms_code()
					self.sel.waitAndWrite(self.FIELD_SMS_CODE, sms_code)
					self.sel.clickSelector(self.BUTTON_SMS_CODE)
				self.sel.switchMain()
		else:
			LogHelper.log('LOGGING IN')
			LinkedinHelper.login(self.sel, profile, True)
			if self.sel.existWaitElement(self.VERIFICATION_CODE, 4):
				code_value = self.get_email_code(profile['email'])
				self.sel.selectAndWrite(self.VERIFICATION_CODE, code_value)
				self.sel.clickSelector(self.BUTTON_VERIFICATION)
		if self.sel.existWaitElement(self.SELECT_COUNTRY, 4):
			LogHelper.log('COMPLETING')
			self.db.update({'email':profile['email']}, {'triedOnce':True})
			self.sel.selectOptionByValue(self.SELECT_COUNTRY, profile['country'].lower())
			# self.selectAndWrite(self.FIELD_ZIP, profile['zip'])
			self.sel.selectAndWrite(self.FIELD_ZIP, '36320')
			self.sel.clickSelector(self.BUTTON_SAVE)
			self.sel.waitAndWrite(self.FIELD_JOB_TITLE, profile['expertise'])
			self.sel.selectAndWrite(self.FIELD_COMPANY, 'Independient')
			self.sel.clickSelector(self.FIELD_JOB_TITLE)
			self.sel.waitShowElement(self.SELECT_INDUSTRY)
			self.sel.selectOptionByValue(self.SELECT_INDUSTRY, 'urn:li:industry:96')
			self.sel.clickSelector(self.BUTTON_JOB)
			self.sel.waitAndClick(self.BUTTON_INTERESTED)
			self.sel.waitShowElement(self.FIELD_CODE)
			LogHelper.log('GETTING EMAIL CODE')
			code_value = self.get_email_code(profile['email'])
			LogHelper.log('EMAIL CODE RETRIEVED')
			LogHelper.log(code_value)
			self.sel.selectAndWrite(self.FIELD_CODE, code_value)
			self.sel.clickSelector(self.BUTTON_CODE)
			self.sel.waitAndClick(self.BUTTON_SKIP_EMAIL)
			self.sel.waitAndClick(self.BUTTON_SKIP_EMAIL_CONFIRM, 4)
			self.sel.waitAndClick(self.BUTTON_SKIP, 4)
			self.sel.waitAndClick(self.BUTTON_SKIP, 4)
			self.sel.waitAndClick(self.BUTTON_SKIP_CONN, 4)
			self.sel.waitAndClick(self.BUTTON_SKIP_PHOTO, 4)
			self.sel.waitAndClick(self.BUTTON_SKIP_SMS, 4)
			self.sel.waitShowElement(self.PROFILE_SECTION, 4)

	def get_sms_code(self):
		code_value = ''
		while not code_value:
			time.sleep(1)
			sms_text = VoiceHelper.get_sms_last()
			code_value = TextHelper.text_between(sms_text,'verification code is ','.')
		return code_value

	def get_email_code(self, email):
		url = self.URL_READ_EMAIL_API + email
		code_value = ''
		while not code_value:
			time.sleep(1)
			email_text = NetworkHelper.get(url)
			code_value = TextHelper.text_between(email_text, 'full access to LinkedIn. ', ' Enter your verificatio')
		return code_value