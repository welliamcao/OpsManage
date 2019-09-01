#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from databases.models import (SQL_Execute_Histroy,Database_Detail)

@task
def record_exec_sql(exe_user,exe_db,exe_sql,exe_time,exec_status=None,exe_result=None):
    try:
        exe_db = Database_Detail.objects.get(id=exe_db)
    except Exception as ex:
        return {"status":"failed","msg":str(ex)} 
    try:
        SQL_Execute_Histroy.objects.create(
                                  exe_user = exe_user,
                                  exe_db = exe_db,
                                  exe_sql = exe_sql,
                                  exec_status = exec_status,
                                  exe_result = exe_result,
                                  exe_time = exe_time
                                  )
        return {"status":"success","msg":None}
    except Exception as ex:
        return {"status":"failed","msg":str(ex)} 