#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import os, json, uuid
from deploy.models import *
from utils.logger import logger 
from django.http import QueryDict
from dao.base import DataHandle
from datetime import datetime,timedelta,date

class DeploySaveResult(object): 
    class Model(object): 
        @staticmethod
        def insert(logId,content):
            try:
                return Deploy_CallBack_Model_Result.objects.create(
                                          logId= logId,
                                          content = content
                                          )
            except Exception as ex:
                logger.error(msg="记录模块执行日志失败:{ex}".format(ex=ex))
                return False
            
    class PlayBook(object):
        @staticmethod
        def insert(logId,content):
            try:
                return Deploy_CallBack_PlayBook_Result.objects.create(
                                          logId= logId,
                                          content = content
                                          )
            except Exception as ex:
                logger.error(msg="记录剧本执行日志失败:{ex}".format(ex=ex))
                return False    
                
class DeployRecord(object):
    class Model(object):
        @staticmethod
        def insert(user,ans_model,ans_server,ans_args=None):
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
            
    class PlayBook(object):
        @staticmethod
        def insert(user,ans_id,ans_name,ans_content,ans_server=None):
            try:
                return Log_Deploy_Playbook.objects.create(
                                          ans_user = user,
                                          ans_server = ans_server,
                                          ans_name = ans_name,
                                          ans_id = ans_id,
                                          ans_content = ans_content,
                                          )
            except Exception as ex:
                logger.error(msg="记录剧本执行日志失败:{ex}".format(ex=ex))
                return False 

       
            
class DeployScript(DataHandle):   
    def __init__(self):
        super(DeployScript,self).__init__()    
            
        
    def script(self,ids):
        try:
            script = Deploy_Script.objects.get(id=ids)
        except Exception as ex:
            return "查询部署脚本{ids}，失败{ex}".format(ids=ids,ex=ex)
        script_file = os.getcwd()  + str(script.script_file)
        if os.path.exists(script_file):
            content = ''
            with open(script_file,"r") as f:
                for line in f.readlines(): 
                    content =  content + line 
            script.script_contents = content  
        return  json.dumps(self.convert_to_dict(script))         
       
    
    def scriptList(self):
        dataList = []
        for ds in Deploy_Script.objects.all():
            dataList.append(ds.to_json())
        return dataList       

        
    def createScript(self,request):
        fileName = '/upload/scripts/script-{ram}'.format(ram=uuid.uuid4().hex[0:8]) 
        filePath = os.getcwd() + fileName
        self.saveScript(content=request.POST.get('script_file'),filePath=filePath)          
        try:
            Deploy_Script.objects.create(
                                          script_name=request.POST.get('script_name'),
                                          script_args=request.POST.get('script_args'),
                                          script_server=json.dumps(request.POST.getlist('server[]')),
                                          script_group=self.change(request.POST.get('group')),
                                          script_tags=self.change(request.POST.get('tags')),
                                          script_file=fileName,
                                          script_user=request.user.id,
                                          script_inventory_groups=self.change(request.POST.get('inventory_groups')),
                                          script_service=self.change(request.POST.get('service')),
                                          script_type=request.POST.get('server_model')
                                          )
        except Exception as ex:
            logger.warn(msg="添加部署脚本失败: {ex}".format(ex=ex))  
            return "添加部署脚本失败: {ex}".format(ex=ex)
        return True  
    
    def updateScript(self,request):
        try:   
            script = Deploy_Script.objects.get(id=QueryDict(request.body).get('script_id'))
        except Exception as ex:
            return "更新部署脚本失败: {ex}".format(ex=ex)
        filePath = os.getcwd() + '/' + str(script.script_file)
        self.saveScript(content=QueryDict(request.body).get('script_file'),filePath=filePath)
        try:
            Deploy_Script.objects.filter(id=script.id).update(
                                          script_server=json.dumps(QueryDict(request.body).getlist('server[]')),
                                          script_group=self.change(QueryDict(request.body).get('group')),
                                          script_tags=self.change(QueryDict(request.body).get('tags')),
                                          script_args=QueryDict(request.body).get('script_args'),
                                          script_user=request.user.id,
                                          script_inventory_groups=self.change(QueryDict(request.body).get('inventory_groups')),
                                          script_service=self.change(QueryDict(request.body).get('service')),
                                          script_type=QueryDict(request.body).get('server_model'),
                                          update_date = datetime.now()
                                          )
        except Exception as ex:
            logger.error(msg="更新脚本失败: {ex}".format(ex=str(ex)))
            return "更新脚本失败: {ex}".format(ex=str(ex))
        return True 
    
    def deleteScript(self,request):
        try:   
            script = Deploy_Script.objects.get(id=QueryDict(request.body).get('script_id'))
            script.delete()
        except Exception as ex:
            return "删除部署脚本失败: {ex}".format(ex=ex)             
        return True 
    
    
