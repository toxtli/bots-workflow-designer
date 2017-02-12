from utils import NetworkHelper, MailHelper, LogHelper, TextHelper

class ProfilesGenerator(object):

	RANDOM_USERS_API_URL = 'https://randomuser.me/api/'
	
	DOMAIN_NAME = 'hcilab.ml'
	DEFAULT_PASSWORD = 'edupassword'

	def run(self, params, callback=None, batch=False):
		results = self.generate_profiles(params)
		if batch:
			profiles = []
		for result in results['results']:
			profile = self.complete_profile(params, result)
			email_result = MailHelper.create_email(profile)
			LogHelper.log('EMAIL RESULT')
			LogHelper.log(email_result)
			profile['emailCreated'] = True
			if batch:
				profiles.append(profile)
			elif callback:
				callback(profile)
		if batch:
			if callback:
				callback(profiles)
			else:
				return profiles	

	def generate_profiles(self, params):
		extra = ''
		num_results = 10
		if 'num_results' in params:
			num_results = int(params['num_results'])
		elif 'feedback' in params:
			if params['feedback'].isdigit():
				num_results = int(params['feedback'])
		extra += '&results=' + str(num_results)
		if params['gender']:
			if params['gender'] == 'male' or params['gender'] == 'female':
				extra += '&gender=' + params['gender']
		url = self.RANDOM_USERS_API_URL + '?format=pretty&nat=es' + extra
		results = NetworkHelper.get_json(url)
		return results

	def complete_profile(self, params, result):
		profile = {
			'network': params['platforms'],
			'expertise': params['expertise'],
			'gender': result['gender'],
			'firstName': result['name']['first'],
			'lastName': result['name']['last'],
			'country': result['nat'],
			'state': result['nat'],
			'country': result['nat'],
			'state': result['location']['state'],
			'city': result['location']['city'],
			'street': result['location']['street'],
			'zip': result['location']['postcode'],
			'imageSmall': result['picture']['large'],
			'imageMedium': result['picture']['medium'],
			'imageThumb': result['picture']['thumbnail'],
			'phone': result['phone'],
			'mobile': result['cell'],
			'birthday': result['dob'],
			'accountCreated': False,
			'emailCreated': False,
			'triedOnce': False,
			'suspended': False,
			'cookies': False,
			'password': self.DEFAULT_PASSWORD
		}
		profile['username'] = TextHelper.clean_text(result['email'].split('@')[0])
		profile['domain'] = self.DOMAIN_NAME
		profile['email'] = profile['username'] + '@' + profile['domain']
		return profile
