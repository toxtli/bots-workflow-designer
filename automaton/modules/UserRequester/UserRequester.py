import json
import requests
from utils import LogHelper, NetworkHelper, StateMachineHelper

class UserRequester(object):

	app = None

	def __init__(self):
		NetworkHelper.config_server({
			'endpoints': {
				'/webhook-lrs': self.webhook
			}
		})

	def webhook(self, params):
		LogHelper.log('WEBHOOK RECEIVED ...')
		info = params['json']
		LogHelper.log(info)
		if info:
			LogHelper.log('WEBHOOK JSON ...')
			url = ''
			for record in info:
				if record['verb'] == 'attempted' or record['verb'] == 'experienced':
					if record['object']['objectType'] == 'Activity':
						LogHelper.log('WEBHOOK FORMAT CORRECT...')
		StateMachineHelper.set_values('user', {
			'expertise': 'Software Engineer'
		})
		return '{"status":"webhook"}'
