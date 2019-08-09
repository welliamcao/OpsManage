# -*- coding:utf-8 -*-
import json, time, os, uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from dao.assets import AssetsAnsible
from utils.ansible.runner import ANSRunner
from utils.logger import logger
from deploy.models import *

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)  
    return "%02d:%02d:%02d" % (h, m, s)  

class AnsibleModel(WebsocketConsumer,AssetsAnsible):
    def __init__(self, *args, **kwargs):
        super(AnsibleModel, self).__init__(*args, **kwargs) 
        self.stime = int(time.time())  
        self.logId = None
    
    def send_msg(self, msg, logId):  
        
        self.send(text_data=msg)   
         
        try:
            Deploy_CallBack_Model_Result.objects.create(
                                      logId= logId,
                                      content = msg
                                      )
        except Exception as ex:
            logger.error(msg="记录模块执行日志失败:{ex}".format(ex=ex))
            return False                
    
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        try:
            request = json.loads(text_data)
            request["user"] = self.scope["user"]
            request["is_superuser"] = self.scope["user"].is_superuser
        except Exception as ex:
            self.send(text_data="Ansible Doc运行失败: {ex}".format(ex=ex))   
            self.close() 

        self.run_model(request)
    
    def record_resullt(self,user, ans_model, ans_server, ans_args):
        
        try:
            return Log_Deploy_Model.objects.create(
                                      ans_user = user,
                                      ans_server = ans_server,
                                      ans_args = ans_args,
                                      ans_model = ans_model,
                                      )
        except Exception as ex:
            logger.error(msg="记录剧本执行日志失败:{ex}".format(ex=ex))
            return False        
        
    def run_model(self,request):
        
        sList,resource = self.allowcator(request.get('server_model'), request)
        
        if request.get('deploy_model') == 'custom':
            model_name = request.get('custom_model')
        else:
            model_name = request.get('deploy_model',None)

        count = len(sList)
        
        if count > 0 and request["user"].has_perm('deploy.deploy_exec_deploy_model'):
            
            self.logId = self.record_resullt(self.scope["user"].username, model_name, ','.join(sList), request.get('deploy_args',""))

            if request.get('deploy_debug') == 'on':
                ANS = ANSRunner(hosts=resource,websocket=self,verbosity=4)

            else:
                ANS = ANSRunner(hosts=resource,websocket=self)
                
            if request.get('server_model') == 'inventory_groups':
                sList = ",".join(resource.keys())
                
            ANS.run_model(host_list=sList,module_name=model_name,module_args=request.get('deploy_args',""))  
        
        else:
            self.send("未选择主机或者您没有主机权限")
            self.close()
            
        self.send("\n<font color='white'>执行完成，总共{count}台机器，耗时：{time}</font>".format(count=count, time=format_time(int(time.time())-self.stime)))
        self.close()         
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()
        
        
        
class AnsibleScript(WebsocketConsumer,AssetsAnsible):
    def __init__(self, *args, **kwargs):
        super(AnsibleScript, self).__init__(*args, **kwargs) 
        self.stime = int(time.time())  
        self.logId = None
        
    def send_msg(self, msg, logId):  
        
        self.send(text_data=msg)    
        
        try:
            Deploy_CallBack_Model_Result.objects.create(
                                      logId= logId,
                                      content = msg
                                      )
        except Exception as ex:
            logger.error(msg="记录模块执行日志失败:{ex}".format(ex=ex))
            return False      
    
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        try:
            request = json.loads(text_data)
            request["user"] = self.scope["user"]
            request["is_superuser"] = self.scope["user"].is_superuser
        except Exception as ex:
            self.send(text_data="Ansible Script运行失败: {ex}".format(ex=ex))   
            self.close() 
  
        self.run_scripts(request)
    
    def record_resullt(self,user, ans_model, ans_server, ans_args):
        
        try:
            return Log_Deploy_Model.objects.create(
                                      ans_user = user,
                                      ans_server = ans_server,
                                      ans_args = ans_args,
                                      ans_model = ans_model,
                                      )
        except Exception as ex:
            logger.error(msg="记录剧本执行日志失败:{ex}".format(ex=ex))
            return False 
        
    def run_scripts(self,request):

        sList,resource = self.allowcator(request.get('server_model'), request)         
        
        count = len(sList)                      
                                             
        if count > 0 and request.get('script_file') and request["user"].has_perm('deploy.deploy_exec_deploy_script'):      
            self.logId = self.record_resullt(self.scope["user"].username, 'script', ','.join(sList), request.get('script_args',""))
                   
            filePath = self.saveScript(content=request.get('script_file'),filePath='/tmp/script-{ram}'.format(ram=uuid.uuid4().hex[0:8]))
            if request.get('deploy_debug') == 'on':
                ANS = ANSRunner(resource,websocket=self,verbosity=4)
                
            else:
                ANS = ANSRunner(hosts=resource,websocket=self)
                
            if request.get('server_model') == 'inventory_groups':
                sList = ",".join(resource.keys())
                
            ANS.run_model(host_list=sList,module_name='script',module_args="{filePath} {args}".format(filePath=filePath,args=request.get('script_args')))
            
            try:
                os.remove(filePath)
            except Exception as ex:
                logger.warn(msg="删除文件失败: {ex}".format(ex=ex))             
    
        else:
            self.send("未选择主机或者您没有主机权限")
            self.close()
               
        self.send("\n<font color='white'>执行完成，总共{count}台机器，耗时：{time}</font>".format(count=count, time=format_time(int(time.time())-self.stime)))
        self.close()       
      
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)     
        self.close()
        