class DeployPlaybook(DataHandle):   
    def __init__(self):
        super(DeployPlaybook,self).__init__()    
            
        
    def playbook(self,ids):
        try:
            playbook = Deploy_Playbook.objects.get(id=ids)
        except Exception as ex:
            return "查询部署剧本{ids}，失败{ex}".format(ids=ids,ex=ex)
        playbook_file = os.getcwd()  + str(playbook.playbook_file)
        if os.path.exists(playbook_file):
            content = ''
            with open(playbook_file,"r") as f:
                for line in f.readlines(): 
                    content =  content + line 
            playbook.playbook_contents = content  
        return  json.dumps(self.convert_to_dict(playbook))         
       
    
    def playbookList(self):
        dataList = []
        for ds in Deploy_Playbook.objects.all():
            dataList.append(ds.to_json())
        return dataList
        
    def createPlaybook(self,request):
        fileName = '/upload/playbook/playbook-{ram}'.format(ram=uuid.uuid4().hex[0:8]) 
        filePath = os.getcwd() + fileName
        self.saveScript(content=request.POST.get('playbook_file'),filePath=filePath)          
        try:
            Deploy_Playbook.objects.create(
                                          playbook_name=request.POST.get('playbook_name'),
                                          playbook_vars=request.POST.get('playbook_vars'),
                                          playbook_desc = request.POST.get('playbook_desc'),
                                          playbook_server=json.dumps(request.POST.getlist('server[]')),
                                          playbook_group=self.change(request.POST.get('group')),
                                          playbook_tags=self.change(request.POST.get('tags')),
                                          playbook_file=fileName,
                                          playbook_user=request.user.id,
                                          playbook_inventory_groups=self.change(request.POST.get('inventory_groups')),
                                          playbook_service=self.change(request.POST.get('service')),
                                          playbook_type=request.POST.get('server_model')
                                          )
        except Exception as ex:
            logger.warn(msg="添加部署脚本失败: {ex}".format(ex=ex))  
            return "添加部署脚本失败: {ex}".format(ex=ex)
        return True  
    
    def updatePlaybook(self,request):
        try:   
            playbook = Deploy_Playbook.objects.get(id=QueryDict(request.body).get('playbook_id'))
        except Exception as ex:
            return "更新部署剧本失败: {ex}".format(ex=ex)
        filePath = os.getcwd() + '/' + str(playbook.playbook_file)
        self.saveScript(content=QueryDict(request.body).get('playbook_file'),filePath=filePath)
        try:
            Deploy_Playbook.objects.filter(id=playbook.id).update(
                                          playbook_server=json.dumps(QueryDict(request.body).getlist('server[]')),
                                          playbook_desc = QueryDict(request.body).get('playbook_desc'),
                                          playbook_group=QueryDict(request.body).get('group',0),
                                          playbook_user=request.user.id,
                                          playbook_tags=QueryDict(request.body).get('tags'),
                                          playbook_inventory_groups=self.change(QueryDict(request.body).get('inventory_groups')),
                                          playbook_service=self.change(QueryDict(request.body).get('service')),
                                          playbook_type=QueryDict(request.body).get('server_model'),
                                          playbook_vars=QueryDict(request.body).get('playbook_vars'),
                                          update_date = datetime.now()
                                          )
        except Exception as ex:
            logger.error(msg="更新剧本失败: {ex}".format(ex=str(ex)))
            return "更新剧本失败: {ex}".format(ex=str(ex))
        return True 
    
    def deletePlaybook(self,request):
        try:   
            playbook = Deploy_Playbook.objects.get(id=QueryDict(request.body).get('playbook_id'))
            playbook.delete()
        except Exception as ex:
            return "删除部署剧本失败: {ex}".format(ex=ex)             
        return True                                       