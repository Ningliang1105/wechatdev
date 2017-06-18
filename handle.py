# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import reply
import receive
import web
import os
import time
import lxml
import hashlib
import requests
import re

def imgtest(picurl):
    print "Hello world"
    s = requests.session()
    url = 'http://how-old.net/Home/Analyze?isTest=False&source=&version=001'
    header = {
    'Accept-Encoding':'gzip, deflate',
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
    'Host': "how-old.net",
    'Referer': "http://how-old.net/",
    'X-Requested-With': "XMLHttpRequest"
        }
    print "OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    data = {'file':s.get(picurl).content}
    #data = {'file': open(sid+'.jpg', 'rb')}
    #此处打开指定的jpg文件

    print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH2"


    r = s.post(url, files=data, headers=header)
    h = r.content
    i = h.replace('\\','')
    #j = eval(i)
    print i

    gender = re.search(r'"gender": "(.*?)"rn', i)
    age = re.search(r'"age": (.*?),rn', i)
    if gender.group(1) == 'Male':
        gender1 = '男'
    else:
        gender1 = '女'
    #print gender1
    #print age.group(1)
    datas = [gender1, age.group(1)]
    return datas

class Handle(object):

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)


    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "ningliang" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            #print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = "Your ID is", str(toUser)
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            elif recMsg.MsgType == 'image':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                picurl = recMsg.PicUrl
                print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
                datas = imgtest(picurl)
                content = '图中人物性别为'+datas[0]+'\n'+'年龄为'+datas[1]
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment