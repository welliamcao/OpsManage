# -*- coding:utf-8 -*-
import json, paramiko,time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from utils.logger import logger
from dao.ipvs import IVPSManage
from websocket.consumers import webTerminalThread

   
class IpvsVipStatus(WebsocketConsumer,IVPSManage):
    def __init__(self, *args, **kwargs):
        super(IpvsVipStatus, self).__init__(*args, **kwargs)  
        self.status = False
    
    def connect(self):
           
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        self.accept()

        self.vips = self.get_ipvs_vip(self.scope['url_route']['kwargs']['id'])

        if not self.vips:
            self.send(text_data="vip不存在")   
            self.close()             
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.vips.ipvs_assets.server_assets.ip, port=int(self.vips.ipvs_assets.server_assets.port), 
                             username=self.vips.ipvs_assets.server_assets.username,
                             password=self.vips.ipvs_assets.server_assets.passwd)
        except Exception as ex:
            self.send(text_data="主机连接失败: {ex}".format(ex=ex))   
            self.close()             
        # 创建channels group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.chan = self.ssh.invoke_shell(term='xterm', width=150, height=30)
        self.chan.settimeout(0)
        self.sshRbt = webTerminalThread(self)
        self.sshRbt.setDaemon(True)
        self.sshRbt.start()
    
    def receive(self, text_data=None, bytes_data=None):
        try:
            request = json.loads(text_data)
            request["is_superuser"] = self.scope["user"].is_superuser
        except Exception as ex:
            self.send(text_data="Server Connect Faailed: {ex}".format(ex=ex))   
            self.sshRbt.stop() 
            self.close() 
        
        if self.status is False:
            
            if request.get("status") == 'open' and request.get("action") == "stats":  
                self.status = True  
                self.chan.send("watch -n1 '{rate}'\n".format(rate=self.vips.stats_vip()))
                
            elif request.get("status") == 'open' and request.get("action") == "rate":
                self.status = True  
                self.chan.send("watch -n1 '{rate}'\n".format(rate=self.vips.rate_vip()))                
        
     
    def user_message(self, event):
        self.send(text_data=event["text"])      

    def disconnect(self, close_code):
        self.sshRbt.stop()       
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
  