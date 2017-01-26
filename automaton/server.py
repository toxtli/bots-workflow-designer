import sys, json, traceback
from flask.app import Flask, request
from flask_cors.extension import CORS
from flask_cors.decorator import cross_origin
from flask.globals import request

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['DEBUG'] = True

@app.route("/", methods=['GET', 'POST'])
@cross_origin()
def index():
	exit = '{"status":"OK"}'
	data = request.json
	if data:
		exit = json.dumps(data)
		print(exit)
		modules = {}
		values = []
		for module in data['modules']:
			modules[module['name']] = get_obj(module['class'])
			print(module['name'] + ' = ' + module['class'] + '()')
			content = {}
			for field in module['fields']:
				modules[module['name']].add_node(field)
				print(module['name'] + ".add_node(" + json.dumps(field) + ")")
				if field['value']:
					content[field['name']] = field['value']
			if content:
				values.append({'window':module['name'],'content':content})
		for connection in data['connections']:
			modules[connection['from']['window']].connect({'name':connection['from']['variable'], 'target':modules[connection['to']['window']]})
			print(connection['from']['window'] + ".connect({'name':'" + connection['from']['variable'] + "', 'target':" + connection['to']['window'] + "})")
		while values:
			record = values.pop()
			print(record['window'] + ".set_values(" + json.dumps(record['content']) + ")")
			modules[record['window']].set_values(record['content'])
	return exit

def get_obj(className):
	mod = __import__('modules.' + className, fromlist=[className])
	klass = getattr(mod, className)
	return klass()

if __name__ == "__main__":
    app.run()