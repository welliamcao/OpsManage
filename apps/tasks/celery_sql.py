#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json, os, gzip
from celery import task
from databases.models import (SQL_Execute_History,Database_MySQL_Detail)
from account.models import User_Async_Task, User
from utils.logger import logger
from django.utils import timezone
from utils import base
from libs.notice import Notice
from utils.mysql.binlog2sql import Binlog2sql

@task
def record_exec_sql(exe_user,exe_db,exe_sql,exe_time,
                    exe_effect_row=0,exec_status=None,exe_result=None):
    try:
        exe_db = Database_MySQL_Detail.objects.get(id=exe_db)
    except Exception as ex:
        return {"status":"failed","msg":str(ex)} 
    try:
        SQL_Execute_History.objects.create(
                                  exe_user = exe_user,
                                  exe_db = exe_db,
                                  exe_sql = exe_sql,
                                  exec_status = exec_status,
                                  exe_result = exe_result,
                                  exe_effect_row = exe_effect_row,
                                  exe_time = exe_time
                                  )
        return {"status":"success","msg":None}
    except Exception as ex:
        return {"status":"failed","msg":str(ex)} 
    
    
@task
def export_table(task_id):
    try:
        task = User_Async_Task.objects.get(task_id=task_id)
        task_user = User.objects.get(id=task.user)   
        args = json.loads(task.to_json().get("args"))  
        email =  task_user.email 
    except Exception as ex:
        logger.error("获取任务失败: {ex}".format(ex=str(ex)))
        task.msg = str(ex)
        task.status = 2
        task.etime = timezone.now()
        task.save()        
        return {"status":"failed","msg":str(ex)}

    try:
        exe_db = Database_MySQL_Detail.objects.get(id=task.extra_id)
        db, table, where_claus = exe_db.to_connect(), args.get("value").split("|")[1], args.get("vars") 
        if len(where_claus) == 0:where_claus = None
    except Exception as ex:
        logger.error("获取数据库失败: {ex}".format(ex=str(ex)))
        task.status = 2
        task.msg = str(ex)
        task.etime = timezone.now()
        task.save() 
        return {"status":"failed","msg":str(ex)} 
    
    save_path ,file_name = os.getcwd() + '/upload/tasks/','{task_id}.sql.gz'.format(task_id=task_id)
    backup_file = save_path + file_name    
    
    try:
        task.status = 1  
        code, result = base.mysql_bakcup_tables(db, table, save_path, task_id, where_claus, 3600)  
        if args.get("email"): email = args.get("email")
        if code == 0: 
            message = {
                    "e_content": u"<strong>数据库:</strong> {db}<br><strong>表:</strong> {table}<br><strong>条件:</strong> {where_claus}<br>请注意查收附件".format(db = db.get("db_name"), table = table, where_claus = where_claus),
                    "e_sub":"[OpsManage-数据导出] {subject}".format(subject = task.task_name),
                    "e_to":email,
                    "attachFile":backup_file,
                }            
            rs = Notice(0).send(**message)
            if isinstance(rs, str):
                task.status = 2
                task.msg = str(rs)                
        else:         
            task.status = 2
            task.msg = str(result)
    except Exception as ex:
        task.msg = str(ex)
        task.status = 2       
        logger.error("表数据导出失败: {ex}".format(ex=str(ex))) 
    finally: 
        task.file = 'upload/tasks/' + file_name   
        task.etime = timezone.now()
        task.save()
#         if os.path.exists(backup_file):
#             os.remove(backup_file)   
            
@task
def parse_binlog(task_id, binlog):
    try:
        task = User_Async_Task.objects.get(task_id=task_id)  
    except Exception as ex:
        logger.error("获取任务失败: {ex}".format(ex=str(ex)))     
        return {"status":"failed","msg":str(ex)}

    binlog2sql = Binlog2sql(connection_settings=binlog.get("conn_setting"),             
                            back_interval=1.0, only_schemas=binlog.get("only_schemas"),
                            end_file='', end_pos=0, start_pos=4,
                            flashback=binlog.get("flashback"), only_tables=binlog.get("only_tables"), 
                            no_pk=False, only_dml=True,stop_never=False, 
                            sql_type=['INSERT', 'UPDATE', 'DELETE'], 
                            start_file=binlog.get("start_file"), 
                            start_time=binlog.get("start_time").replace("T"," "), 
                            stop_time=binlog.get("stop_time").replace("T"," "),)

    save_path ,file_name = os.getcwd() + '/upload/tasks/','{task_id}.sql.gz'.format(task_id=task_id)
    backup_file = save_path + file_name
    if not os.path.exists(save_path):
        os.makedirs(save_path)    
          
    try:
        task.status = 1 
        sql_list =  binlog2sql.process_binlog()
        if sql_list:
            with gzip.open(backup_file, 'w') as f:
                for sql in sql_list:
                    sql = sql + '\n'   
                    f.write(sql.encode('utf-8'))  
            task.file = 'upload/tasks/' + file_name
        else:      
            task.msg = "无数据"
            task.status = 2             
    except Exception as ex:
        task.msg = str(ex)
        task.status = 2       
        logger.error("解析binlog失败: {ex}".format(ex=str(ex))) 
    finally:    
        task.etime = timezone.now()
        task.save()             
    