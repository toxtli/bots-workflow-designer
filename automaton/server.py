from config import Configuration
from utils import NetworkHelper, StateMachineHelper

StateMachineHelper.load_config(Configuration.logic_file)
NetworkHelper.config_server(StateMachineHelper.get_endpoints())
NetworkHelper.start_server({
	'host': '0.0.0.0',
	'port': 5000,
	'debug': False
})