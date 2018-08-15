#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import os,json
from celery import task
from OpsManage.models import (Ansible_Script,Ansible_Playbook,Server_Assets,
                              Ansible_Playbook_Number)
from OpsManage.data.DsMySQL import AnsibleRecord
from OpsManage.utils.ansible_api_v2 import ANSRunner
from dao.assets import AssetsSource


    
    
    
@task  
def AnsibleScripts(**kw):
    logId = None
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
                    sList = json.loads(script.script_server)
                except Exception, ex:
                    return ex           
            if kw.has_key('logs'):
                logId = AnsibleRecord.Model.insert(user='celery',ans_model='script',ans_server=','.join(sList),ans_args=filePath)
            sList, resource = AssetsSource().queryAssetsByIp(ipList=sList)        
            ANS = ANSRunner(resource,redisKey=None,logId=logId)
            ANS.run_model(host_list=sList,module_name='script',module_args="{filePath} {args}".format(filePath=filePath,args=script.script_args))
            return ANS.get_model_result()
    except Exception,e:
        print e
        return False
    
    
@task  
def AnsiblePlayBook(**kw):
    logId = None
    try:
        if kw.has_key('playbook_id'):
            playbook = Ansible_Playbook.objects.get(id=kw.get('playbook_id'))
            filePath = os.getcwd() + '/upload/' + str(playbook.playbook_file)
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
            sList, resource = AssetsSource().queryAssetsByIp(ipList=sList)       
            ANS = ANSRunner(resource,redisKey=None,logId=logId)
            ANS.run_playbook(host_list=sList, playbook_path=filePath,extra_vars=playbook.playbook_vars)
            return ANS.get_playbook_result()
    except Exception,e:
        print e
        return False       