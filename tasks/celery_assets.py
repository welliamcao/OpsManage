#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import time
from celery import task
from utils import base
from asset.models import Log_Assets,Assets
from django.contrib.auth.models import User


@task  
def recordAssets(user,content,type,id=None):
    try:
        logs = Log_Assets.objects.create(
                                  assets_id = id,
                                  assets_user = user,
                                  assets_content = content,
                                  assets_type = type
                                  )
        return logs.id
    except Exception as ex:
        return False
    

@task
def debug_task():
    print(time.time())
    return time.time()    
