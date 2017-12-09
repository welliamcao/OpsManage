#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import paramiko
import socket
from channels.generic.websockets import WebsocketConsumer
try:
    import simplejson as json
except ImportError:
    import json
from OpsManage.interactive import interactive_shell,get_redis_instance,SshTerminalThread

from django.core.exceptions import ObjectDoesNotExist
from OpsManage.models import Global_Config,User_Server,Server_Assets
from django.contrib.auth.models import User
from django.utils.timezone import now
import os
                
class webterminal(WebsocketConsumer):
    
    ssh = paramiko.SSHClient() 
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True   

    
    def connect(self, message):
        try:
            webssh = Global_Config.objects.get(id=1).webssh
        except Exception,ex:
            webssh = 0
        if webssh != 1:
            self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31m请联系管理员开启WebSSH功能~\033[0m'])},immediately=True)  
            self.disconnect(message)            
        if self.message.user:
            #获取用户信息
            user = User.objects.get(username=self.message.user)    
            if user.is_superuser:
                self.message.reply_channel.send({"accept": True})
            else:
                try:
                    sid = int(self.message.content.get('query_string').split('=')[1])
                except Exception:
                    self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31m"主机不存在或者已被删除"\033[0m'])},immediately=True)  
                    self.disconnect(message) 
                server = User_Server.objects.get(user_id=user.id,server_id=sid)   
                if server:self.message.reply_channel.send({"accept": True})                          
        else:
            self.disconnect(message) 
        
        
    def disconnect(self, message):
        self.closessh()
        
        self.message.reply_channel.send({"accept":False})
        
        self.close()
    
    def queue(self):
        queue = get_redis_instance()
        return queue
    
    def closessh(self):
        self.queue().publish(self.message.reply_channel.name, json.dumps(['close']))
        
    def receive(self,text=None, bytes=None, **kwargs):   
        try:
            if text:
                data = json.loads(text)
                if data[0] == 'id':
                    width = data[2]
                    height = data[3]
                    self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        server = Server_Assets.objects.get(id=data[1])
                    except ObjectDoesNotExist:
                        self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mConnect to server! Server ip doesn\'t exist!\033[0m'])},immediately=True)
                        self.message.reply_channel.send({"accept":False})                        
                    try:
                        self.ssh.connect(server.ip, port=int(server.port), username=server.username, password=server.passwd, timeout=3)
                    except socket.timeout:
                        self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mConnect to server time out\033[0m'])},immediately=True)
                        self.message.reply_channel.send({"accept":False})
                        return
                    except Exception, ex:
                        self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31m连接服务器失败: {ex}\033[0m'.format(ex=str(ex))])},immediately=True)
                        self.message.reply_channel.send({"accept":False})
                        return
                    
                    chan = self.ssh.invoke_shell(width=width, height=height,)
                    sRbt=SshTerminalThread(self.message,chan)
                    sRbt.setDaemon = True
                    sRbt.start()     
                    
                    directory_date_time = now()
                    log_name = os.path.join('{0}-{1}-{2}'.format(directory_date_time.year,directory_date_time.month,directory_date_time.day),'{0}.json'.format('cmdlogs'))
                    interactive_shell(chan,self.message.reply_channel.name,log_name=log_name,width=width,height=height)
                    
                elif data[0] in ['stdin','stdout']:
                    self.queue().publish(self.message.reply_channel.name, json.loads(text)[1])
                elif data[0] == u'set_size':
                    self.queue().publish(self.message.reply_channel.name, text)
                else:
                    self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mUnknow command found!\033[0m'])},immediately=True)
            elif bytes:
                self.queue().publish(self.message.reply_channel.name, json.loads(bytes)[1])
        except socket.error:
            self.closessh()
            self.close()
        except Exception,e:
            import traceback
            print traceback.print_exc()
            self.closessh()
            self.close()

