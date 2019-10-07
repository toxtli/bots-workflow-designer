import urllib
import time
import threading
import requests
from flask import Flask, request
from flask_cors import CORS
from utils import LogHelper
from multiprocessing import Process

args = None

def url_encode(url):
	return urllib.quote(url, safe='')

def dict_to_querystring(params):
	return urllib.urlencode(params)

def get_json(url, headers=None):
	LogHelper.log(url)
	r = requests.get(url, headers=headers)
	return r.json()

def post_json(url, json=None, headers=None):
	r = requests.post(url, json=json, headers=headers)
	return r.json()

def get(url):
	r = requests.get(url)
	return r.text

def hello():
	return '{"status":"OK"}'

def honeypot(path=''):
	global args
	params = {
		'path': path,
		'headers': request.headers,
		'qs': request.query_string,
		'all': request.values,
		'get': request.args,
		'post': request.form,
		'method': request.method,
		'files': request.files,
		'cookies': request.cookies,
		'json': request.json
	}
	clean_path = path.split('/')[0]
	full_path = '/' + clean_path
	if full_path in args['endpoints']:
		return args['endpoints'][full_path](params)
	else:
		return '{"status":" ' + full_path + '"}'

def init_params():
	global args
	if not args:
		args = {
			'name': __name__,
			'port': 8080,
			'host': '0.0.0.0',
			'debug': True,
			'endpoints': {}
		}

def config_server(params):
	global args
	init_params()
	if params:
		for param in params:
			if param != 'endpoints':
				args[param] = params[param]
			else:
				for index in params[param]:
					args[param][index] = params[param][index]

def start_server(params):
	global args
	LogHelper.log('CREATING SERVER')
	config_server(params)
	app = Flask(args['name'])
	CORS(app)
	app.add_url_rule('/', '/', honeypot, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
	app.add_url_rule('/<path:path>', '/<path:path>', honeypot, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
	args['app'] = app
	run_server()

def run_server():
	global args
	args['app'].run(host= args['host'],port=args['port'], debug=args['debug'])
