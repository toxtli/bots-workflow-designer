from googlevoice import Voice
import sys
import BeautifulSoup
from config import Configuration

def get_sms_last():
    sms_list = get_sms_list()
    return sms_list.pop(0)

def get_sms_list():
    voice = Voice()
    voice.login(email=Configuration.sms_user, passwd=Configuration.sms_password)
    voice.sms()
    sms_list = []
    for msg in extractsms(voice.sms.html):
        sms_list.append(str(msg))
    return sms_list

def extractsms(htmlsms) :
    msgitems = []
    tree = BeautifulSoup.BeautifulSoup(htmlsms)
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in reversed(rows) :
            msgitem = {"id" : conversation["id"]}
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()
            msgitems.append(msgitem)
    return msgitems
