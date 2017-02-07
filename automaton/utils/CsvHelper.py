from utils import NetworkHelper

def gsheets_get_num_rows(url):
	result = NetworkHelper.get(url)
	num_results = result.count('\n') + 1
	return num_results