from config import Configuration
from utils.DatabaseHelper import DatabaseHelper
from utils.SheetsHelper import SheetsHelper

def get_dataset(params=None):
	dataset = None
	source = params['source'] if params and 'source' in params else Configuration.default_datasource
	if source == 'sheets':
		dataset = SheetsHelper(params)
	else:
		dataset = DatabaseHelper(params)
	return dataset