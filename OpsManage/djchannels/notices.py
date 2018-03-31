#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import json
from channels.generic.websockets import WebsocketConsumer
from channels import Group
from django.contrib.auth.models import User
from OpsManage.utils.logger import logger

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
            logger.error(msg="webssh连接失败: {ex}".format(ex=str(ex)))     
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
            logger.error(msg="webssh获取用户[{user}]信息失败: {ex}".format(user=self.message.user,ex=str(ex)))
            pass
        Group(user.username).discard(message.reply_channel)    