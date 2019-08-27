#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from dao.assets import AssetsBase
import paramiko
import threading
import time



class webTerminalThread(threading.Thread):
    def __init__(self, chan):
        super(webTerminalThread, self).__init__()
        self.chan = chan
        self._stop_event = threading.Event()
 
    def stop(self):
        self._stop_event.set()
 
    def run(self):
        self.start_time = time.time()
        while not self._stop_event.is_set():
            try:
                data = self.chan.chan.recv(1024)
                if data:
                    str_data = bytes.decode(data)
                    self.send_msg(str_data)
            except Exception as ex:
                pass
        self.chan.ssh.close()
        self.stop()
 
    def send_msg(self, msg):  
        async_to_sync(self.chan.channel_layer.group_send)(
            self.chan.group_name,
            {
                "type": "user.message",
                "text": msg
            },
        )


class webterminal(WebsocketConsumer,AssetsBase):

    def __init__(self, *args, **kwargs):
        super(webterminal, self).__init__(*args, **kwargs)     


    def connect(self):

        self.group_name = self.scope['url_route']['kwargs']['group_name']

        self.accept()

        assets = self.check_user_assets(userid=self.scope["user"].id, assetsid=self.scope['url_route']['kwargs']['id'])

        if not assets:
            self.send(text_data="主机连接失败: 您没有登录该资产的权限")   
            self.close()             
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(assets.server_assets.ip, int(assets.server_assets.port), assets.server_assets.username, assets.server_assets.passwd)
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
        self.chan.send(text_data)
#         async_to_sync(self.channel_layer.group_send)(
#             self.group_name,
#             {
#                 "type": "user.message",
#                 "text": text_data
#             },
#         ) 
    def user_message(self, event):
        self.send(text_data=event["text"])
 
    def disconnect(self, close_code):
        self.sshRbt.stop()       
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
