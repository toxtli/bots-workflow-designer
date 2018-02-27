from core.Module import Module
from utils import LogHelper
import csv

class Module4(Module):
    
    def run(self,params,callback):
        self.MAX_PROCESSES = 1;
        self.push(params,callback,self.run_queue)
    
    def run_queue(self, params, callback):
		LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
		LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params), True)
		ans=params["mod2out"]+params["mod3out"]
		out={"mod4out":ans}
		print(out)
		self.pop(params,out,callback)
		ofile=open("output.csv",'a')
		writer=csv.writer(ofile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_ALL)
		writer.writerow([ans])
