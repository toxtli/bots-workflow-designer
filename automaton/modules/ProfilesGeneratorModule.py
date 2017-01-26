import requests
from core.Module import Module

class ProfilesGeneratorModule(Module):

	def run(self, params, callback):
		print('RUNNING ' + self.__class__.__name__)
		print('INPUT ' +  str(params))
		r = requests.get('https://randomuser.me/api/?nat=es&results=10&format=pretty')
		results = r.json()
		profiles = []
		for result in results['results']:
			profiles.append({
				'expertise': params['expertise'],
				'gender': result['gender'],
				'firstname': result['name']['first'],
				'lastname': result['name']['last'],
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
				'birthday': result['dob']
			})
		output = {'profiles': profiles}
		print('OUTPUT ' +  str(output))
		callback(params, output)
