from core.Module import Module
from utils import LogHelper, LinkedinHelper, DatasourceHelper
from modules.ConnectionRequester.ConnectionRequester import ConnectionRequester

class ConnectionRequesterModule(Module):

	DATABASE_TABLE = 'contacts'

	def run(self, params, callback):
		self.MAX_PROCESSES = 10
		self.push(params, callback, self.run_queue)

	def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params))
		self.db = DatasourceHelper.get_dataset({"table": self.DATABASE_TABLE})
		email = params['bots']['email']
		urls = params['contacts']
		for url in urls:
			contact = self.db.select_one({'email':email, 'url':url})
			if not contact['friend']:
				if contact['status'] == 'FOUND':
					sel = LinkedinHelper.clone_driver_wait(params['bots']['driver'])
					args = {'driver': sel}
					connection_requester = ConnectionRequester(args)
					def connection_requester_callback(url):
						self.db.update_one({'email':email,'url':url},{'status':'INVITED'})
						output = {'accepted': [url]}
						LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
						self.pop(params, output, callback)
					connection_requester.run(params, connection_requester_callback)
				else:
					LogHelper.log('ALREADY INVITED')
					output = {'accepted': [url]}
					LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
					self.pop(params, output, callback)
			else:
				LogHelper.log('NO CONNECTION NEEDED')
				output = {'accepted': [url]}
				LogHelper.log('OUTPUT ' + self.__class__.__name__ + ' ' + str(output))
				self.pop(params, output, callback)
