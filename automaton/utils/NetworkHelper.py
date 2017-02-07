import requests

def get_json(url):
	r = requests.get(url)
	return r.json()

def get(url):
	r = requests.get(url)
	return r.text
