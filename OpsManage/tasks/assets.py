#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from OpsManage.models import Log_Assets,Global_Config



@task  
def recordAssets(user,content,type,id=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.assets == 1:
            logs = Log_Assets.objects.create(
                                      assets_id = id,
                                      assets_user = user,
                                      assets_content = content,
                                      assets_type = type
                                      )
        return logs.id
    except Exception,e:
        return False