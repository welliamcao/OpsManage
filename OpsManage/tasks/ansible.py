#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import os
from celery import task
from OpsManage.models import (Log_Ansible_Model,Log_Ansible_Playbook,Global_Config,
                              Ansible_Script,Ansible_Playbook,Server_Assets,
                              Ansible_Playbook_Number)
from OpsManage.data.DsMySQL import AnsibleRecord
from OpsManage.utils.ansible_api_v2 import ANSRunner



    
    
    
@task  
def AnsibleScripts(**kw):
    logId = None
    resource = []
    try:
        if kw.has_key('scripts_id'):
            script = Ansible_Script.objects.get(id=kw.get('scripts_id'))
            filePath = os.getcwd()  + str(script.script_file)
            if kw.has_key('hosts'):
                try:
                    sList = list(kw.get('hosts'))
                except Exception, ex:
                    return ex
            else:
                try:
                    sList = list(script.script_server)
                except Exception, ex:
                    return ex           
            if kw.has_key('logs'):
                logId = AnsibleRecord.Model.insert(user='celery',ans_model='script',ans_server=','.join(sList),ans_args=filePath)
            for sip in sList:
                try:
                    server_assets = Server_Assets.objects.get(ip=sip)
                except Exception, ex:
                    continue
                if server_assets.keyfile == 1:resource.append({"hostname": server_assets.ip, "port": int(server_assets.port)})
                else:resource.append({"hostname": server_assets.ip, "port": int(server_assets.port),"username": server_assets.username,"password": server_assets.passwd})         
            ANS = ANSRunner(resource,redisKey=None,logId=logId)
            ANS.run_model(host_list=sList,module_name='script',module_args=filePath)
            return ANS.get_model_result()
    except Exception,e:
        print e
        return False
    
    
@task  
def AnsiblePlayBook(**kw):
    logId = None
    resource = []
    try:
        if kw.has_key('playbook_id'):
            playbook = Ansible_Playbook.objects.get(id=kw.get('playbook_id'))
            filePath = os.getcwd()  + str(playbook.playbook_file)
            if kw.has_key('hosts'):
                try:
                    sList = list(kw.get('hosts'))
                except Exception, ex:
                    return ex
            else:
                try:
                    numberList = Ansible_Playbook_Number.objects.filter(playbook=playbook)
                    if numberList:sList = [ s.playbook_server for s in numberList ]
                except Exception, ex:
                    return ex           
            if kw.has_key('logs'):
                logId = AnsibleRecord.PlayBook.insert(user='celery',ans_id=playbook.id,ans_name=playbook.playbook_name,
                                            ans_content=u"执行Ansible剧本",ans_server=','.join(sList)) 
            for sip in sList:
                try:
                    server_assets = Server_Assets.objects.get(ip=sip)
                except Exception, ex:
                    continue
                if server_assets.keyfile == 1:resource.append({"hostname": server_assets.ip, "port": int(server_assets.port)})
                else:resource.append({"hostname": server_assets.ip, "port": int(server_assets.port),"username": server_assets.username,"password": server_assets.passwd})         
            ANS = ANSRunner(resource,redisKey=None,logId=logId)
            ANS.run_playbook(host_list=sList, playbook_path=filePath)
            return ANS.get_playbook_result()
    except Exception,e:
        print e
        return False    
    
@task  
def recordAnsibleModel(user,ans_model,ans_server,uuid,ans_args=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.ansible_model == 1:
            Log_Ansible_Model.objects.create(
                                      ans_user = user,
                                      ans_server = ans_server,
                                      ans_args = ans_args,
                                      ans_model = ans_model,
                                      ans_uuid = uuid
                                      )
            return True
    except Exception,e:
        return False
    
@task  
def recordAnsiblePlaybook(user,ans_id,ans_name,ans_content,uuid=None,ans_server=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.ansible_playbook == 1:
            Log_Ansible_Playbook.objects.create(
                                      ans_user = user,
                                      ans_server = ans_server,
                                      ans_name = ans_name,
                                      ans_id = ans_id,
                                      ans_content = ans_content,
                                      ans_uuid = uuid
                                      )
        return True
    except Exception,e:
        print e
        return False    