from core.Module import Module
from utils import LogHelper, LinkedinHelper
from utils.DatabaseHelper import DatabaseHelper
from modules.BotsCreator.BotsCreator import BotsCreator

class BotsCreatorModule(Module):

	db = None
	DATABASE_TABLE = 'profiles'

	drivers = {}

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		profiles = params['profiles']
		self.db = DatabaseHelper(table=self.DATABASE_TABLE)
		for profile in profiles:
			email = profile['email']
			if email not in self.drivers:
				self.drivers[email] = LinkedinHelper.get_driver()
			sel = self.drivers[email]
			args = {'driver': sel}
			bots_creator = BotsCreator(args)
			record = self.db.select_one({'email':profile['email']})
			if not record['accountCreated']:
				bots_creator.createAccount(profile)
				self.db.update({'email':profile['email']}, {'accountCreated':True, 'cookies':sel.getCookies()})
			else:
				cookies = LinkedinHelper.login(sel, profile)
				if cookies:
					self.db.update({'email':email},{'cookies': cookies})
			output = {'bots':{'email': profile['email'], 'driver': sel}}
			LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
			self.pop(params, output, callback)
