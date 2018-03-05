from core.Module import Module
from utils import LogHelper
import requests
from bs4 import BeautifulSoup

class testcrawler(Module):

    def run(self, params, callback):
        self.MAX_PROCESSES = 1
        self.push(params, callback, self.run_queue)

    def run_queue(self, params, callback):
        LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
        LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params), True)
        output = {}
        val=params["mod1out"]
        URL="https://www.google.co.in/search?q="+str(val)
        r  = requests.get(URL)
        data = r.text
        soup = BeautifulSoup(data,"lxml")
        for item in soup.select('.r a'):
            myurl=item.get('href')
            u=myurl.find('http')
            if(u!=-1):
                u=myurl.replace(myurl[:u],'')
                u=u.split('&')
                u=u[0]
                output["mod2out"]=u
                self.pop(params, output, callback)