import sys, json, traceback
from utils import LogHelper

args = {}

def load_config(filepath):
	data = json.load(open(filepath,'r'))
	load({
		'json': data
	})

def set_values(module, value):
	global args
	args['modules'][module].set_values(value)

def load(params):
	global args
	LogHelper.log('STARTING', True)
	exit = '{"status":"OK"}'
	data = params['json']
	if data:
		exit = json.dumps(data)
		# LogHelper.log(exit)
		args['modules'] = {}
		values = []
		for module in data['modules']:
			args['modules'][module['name']] = get_obj(module['class'])
			LogHelper.log(module['name'] + ' = ' + module['class'] + '()')
			content = {}
			for field in module['fields']:
				args['modules'][module['name']].add_node(field)
				LogHelper.log(module['name'] + ".add_node(" + json.dumps(field) + ")")
				if field['value']:
					content[field['name']] = field['value']
			if content:
				values.append({'window':module['name'],'content':content})
		for connection in data['connections']:
			args['modules'][connection['from']['window']].connect({'name':connection['from']['variable'], 'target':args['modules'][connection['to']['window']]})
			LogHelper.log(connection['from']['window'] + ".connect({'name':'" + connection['from']['variable'] + "', 'target':" + connection['to']['window'] + "})")
		while values:
			record = values.pop()
			LogHelper.log(record['window'] + ".set_values(" + json.dumps(record['content']) + ")")
			args['modules'][record['window']].set_values(record['content'])
	return exit

def get_obj(className):
	mod = __import__('modules.' + className, fromlist=[className])
	klass = getattr(mod, className)
	return klass()

def get_endpoints():
	return {
		'endpoints': {
			'/load': load
		}
	}
