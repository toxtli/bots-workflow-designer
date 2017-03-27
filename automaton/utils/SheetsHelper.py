import sys, json, urllib
from utils import LogHelper, NetworkHelper
from config import Configuration

class SheetsHelper():
	
	def select(self, where, table=None):
		result = False
		try:
			col = self.get_collection('select', table)
			col += self.encode(where)
			LogHelper.log(col)
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def select_one(self, where, table=None):
		result = False
		try:
			col = self.get_collection('select_one', table)
			col += self.encode(where)
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def insert(self, params, table=None):
		result = False
		try:
			col = self.get_collection('insert', table)
			col += self.encode(params)
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def insert_one(self, params, table=None):
		result = False
		try:
			col = self.get_collection('insert_one', table)
			col += self.encode(params)
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def update(self, where, params, table=None):
		result = False
		try:
			col = self.get_collection('update', table)
			col += self.encode([where, params])
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def update_one(self, where, params, table=None):
		result = False
		try:
			col = self.get_collection('update_one', table)
			col += self.encode([where, params])
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def delete(self, where, table=None):
		result = False
		try:
			col = self.get_collection('delete', table)
			col += self.encode(where)
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def delete_one(self, where, table=None):
		table = table if table else self.table
		result = False
		try:
			col = self.get_collection('delete_one', table)
			col += self.encode(where)
			result = NetworkHelper.get_json(col)
			result = result['row']
		except:
			LogHelper.log(sys.exc_info())
		return result

	def count(self, where, table=None):
		return self.select(where, table).count()

	def encode(self, value):
		return urllib.quote_plus(json.dumps(value))

	def get_collection(self, action, table):
		table = table if table else self.table
		return self.url + '?action=' + action + '&table=' + table + '&params='

	def __init__(self, params=None):
		self.table = params['table'] if params and 'table' in params else Configuration.db_collection
		self.url = params['table'] if params and 'url' in params else Configuration.sheets_url