class AnsiblePlaybook(WebsocketConsumer,AssetsAnsible):
    def __init__(self, *args, **kwargs):
        super(AnsiblePlaybook, self).__init__(*args, **kwargs) 
        self.stime = int(time.time())  
        self.logId = None
        
    def send_msg(self, msg, logId): 
         
        self.send(text_data=msg)    
        
        try:
            Deploy_CallBack_PlayBook_Result.objects.create(
                                      logId= logId,
                                      content = msg
                                      )
        except Exception as ex:
            logger.error(msg="记录模块执行日志失败:{ex}".format(ex=ex))
            return False     
    
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        try:
            request = json.loads(text_data)
            request["user"] = self.scope["user"]
            request["is_superuser"] = self.scope["user"].is_superuser
        except Exception as ex:
            self.send(text_data="Ansible Playbook运行失败: {ex}".format(ex=ex))   
            self.close() 
               
        self.run_playbook(request)
    
    def record_resullt(self,ans_id, ans_user, ans_name, ans_content, ans_server):       
        try:
            return Log_Deploy_Playbook.objects.create(
                                      ans_id = ans_id,
                                      ans_user = ans_user,
                                      ans_server = ans_server,
                                      ans_name = ans_name,
                                      ans_content = ans_content,
                                      )
        except Exception as ex:
            logger.error(msg="记录剧本执行日志失败:{ex}".format(ex=ex))
            return False     
        
    def run_playbook(self,request):                                       
        try:
            playbook = Deploy_Playbook.objects.get(id=request.get('playbook_id'))
        except Exception as ex:
            self.send("剧本不存在")
            self.close()
            
        if request.get('server_model'):            
            server_model = request.get('server_model')
        
        else:
            server_model = playbook.playbook_type

        sList,resource = self.allowcator(server_model, request)         

        count = len(sList)
                                                            
        playbook_file = os.getcwd()  + str(playbook.playbook_file)                 
        if playbook.playbook_vars:
            playbook_vars = playbook.playbook_vars
        else:
            playbook_vars = request.get('playbook_vars')
        try:
            if len(playbook_vars) == 0:playbook_vars=dict()
            else:playbook_vars = json.loads(playbook_vars)
            playbook_vars['host'] = sList    
        except Exception as ex:
            self.send("读取剧本错误: {ex}" % str(ex))
            self.close()
        #执行ansible playbook
        if count > 0 and request["user"].has_perm('deploy.deploy_exec_deploy_playbook'):           
            self.logId = self.record_resullt(playbook.id, self.scope["user"].username, playbook.playbook_name, playbook.playbook_desc, sList)
            
            ANS = ANSRunner(hosts=resource,websocket=self)                  
            ANS.run_playbook(host_list=sList, playbook_path=playbook_file,extra_vars=playbook_vars)

        else:
            self.send("未选择主机或者您没有主机权限")
            self.close()
               
        self.send("\n<font color='white'>执行完成，总共{count}台机器，耗时：{time}</font>".format(count=count, time=format_time(int(time.time())-self.stime)))
        self.close()           
      
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)     
        self.close()       