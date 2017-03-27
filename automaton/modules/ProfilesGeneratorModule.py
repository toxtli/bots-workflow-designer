from core.Module import Module
from utils import LogHelper, CsvHelper, TextHelper, DatasourceHelper
from modules.ProfilesGenerator.ProfilesGenerator import ProfilesGenerator

class ProfilesGeneratorModule(Module):

	DATABASE_TABLE = 'profiles'
	FORCE_STOP = False

	def run(self, params, callback):
		self.MAX_PROCESSES = 1
		self.push(params, callback, self.run_queue)
		# super(self.__class__, self).run(params, callback)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatasourceHelper.get_dataset({"table": self.DATABASE_TABLE})
		if params['feedback']:
			num_results = CsvHelper.gsheets_get_num_rows(params['feedback'])
		params['expertise'] = 'Software Engineer'
		params['location'] = 'United States'
		LogHelper.log(params['expertise'], True)
		LogHelper.log(params['location'], True)
		regex_expertise = self.get_as_regex(params['expertise'])
		regex_location = self.get_as_regex(params['location'])
		records = self.db.select({'suspended': False,'expertises':{'$in':regex_expertise},'country':{'$in':regex_location}})
		existing = len(records)
		LogHelper.log(existing)
		if existing < num_results:
			restant = num_results - existing
			params['num_results'] = restant
			LogHelper.log('CREATING ACCOUNTS ' + str(restant), True)
			profiles_generator = ProfilesGenerator()
			def profiles_generator_callback(profile):
				output = {'profiles': [profile]}
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.db.insert_one(profile)
				self.pop(params, output, callback)
			profiles_generator.run(params, profiles_generator_callback)
		if existing != 0:
			if existing < num_results:
				to_value = existing
			else:
				to_value = num_results
			cont = 0
			for i in range(to_value):
				profile = records[i]
				output = {'profiles': [profile]}
				LogHelper.log('EXTRACTING ACCOUNTS', True)
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.pop(params, output, callback)

	def get_as_regex(self, text):
		regexs = []
		values = text.split(',')
		for value in values:
			value = value.strip()
			regexs.append(TextHelper.get_regexp(value))
		return regexs

