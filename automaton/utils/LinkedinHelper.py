import time
from config import Configuration
from utils import LogHelper
from utils.SeleniumHelper import SeleniumHelper

URL_INIT = 'https://www.linkedin.com/'
FIELD_LOGIN_USER = '#login-email'
FIELD_LOGIN_PASS = '#login-password'
# ELEMENT_TOP_BAR = '.header-section'
ELEMENT_TOP_BAR = '#top-header'
REQUEST_ERRROR = '#main > h1'
ERROR_UNPLANNED = '.wiper'

def get_conn_id(html):
	connId = ''
	arr1 = html.split('connId=')
	if len(arr1) > 1:
		arr2 = arr1[1].split('&')
		connId = arr2[0]
	return connId

def get_driver(params=None):
	if params:
		if 'driver' in params:
			return params['driver']
	return SeleniumHelper(Configuration.selenium_driver_type)

def login(driver, params, skipLoad=False):
	cookies = None
	if not skipLoad:
		driver.loadPage(URL_INIT)
	logged = driver.getElement(ELEMENT_TOP_BAR)
	if not logged:
		if params['cookies']:
			driver.applyCookies(URL_INIT, params['cookies'])
			logged = driver.getElement(ELEMENT_TOP_BAR)
		if not logged:
			if params['cookies']:
				driver.cleanCookies()
			url = driver.getUrl()
			if not 'error' in url:
				LogHelper.log('FIRST TIME', True)
				has_logged = login_enter_credentials(driver, params)
				if has_logged:
					cookies = has_logged
				else:
					LogHelper.log('SECOND TIME', True)
					driver.loadPage(URL_INIT)
					LogHelper.log('TIME 3', True)
					has_logged = login_enter_credentials(driver, params)
					if has_logged:
						LogHelper.log('TIME 4', True)
						cookies = has_logged
					else:
						LogHelper.log('ERROR AGAIN', True)
						time.sleep(100)
			else:
				LogHelper.log('ERROR FOUND', True)
				time.sleep(100)
	return cookies

def login_enter_credentials(driver, params):
	exit = False
	if driver.existElement(FIELD_LOGIN_USER):
		driver.selectAndWrite(FIELD_LOGIN_USER, params['email'])
		driver.selectAndWrite(FIELD_LOGIN_PASS, params['password'])
		driver.submitFormSelector(FIELD_LOGIN_PASS)
		time.sleep(0.4)
		# driver.waitPageLoad()
		title = driver.getTitle()
		LogHelper.log(title, True)
		if 'Error' not in title:
			exit = driver.waitGetCookies()
	return exit

def get_logged_in_driver(params=None):
	if params:
		if 'driver' in params:
			return params['driver']
	driver = SeleniumHelper(Configuration.selenium_driver_type)
	login(driver, params)
	return driver

def clone_driver(driver):
	return driver.cloneDriverSite(URL_INIT)

def clone_driver_wait(driver):
	return driver.waitCloneDriverSite(URL_INIT, ELEMENT_TOP_BAR)
