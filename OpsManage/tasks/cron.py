#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from OpsManage.models import Global_Config,Log_Cron_Config


@task  
def recordCron(cron_user,cron_id,cron_name,cron_content,cron_server=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.cron == 1:
            Log_Cron_Config.objects.create(
                                      cron_id = cron_id,
                                      cron_user = cron_user,
                                      cron_name = cron_name,
                                      cron_content = cron_content,
                                      cron_server = cron_server
                                      )
        return True
    except Exception,e:
        print e
        return False