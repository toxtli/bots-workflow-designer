import time
from config import Configuration
from utils import NetworkHelper

URL_NEW_CONVERSATION = 'https://directline.botframework.com/v3/directline/conversations'
URL_ACTIVITIES = 'https://directline.botframework.com/v3/directline/conversations/[ID]/activities'
WAIT = 4

def new_conversation():
	result = NetworkHelper.post_json(URL_NEW_CONVERSATION, headers=get_headers())
	return result

def send_and_wait_response(conversationId, message, wait=WAIT):
	sent = send_message(conversationId, message)
	times = 0
	response = ''
	while times < wait and not response:
		time.sleep(1)
		times += 1
		activities = get_activities(conversationId)
		for activity in activities['activities']:
			if 'replyToId' in activity:
				if activity['replyToId'] == sent['id']:
					response = activity['text']
	return response

def send_message(conversationId, message):
	payload = {
	  "type": "message",
	  "from": {
	    "id": "bot"
	  },
	  "text": message
	}
	url = URL_ACTIVITIES.replace('[ID]', conversationId)
	result = NetworkHelper.post_json(url, json=payload, headers=get_headers())
	return result

def get_activities(conversationId):
	url = URL_ACTIVITIES.replace('[ID]', conversationId)
	result = NetworkHelper.get_json(url, headers=get_headers())
	return result

def get_headers():
	return {
		'Authorization': 'Bearer ' + Configuration.mbf_secret
	}