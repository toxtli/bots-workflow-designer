from core.Module import Module
from utils import LogHelper
import requests
from bs4 import BeautifulSoup
import sqlite3

class testcrawler3(Module):
    
    def run(self,params,callback):
        self.MAX_PROCESSES = 1;
        self.push(params,callback,self.run_queue)
    
    def run_queue(self, params, callback):
        LogHelper.log('EXECUTING ' + self.__class__.__name__, True)
        LogHelper.log('INPUT ' + self.__class__.__name__ + ' ' + str(params), True)
        with sqlite3.connect("content.db") as db:
            cursor=db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS content(
            Domain VARCHAR(100),
            Content VARCHAR(500));""")
        value=params["mod2out"]
        resp=requests.get(value)
        soup= BeautifulSoup(resp.text,"lxml")
        cont=soup.find('body').text
        insert_vals=("INSERT INTO content(Domain,Content) VALUES(?,?)")
        cursor.execute(insert_vals,[(value),(cont)])
        db.commit()
        out={"mod3out":"content.db"}
        self.pop(params,out,callback)
