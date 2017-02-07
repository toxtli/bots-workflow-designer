from core.Module import Module
from utils import LogHelper, LinkedinHelper
from utils.DatabaseHelper import DatabaseHelper
from modules.ProfilesFinder.ProfilesFinder import ProfilesFinder

class ProfilesFinderModule(Module):

	DATABASE_TABLE = 'contacts'

	drivers = {}
	db = None

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatabaseHelper(table=self.DATABASE_TABLE)
		email = params['bots']['email']
		if email not in self.drivers:
			self.drivers[email] =  LinkedinHelper.clone_driver_wait(params['bots']['driver'])
		sel = self.drivers[email]
		args = {'driver': sel}
		profiles_finder = ProfilesFinder(args)
		args = params.copy()
		args['from_page'] = 1
		args['to_page'] = 1
		args['email'] = email
		def profiles_finder_callback(userData):
			self.db.insert(userData)
			output = {'contacts': [userData]}
			LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
			self.pop(params, output, callback)
		profiles_finder.run(args, profiles_finder_callback)
