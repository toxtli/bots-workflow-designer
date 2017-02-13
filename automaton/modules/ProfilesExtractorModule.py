from core.Module import Module
from utils import LogHelper, LinkedinHelper
from utils.DatabaseHelper import DatabaseHelper
from utils.SeleniumHelper import SeleniumHelper
from modules.ProfilesExtractor.ProfilesExtractor import ProfilesExtractor

class ProfilesExtractorModule(Module):

	# CONFIG

	DATABASE_TABLE = 'contacts'
	MODE = 'LOGGED'

	def run(self, params, callback):
		self.MAX_PROCESSES = 10
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatabaseHelper(table=self.DATABASE_TABLE)	
		bot_email = params['bots']['email']
		if self.MODE == 'LOGGED':
			sel = LinkedinHelper.clone_driver(params['bots']['driver'])
		else:
			sel = SeleniumHelper()
		args = {'driver': sel}
		profiles_extractor = ProfilesExtractor(args)
		def profiles_extractor_callback(userdata):
			self.db.update({'url':userdata['userUrl']},{'userId':userdata['connId'], 'userdata':userdata})
			output = {'userdata': [userdata['userUrl']]}
			LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
			self.pop(params, output, callback)
		profiles_extractor.run(params, profiles_extractor_callback)
