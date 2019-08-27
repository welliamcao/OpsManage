#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json
from celery import task
from utils import base
from databases.models import (SQL_Execute_Histroy)
from orders.models import Order_System
from django.contrib.auth.models import User


@task  
def recordSQL(exe_user,exe_db,exe_sql,exec_status,exe_result=None):
    try:
        SQL_Execute_Histroy.objects.create(
                                  exe_user = exe_user,
                                  exe_db = exe_db,
                                  exe_sql = exe_sql,
                                  exec_status = exec_status,
                                  exe_result = exe_result
                                  )
        return True
    except Exception as ex:
        print (ex)
        return False 