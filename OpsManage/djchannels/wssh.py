#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import paramiko
import socket
from channels.generic.websockets import WebsocketConsumer
try:
    import simplejson as json
except ImportError:
    import json
from OpsManage.utils.interactive import interactive_shell,get_redis_instance,SshTerminalThread
from OpsManage.models import Global_Config,User_Server,Server_Assets
from django.contrib.auth.models import User
from OpsManage.utils.logger import logger
                
class webterminal(WebsocketConsumer):
    
    ssh = paramiko.SSHClient() 
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True   

    
    def connect(self,message,**kwargs):
        try:
            webssh = Global_Config.objects.get(id=1).webssh
        except Exception,ex:
            webssh = 0
        if webssh != 1:
            message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31m请联系管理员开启WebSSH功能~\033[0m'])},immediately=True)  
            message.reply_channel.send({"accept":False}) 
            self.disconnect(message)            
        if self.message.user:
            #获取用户信息
            user = User.objects.get(username=self.message.user)  
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())      
            self.ssh.load_system_host_keys()    
            try:
                sid = int(message['path'].strip('/').split('/')[-1])
            except Exception:
                message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31m"主机不存在或者已被删除"\033[0m'])},immediately=True)  
                self.disconnect(message)      
            try:
                if user.is_superuser:
                    server = Server_Assets.objects.get(id=sid)                  
                else:
                    user_server = User_Server.objects.get(user_id=user.id,server_id=sid)
                    server = Server_Assets.objects.get(id=user_server.server_id) 
            except:
                message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31m"主机不存在或者已被删除"\\033[0m'])},immediately=True)
                message.reply_channel.send({"accept":False})
                self.disconnect(message)                                    
            try:
                if server.username == 'root':keyfile = "/root/.ssh/id_rsa"
                else:keyfile = "/home/{user}/.ssh/id_rsa".format(user=server.username) 
                pkey = paramiko.RSAKey.from_private_key_file(keyfile)                 
                self.ssh.connect(server.ip, port=int(server.port), username=server.username, password=server.passwd, timeout=3, pkey=pkey)
            except socket.timeout:
                message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mConnect to server time out\033[0m'])},immediately=True)
                message.reply_channel.send({"accept":False})
                self.disconnect(message) 
                return
            except Exception, ex:
                message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31m连接服务器失败: {ex}\033[0m'.format(ex=str(ex))])},immediately=True)
                message.reply_channel.send({"accept":False})
                self.disconnect(message) 
                return
            self.chan = self.ssh.invoke_shell(width=150, height=100)
            sRbt=SshTerminalThread(self.message,self.chan)
            sRbt.setDaemon = True    
            if user.is_superuser and server:
                sRbt.start()   
                interactive_shell(self.chan,message.reply_channel.name)                
                message.reply_channel.send({"accept": True})
            elif server:
                sRbt.start()   
                interactive_shell(self.chan,message.reply_channel.name)  
                message.reply_channel.send({"accept": True})                  
        else:
            self.disconnect(message) 
        
        
    def disconnect(self, message,**kwargs):
        self.closessh()
        message.reply_channel.send({"accept":False})
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
                if data[0] in ['stdin','stdout']:
                    self.queue().publish(self.message.reply_channel.name, json.loads(text)[1])
                elif data[0] == u'set_size':
                    self.queue().publish(self.message.reply_channel.name, text)
#                 else:
#                     self.message.reply_channel.send({"text":json.dumps(['stdout','\033[1;3;31mUnknow command found!\033[0m'])},immediately=True)
            elif bytes:
                self.queue().publish(self.message.reply_channel.name, json.loads(bytes)[1])
        except socket.error:
            self.closessh()
            self.close()
        except Exception,e:
            import traceback
            print traceback.print_exc()
            logger.error(msg="webssh receive failed: {ex}".format(ex=str(traceback.print_exc())))
            self.closessh()
            self.close()

