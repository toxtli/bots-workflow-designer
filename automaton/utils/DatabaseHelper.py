import sys
from utils import LogHelper
from config import Configuration
from pymongo import MongoClient

class DatabaseHelper():
	
	def select(self, where, table=None):
		col = self.get_collection(table)
		return list(col.find(where))

	def select_one(self, where, table=None):
		col = self.get_collection(table)
		return col.find_one(where)

	def insert(self, params, table=None):
		result = False
		try:
			col = self.get_collection(table)
			result = col.insert_many(params).inserted_ids
		except:
			LogHelper.log(sys.exc_info())
		return result

	def insert_one(self, params, table=None):
		result = False
		try:
			col = self.get_collection(table)
			result = col.insert_one(params).inserted_id
		except:
			LogHelper.log(sys.exc_info())
		return result

	def update(self, where, params, table=None):
		result = False
		try:
			col = self.get_collection(table)
			result = col.update_many(where, {"$set": params}).modified_count
		except:
			LogHelper.log(sys.exc_info())
		return result

	def update_one(self, where, params, table=None):
		result = False
		try:
			col = self.get_collection(table)
			result = col.update_one(where, {"$set": params}).modified_count
		except:
			LogHelper.log(sys.exc_info())
		return result		

	def delete(self, where, table=None):
		result = False
		try:
			col = self.get_collection(table)
			result = col.delete_many(where).deleted_count
		except:
			LogHelper.log(sys.exc_info())
		return result

	def delete_one(self, where, table=None):
		result = False
		try:
			col = self.get_collection(table)
			result = col.delete_one(where).deleted_count
		except:
			LogHelper.log(sys.exc_info())
		return result

	def count(self, where, table=None):
		col = self.get_collection(table)
		return col.find(where).count()

	def get_collection(self, table):
		table = table if table else self.table
		return self.db[table]

	def connect(self):
		self.client = MongoClient(Configuration.db_host)
		self.db = self.client[Configuration.db_name]

	def __init__(self, table=None):
		self.table = table if table else Configuration.db_collection
		self.connect()
