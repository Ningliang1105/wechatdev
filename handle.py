# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import reply
import receive
import web
import os
import time
import lxml
import cognitive_face as CF


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
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    print recMsg.Content, type(recMsg.Content), recMsg.Content[:2]
                    if recMsg.Content[:2] == '天气':
                        replyMsg = reply.TextMsg(toUser, fromUser, 'weather')
                        return replyMsg.send()
                    else:
                        replyMsg = reply.TextMsg(toUser, fromUser, 'test')
                        return replyMsg.send()
                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
                #content = '图中人物性别为'+datas[0]+'\n'+'年龄为'+datas[1]
                #replyMsg = reply.TextMsg(toUser, fromUser, content)
                #return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment