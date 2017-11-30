#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from OpsManage.models import (Log_Ansible_Model,Ansible_CallBack_Model_Result,
                              Global_Config,Ansible_CallBack_PlayBook_Result,
                              Log_Ansible_Playbook)

class AnsibleSaveResult(object): 
    class Model(object): 
        @staticmethod
        def insert(logId,content):
            try:
                config = Global_Config.objects.get(id=1)
                if config.ansible_model == 1:
                    return Ansible_CallBack_Model_Result.objects.create(
                                              logId= logId,
                                              content = content
                                              )
            except Exception,e:
                return False
            
    class PlayBook(object):
        @staticmethod
        def insert(logId,content):
            try:
                config = Global_Config.objects.get(id=1)
                if config.ansible_playbook == 1:
                    return Ansible_CallBack_PlayBook_Result.objects.create(
                                              logId= logId,
                                              content = content
                                              )
            except Exception,e:
                return False    
                
class AnsibleRecord(object):
    class Model(object):
        @staticmethod
        def insert(user,ans_model,ans_server,ans_args=None):
            try:
                config = Global_Config.objects.get(id=1)
                if config.ansible_model == 1:
                    return Log_Ansible_Model.objects.create(
                                              ans_user = user,
                                              ans_server = ans_server,
                                              ans_args = ans_args,
                                              ans_model = ans_model,
                                              )
            except Exception,e:
                return False
            
    class PlayBook(object):
        @staticmethod
        def insert(user,ans_id,ans_name,ans_content,ans_server=None):
            try:
                config = Global_Config.objects.get(id=1)
                if config.ansible_playbook == 1:
                    return Log_Ansible_Playbook.objects.create(
                                              ans_user = user,
                                              ans_server = ans_server,
                                              ans_name = ans_name,
                                              ans_id = ans_id,
                                              ans_content = ans_content,
                                              )
            except Exception, ex:
                print ex
                return False        