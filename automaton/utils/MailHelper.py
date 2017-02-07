CREATE_EMAILS_API_URL = 'http://hcilab.ml/api/?method=create'

def create_email(params):
	url = CREATE_EMAILS_API_URL + '&domain=' + params['domain'] + \
		'&userId=' + params['username'] + '&firstName=' + params['firstName'] + \
		'&lastName=' + params['lastName']
	email_result = NetworkHelper.get_json(url)
	return email_result