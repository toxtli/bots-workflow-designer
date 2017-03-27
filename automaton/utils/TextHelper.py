import re
import unicodedata
from config import Configuration

def get_regexp(text):
	if Configuration.default_datasource == 'sheets':
		return text
	return re.compile(text, re.IGNORECASE)

def clean_text(input_str):
	nfkd_form = unicodedata.normalize('NFKD', input_str)
	only_ascii = nfkd_form.encode('ASCII', 'ignore')
	return only_ascii.decode("utf-8")

def text_between( s, first, last ):
	return re.findall(first + '(.*?)' + last, s)

"""
def text_between( s, first, last ):
	try:
		start = s.rindex( first ) + len( first )
		end = s.rindex( last, start )
		return s[start:end]
	except ValueError:
		return ""
"""