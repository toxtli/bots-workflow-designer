from config import Configuration

def log(output, severity=None):
	if Configuration.debug or severity:
		print(output)