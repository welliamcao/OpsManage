#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json
from celery import task
from utils import base
from project.models import Log_Project_Config
from config.models import Global_Config,Email_Config
from django.contrib.auth.models import User
from channels import Group as CGroups

@task  
def recordProject(project_user,project_id,project_name,project_content,project_branch=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.project == 1:
            Log_Project_Config.objects.create(
                                      project_id = project_id,
                                      project_user = project_user,
                                      project_name = project_name,
                                      project_content = project_content,
                                      project_branch = project_branch
                                      )
        return True
    except Exception as ex:
        print(ex)
        return False