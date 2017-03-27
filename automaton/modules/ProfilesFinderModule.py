from core.Module import Module
from utils import LogHelper, LinkedinHelper, TextHelper, DatasourceHelper
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
		self.db = DatasourceHelper.get_dataset({"table": self.DATABASE_TABLE})
		email = params['bots']['email']
		regex_expertise = []
		expertises = params['expertise'].split(',')
		for expertise in expertises:
			expertise = expertise.strip()
			regex_expertise.append(TextHelper.get_regexp(expertise))
		regex_location = []
		locations = params['location'].split(',')
		for location in locations:
			location = location.strip()
			regex_location.append(TextHelper.get_regexp(location))
		records = self.db.select({'email': email,'keywords':{'$in':regex_expertise},'where':{'$in':regex_location}})
		num_results = len(records)
		LogHelper.log('RESULTS_NUMBER', True)
		LogHelper.log(num_results, True)
		if num_results == 0:
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
				self.db.insert_one(userData)
				output = {'contacts': [userData['url']]}
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.pop(params, output, callback)
			profiles_finder.run(args, profiles_finder_callback)
		else:
			for record in records:
				output = {'contacts': [record['url']]}
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.pop(params, output, callback)
