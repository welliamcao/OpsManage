#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import json,time
from OpsManage.utils.spider import Spider
from channels.generic.websockets import WebsocketConsumer
from channels import Group
from django.contrib.auth.models import User

class WebChat(WebsocketConsumer):
    
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True  
    spider = Spider()
    
    def chat(self,msg):
        return self.spider.chat(msg)
        
    def connect(self,message,**kwargs):     
        if self.message.user:
            try:
                user = User.objects.get(username=self.message.user)  
            except Exception,ex:
                message.reply_channel.send({"accept":False})  
            message.reply_channel.send({'accept': True})
            Group("chats").add(message.reply_channel)            
        else:           
            message.reply_channel.send({"accept":False})  
            self.disconnect(message)             
#             Group(user.username).send({'text': json.dumps(["连接成功"])})
    def receive(self,text=None, bytes=None, **kwargs):
        try:
            if text:
                data = json.loads(text)
                msg = self.chat(data.get('msg'))
                self.message.reply_channel.send({"text":json.dumps({"msg":msg,"ctime":"{ctime}".format(ctime=time.strftime('%Y-%m-%d %H:%M:%S' ,time.localtime())),"user":'Robot'})},immediately=True)
        except Exception, ex:
            print ex
       
        
    def disconnect(self,message,**kwargs):
        Group("chats").discard(message.reply_channel)    