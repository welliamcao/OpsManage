#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import json
from channels.generic.websockets import WebsocketConsumer
from channels import Group
from django.contrib.auth.models import User

class WebNotice(WebsocketConsumer):
    
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True  
        
    def connect(self,message,**kwargs):
        try:
            username = message['path'].strip('/').split('/')[-1]
        except Exception, ex:
            message.reply_channel.send({"accept":False}) 
            print ex        
        try:
            user = User.objects.get(username=self.message.user)  
        except Exception,ex:
            message.reply_channel.send({"accept":False}) 

        if str(self.message.user) == str(username):
            message.reply_channel.send({'accept': True})
            Group(user.username).add(message.reply_channel)
#             Group(user.username).send({'text': json.dumps(["连接成功"])})
    
        
    def disconnect(self,message,**kwargs):
        try:
            user = User.objects.get(username=self.message.user)
        except Exception,ex:
            print ex
            pass
        Group(user.username).discard(message.reply_channel)    