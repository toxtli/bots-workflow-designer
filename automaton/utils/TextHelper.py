import re
import unicodedata

def clean_text(input_str):
	nfkd_form = unicodedata.normalize('NFKD', input_str)
	only_ascii = nfkd_form.encode('ASCII', 'ignore')
	return only_ascii.decode("utf-8")

def text_between( s, first, last ):
	exit = []
	if s:
		exit = re.findall(first + '(.*?)' + last, s)
	return exit

"""
def text_between( s, first, last ):
	try:
		start = s.rindex( first ) + len( first )
		end = s.rindex( last, start )
		return s[start:end]
	except ValueError:
		return ""
"""