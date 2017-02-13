import sys
import time
from random import randint
from selenium import webdriver
from config import Configuration
from utils import LogHelper
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumHelper:
	driver = None
	driverType = None
	WAIT = 99999

	def __init__(self, driverType=None):
		self.driverType = driverType
		if driverType == 'proxy':
			profile = webdriver.FirefoxProfile()
			profile.set_preference( "network.proxy.type", 1 )
			profile.set_preference( "network.proxy.socks", "127.0.0.1" )
			profile.set_preference( "network.proxy.socks_port", 9150 )
			profile.set_preference( "network.proxy.socks_remote_dns", True )
			profile.set_preference( "places.history.enabled", False )
			profile.set_preference( "privacy.clearOnShutdown.offlineApps", True )
			profile.set_preference( "privacy.clearOnShutdown.passwords", True )
			profile.set_preference( "privacy.clearOnShutdown.siteSettings", True )
			profile.set_preference( "privacy.sanitize.sanitizeOnShutdown", True )
			profile.set_preference( "signon.rememberSignons", False )
			profile.set_preference( "network.cookie.lifetimePolicy", 2 )
			profile.set_preference( "network.dns.disablePrefetch", True )
			profile.set_preference( "network.http.sendRefererHeader", 0 )
			profile.set_preference( "javascript.enabled", False )
			profile.set_preference( "permissions.default.image", 2 )
			self.driver = webdriver.Firefox(profile)
		elif driverType == 'headless':
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap["phantomjs.page.settings.userAgent"] = Configuration.selenium_user_agent
			self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
		else:
			self.driver = webdriver.Firefox()
			self.driver.set_window_size(640, 480)
			self.driver.set_window_position(randint(0,800), randint(0,400))

	def loadPage(self, page):
		try:
			self.driver.get(page)
			return True
		except:
			return False

	def submitForm(self, element):
		try:
			element.submit()
			return True
		except TimeoutException:
			return False

	def submitFormSelector(self, selector):
		try:
			element = self.getElement(selector)
			element.submit()
			return True
		except TimeoutException:
			return False

	def waitShowElement(self, selector, wait=None):
		try:
			wait = WebDriverWait(self.driver, wait if wait else self.WAIT)
			element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
			return element
		except:
			return None

	def waitHideElement(self, selector, wait=None):
		try:
			wait = WebDriverWait(self.driver, wait if wait else self.WAIT)
			element = wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, selector)))
			return element
		except:
			return None

	def getElementFrom(self, fromObject, selector):
		try:
			return fromObject.find_element_by_css_selector(selector)
		except:
			return None

	def getElementsFrom(self, fromObject, selector):
		try:
			return fromObject.find_elements_by_css_selector(selector)
		except:
			return None		

	def existElement(self, selector):
		element = self.getElement(selector)
		if element:
			return True
		else:
			return False

	def existWaitElement(self, selector, wait=None):
		element = self.waitShowElement(selector, wait if wait else self.WAIT)
		if element:
			return True
		else:
			return False

	def getElement(self, selector):
		return self.getElementFrom(self.driver, selector)

	def getElements(self, selector):
		return self.getElementsFrom(self.driver, selector)

	def getElementFromValue(self, fromObject, selector):
		element = self.getElementFrom(fromObject, selector)
		return self.getValue(element)

	def getElementValue(self, selector):
		element = self.getElement(selector)
		return self.getValue(element)

	def getValue(self, element):
		if element:
			return element.text
		return None

	def getAttribute(self, element, attribute):
		if element:
			return element.get_attribute(attribute)
		return None

	def getElementFromAttribute(self, fromObject, selector, attribute):
		element = self.getElementFrom(fromObject, selector)
		return self.getAttribute(element, attribute)

	def getElementAttribute(self, selector, attribute):
		element = self.getElement(selector)
		return self.getAttribute(element, attribute)

	def getParentLevels(self, node, levels):
		path = '..'
		if levels > 1:
			for i in range(1, levels):
				path = path + '/..'
		return node.find_element_by_xpath(path)

	def getParentNode(self, node):
		return node.find_element_by_xpath('..')

	def getChildNodes(self, node):
		return node.find_elements_by_xpath('./*')

	def selectOptionByValue(self, selector, value):
		element = self.getElement(selector)
		select = Select(element)
		select.select_by_value(value)

	def selectOptionByText(self, selector, value):
		element = self.getElement(selector)
		select = Select(element)
		select.select_by_visible_text(value)

	def selectAndWrite(self, field, value):
		fieldObject = self.getElement(field)
		fieldObject.send_keys(value)
		return fieldObject

	def selectCleanAndWrite(self, field, value):
		fieldObject = self.getElement(field)
		fieldObject.clear()
		fieldObject.send_keys(value)
		return fieldObject

	def waitAndWrite(self, field, value, wait=None):
		fieldObject = self.waitShowElement(field, wait if wait else self.WAIT)
		if fieldObject:
			fieldObject.send_keys(value)
		return fieldObject

	def waitCleanAndWrite(self, field, value, wait=None):
		fieldObject = self.waitShowElement(field, wait if wait else self.WAIT)
		if fieldObject:
			fieldObject.clear()
			time.sleep(0.5)
			fieldObject.send_keys(value)
		return fieldObject

	def waitAndClick(self, field, wait=None):
		fieldObject = self.waitShowElement(field, wait if wait else self.WAIT)
		if fieldObject:
			self.click(fieldObject)
		return fieldObject

	def cleanFieldSelector(self, field):
		fieldObject = self.getElement(field)
		fieldObject.clear()

	def pressEnter(self, fieldObject):
		fieldObject.send_keys(Keys.RETURN)
		return fieldObject

	def clickSelector(self, selector):
		element = self.getElement(selector)
		if element:
			try:
				actions = webdriver.ActionChains(self.driver)
				actions.move_to_element(element)
				actions.click(element)
				actions.perform()
				return True
			except:
				return False
		return False

	def clickMultiple(self, selector):
		exit = False
		elements = self.getElements(selector)
		if elements:
			for element in elements:
				try:
					actions = webdriver.ActionChains(self.driver)
					actions.move_to_element(element)
					actions.click(element)
					actions.perform()
					exit = True
				except:
					pass
		return exit

	def click(self, element):
		try:
			actions = webdriver.ActionChains(self.driver)
			actions.move_to_element(element)
			actions.click(element)
			actions.perform()
			return True
		except:
			return False

	def clickAndJavascript(self, selector):
		self.clickJavascript(selector)
		if not self.clickSelector(selector):
			return False
		return True

	def injectLocalScript(self, filepath):
		return self.driver.execute_script(open(filepath).read())

	def injectRemoteScript(self, url):
		return self.driver.execute_script("var s=window.document.createElement('script');s.src='" + url + "';window.document.head.appendChild(s);")

	def executeScript(self, code):
		return self.driver.execute_script(code)

	def clickJavascript(self, selector):
		return self.driver.execute_script("var obj=document.querySelector('" + selector + "');if(obj){obj.click();return true;}else{return false;}")

	def moveToElement(self, element):
		self.driver.execute_script("return arguments[0].scrollIntoView();", element)
		actions = webdriver.ActionChains(self.driver)
		actions.move_to_element(element)
		actions.perform()

	def scrollDown(self):
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

	def scrollingDown(self, times):
		for i in range(1, times):
			self.scrollDown()
			time.sleep(0.5)

	def getFieldValue(self, record, parent=None):
		exit = None
		if parent:
			if record['type'] == 'attr':
				if record['selector']:
					exit = self.getElementFromAttribute(parent, record['selector'], record['attr'])
				else:
					exit = self.getAttribute(parent)
			elif record['type'] == 'text':
				if record['selector']:
					exit = self.getElementFromValue(parent, record['selector'])
				else:
					exit = self.getValue(parent)
			elif record['type'] == 'style':
				exit = record['attr']
		else:
			if record['type'] == 'attr':
				exit = self.getElementAttribute(record['selector'], record['attr'])
			elif record['type'] == 'text':
				exit = self.getElementValue(record['selector'])
			elif record['type'] == 'style':
				exit = record['attr']
		return exit

	def extractSectionFromObjects(self, section, sections, fields):
		self.SECTIONS = sections
		self.FIELDS = fields
		return self.extractSection(section)

	def extractSection(self, section):
		exit = {}
		for subsection in self.SECTIONS[section]:
			container = self.SECTIONS[section][subsection]
			if container['quantity'] == 'multiple':
				exit[subsection] = []
				elements = self.getElements(container['selector'])
				for element in elements:
					row = {}
					for field in self.FIELDS[section][subsection]:
						record = self.FIELDS[section][subsection][field]
						row[field] = self.getFieldValue(record, element)
					exit[subsection].append(row)
			elif container['quantity'] == 'single':
				exit[subsection] = self.getFieldValue(container)
		return exit

	def saveScreenshoot(self, filePath='screenshot.png'):
		self.driver.save_screenshot(filePath)

	def loadAndWait(self, url, selector, wait=None):
		self.loadPage(url)
		return self.waitShowElement(selector, wait if wait else self.WAIT)

	def switchFrame(self, selector):
		frame = self.getElement(selector)
		self.driver.switch_to.frame(frame)

	def switchMain(self):
		self.driver.switch_to.default_content()

	def getCode(self):
		return self.driver.page_source

	def getUrl(self):
		return self.driver.current_url

	def getTitle(self):
		return self.driver.title

	def wait_for(self, condition_function, wait):
	    start_time = time.time()
	    while time.time() < start_time + wait:
	        if condition_function():
	            return True
	        else:
	            time.sleep(0.1)
	    return False

	def waitPageLoad(seld, wait=None):
		wait = wait if wait else self.WAIT
	    def page_has_loaded():
	        page_state = self.driver.execute_script(
	            'return document.readyState;'
	        ) 
	        return page_state == 'complete'
	    return self.wait_for(page_has_loaded, wait)

	def waitGetCookies(self):
		cookies = {}
		try:
			cookies = self.driver.get_cookies()
		except:
			LogHelper.log(sys.exc_info(), True)
		if cookies:
			return cookies
		else:
			time.sleep(0.2)
			return self.waitGetCookies()

	def getCookies(self):
		cookies = {}
		try:
			cookies = self.driver.get_cookies()
		except:
			LogHelper.log(sys.exc_info())
		return cookies

	def setCookies(self, cookies):
		for cookie in cookies:
			try:
				self.driver.add_cookie({'name': cookie['name'],'value': cookie['value']})
			except:
				pass

	def applyCookies(self, url, cookies):
		self.loadPage(url)
		self.setCookies(cookies)
		self.loadPage(url)

	def cleanCookies(self):
		self.driver.delete_all_cookies()

	def cloneDriverSite(self, url):
		sel = SeleniumHelper(self.driverType)
		sel.applyCookies(url, self.waitGetCookies())
		return sel

	def waitCloneDriverSite(self, url, waitUntil):
		sel = SeleniumHelper(self.driverType)
		sel.applyCookies(url, self.waitGetCookies())
		sel.waitShowElement(waitUntil)
		return sel

	def close(self):
		self.driver.quit()