#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import os,json
from celery import task
from dao.dispos import DeployRecord
from utils.ansible.runner import ANSRunner
from dao.assets import AssetsAnsible 
from deploy.models import Deploy_Script,Deploy_Playbook
  
    
@task  
def AnsibleScripts(**kw):
    logId = None
    try:
        if 'scripts_id' in kw.keys():
            script = Deploy_Script.objects.get(id=kw.get('scripts_id'))
            filePath = os.getcwd()  + str(script.script_file)    
            sList, resource = AssetsAnsible().allowcator(script.script_type, script.to_celery())  
            if 'logs' in kw.keys():
                logId = DeployRecord.Model.insert(user='celery',ans_model='script',ans_server=','.join(sList),ans_args=filePath)               
            ANS = ANSRunner(resource,background=logId)
            ANS.run_model(host_list=sList,module_name='script',module_args="{filePath} {args}".format(filePath=filePath,args=script.script_args))
            return json.loads(ANS.get_model_result())
    except Exception as ex:
        print(ex)
        return {"status":"failed","msg":str(ex)} 
    
    
@task  
def AnsiblePlayBook(**kw):
    logId = None
    try:
        if 'playbook_id' in kw.keys():
            playbook = Deploy_Playbook.objects.get(id=kw.get('playbook_id'))
            filePath = os.getcwd()  + str(playbook.playbook_file)  
            sList, resource = AssetsAnsible().allowcator(playbook.playbook_type, playbook.to_celery())       
            if 'logs' in kw.keys():
                logId = DeployRecord.PlayBook.insert(user='celery',ans_id=playbook.id,ans_name=playbook.playbook_name,ans_content=u"执行Ansible剧本",ans_server=','.join(sList))                  
            ANS = ANSRunner(resource,background=logId)
            ANS.run_playbook(host_list=sList, playbook_path=filePath)
            return json.loads(ANS.get_playbook_result())
    except Exception as ex:
        print(ex)
        return {"status":"failed","msg":str(ex)}       