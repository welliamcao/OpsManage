#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import shared_task
from databases.models import SQL_Execute_Histroy
from django.contrib.auth.models import User


@shared_task
def record_exec_sql(exe_user,exe_db,exe_sql,exe_time,exec_status=None,exe_result=None):
    try:
        SQL_Execute_Histroy.objects.create(
                                  exe_user = exe_user,
                                  exe_db = exe_db,
                                  exe_sql = exe_sql,
                                  exec_status = exec_status,
                                  exe_result = exe_result,
                                  exe_time = exe_time
                                  )
        return True
    except Exception as ex:
        print (ex)
        return False 
