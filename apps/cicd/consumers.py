# -*- coding:utf-8 -*-
import json, time, ast, uuid
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from dao.cicd import AppsManage
from utils.ansible.runner import ANSRunner
from utils.logger import logger
from cicd.models import *
from dao.redisdb import DsRedis
from cicd.service.deploy import DeployRunner

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)  
    return "%02d:%02d:%02d" % (h, m, s)  

class AppsDeploy(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(AppsDeploy, self).__init__(*args, **kwargs) 
        self.stime = int(time.time())  
    
  
    def connect(self):
        self.project = self.get_apps(self.scope['url_route']['kwargs']['id'])
        
        if self.project:
            self.group_name = self.scope['url_route']['kwargs']['group_name']
            
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
 
            self.accept()            
        else:
            self.close()
        


    def receive(self, text_data=None, bytes_data=None):
        try:
            request = json.loads(text_data)
            request["is_superuser"] = self.scope["user"].is_superuser
        except Exception as ex:
            self.send(json.dumps({"status":"failed","msg":"代码部署失败: {ex}".format(ex=ex)}))   
            self.disconnect(1000)
            
        if request.get('action') == "deploy":
            self.run_deploy(request)
            
        elif request.get('action') == "rollback":
            self.run_rollback(request)
        else:
            self.check_apps_deploy_status(1000)
        
    def get_apps(self,ids):
        try:
            return Project_Config.objects.get(id=ids)
        except Exception as ex:
            logger.warn(msg="获取部署项目失败: {ex}".format(ex=ex))
            return False
    
    def get_task(self,ids):
        try:
            return Log_Project_Config.objects.get(id=ids)
        except Exception as ex:
            logger.warn(msg="获取部署项目任务失败: {ex}".format(ex=ex))
            return False    
    
    def check_apps_deploy_status(self,project):
        if DsRedis.OpsProject.get(redisKey=project.project_uuid+"-locked") is None:#判断该项目是否有人在部署
            return True
        return  False
    
    def check_role(self,request,project,role='manage'):
        if request["is_superuser"]:return True
        try:
            return Project_Roles.objects.get(project=project,user=request.get("userid"),role=role)
        except Exception as ex:
            return False   
    
    def save_deploy_logs(self,key, msg, title, task_id, status):
        AppsManage.create_app_deploy_details_record(self, key=key, msg=msg, title=title, task_id=task_id, status=status)
            
    def run_deploy(self,request):
        
        if self.check_apps_deploy_status(self.project):
            DsRedis.OpsProject.set(redisKey=self.project.project_uuid+"-locked",value=self.scope["user"].username)                        
            if self.check_role(request, self.project):
                task = AppsManage.create_app_deploy_record(self, project=self.project, username=self.scope["user"].username, 
                                                           servers=request["server"], version=request.get("commit_id"), 
                                                           task_id=uuid.uuid4().hex,branch=request.get("branch"),
                                                           tag=request.get("tag"))
                if task:
                    run = DeployRunner(apps_id=self.project.id,task=task,ws=self)
                    run.deploy()
                else:
                    self.disconnect(1000) 
            else:
                self.send(json.dumps({"progress":"summary","status":"error","msg":"您没有权限操作此项"}))
            self.clean_jobs()
            self.send(json.dumps({"progress":"summary","status":"done","msg":"部署完成"}))   
        else:
            self.send(json.dumps({"progress":"summary","status":"error","msg":"{user}正在部署项目".format(user=str(DsRedis.OpsProject.get(redisKey=self.project.project_uuid+"-locked").decode("utf-8")))}))        
            self.disconnect(1000) 
    
    
    def run_rollback(self,request):
        task = self.get_task(request.get("task_ids"))
        if task:
            DsRedis.OpsProject.set(redisKey=self.project.project_uuid+"-locked",value=self.scope["user"].username)  
            if self.check_role(request, self.project):
                rb_task = AppsManage.create_app_deploy_record(self, project=self.project, 
                                                              username=self.scope["user"].username, 
                                                              servers=ast.literal_eval(task.servers),
                                                              version=task.commit_id,package=task.package, 
                                                              task_id=uuid.uuid4().hex,branch=task.branch,
                                                              type="rollback",tag=task.tag)
                if rb_task:
                    run = DeployRunner(task=rb_task,ws=self)
                    run.rollback(task.package)
                else:
                    self.disconnect(1000) 
                self.clean_jobs()
            self.send(json.dumps({"progress":"summary","status":"done","msg":"回滚完成"}))             
        else:
            self.send(json.dumps({"progress":"summary","status":"error","msg":"任务不存在"})) 
            self.disconnect(1000) 
        self.clean_jobs()        
    
    def clean_jobs(self):
        DsRedis.OpsProject.delete(redisKey=self.project.project_uuid+"-locked")
    
    def disconnect(self, close_code):
        self.clean_jobs()
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()