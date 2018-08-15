#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import json,re,csv,os
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User,Group
from django.db.models import Q 
from django.contrib.auth.decorators import login_required
from OpsManage.models import (DataBase_Server_Config,Inception_Server_Config,
                              Custom_High_Risk_SQL,SQL_Audit_Control,
                              Service_Assets,Server_Assets,SQL_Execute_Histroy,
                              Project_Assets)
from orders.models import Order_System,SQL_Audit_Order,SQL_Order_Execute_Result
from OpsManage.tasks.sql import sendOrderNotice,recordSQL
from django.contrib.auth.decorators import permission_required
from OpsManage.utils.inception import Inception
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from OpsManage.data.base import MySQLPool
from OpsManage.utils.binlog2sql import Binlog2sql
from OpsManage.utils import base,mysql
from django.http import StreamingHttpResponse,HttpResponse
from OpsManage.utils.logger import logger

@login_required()
@permission_required('OpsManage.can_add_database_server_config',login_url='/noperm/')
def db_config(request):
    if request.method == "GET":
        groupList = Group.objects.all()
        sqlList = Custom_High_Risk_SQL.objects.all()
        dataBaseList = DataBase_Server_Config.objects.all()
        serviceList = Service_Assets.objects.all()
        serList = Server_Assets.objects.all()
        projectList = Project_Assets.objects.all()
        try:
            config = SQL_Audit_Control.objects.get(id=1)
            gList = json.loads(config.audit_group)
            audit_group = []
            for g in gList:
                audit_group.append(int(g))
            for g in groupList:
                if g.id in audit_group:g.count = 1
        except Exception,ex:
            logger.warn(msg="获取SQL审核配置信息失败: {ex}".format(ex=str(ex)))
            config = None
        try:
            incept = Inception_Server_Config.objects.get(id=1)
        except Exception, ex:
            logger.warn(msg="获取Inception服务器信息失败: {ex}".format(ex=str(ex)))
            incept = None
        return render(request,'database/db_config.html',{"user":request.user,"incept":incept,
                                                        "dataBaseList":dataBaseList,"sqlList":sqlList,
                                                        "config":config,"groupList":groupList,
                                                        "serviceList":serviceList,"serList":serList,
                                                        "projectList":projectList}
                      )
                
@login_required()
@permission_required('orders.can_read_sql_audit_order',login_url='/noperm/')
def db_sqlorder_run(request,id):
    try:
        if request.user.is_superuser:order = Order_System.objects.get(id=id)
        else:order = Order_System.objects.filter(Q(order_user=request.user.id,id=id) | Q(order_executor=request.user.id,id=id))[0]
        incept = Inception_Server_Config.objects.get(id=1)       
        if request.user.id != order.order_executor:order.prem = 0
        else:order.prem = 1
    except Exception,ex:
        logger.error(msg="执行SQL[{id}]错误: {ex}".format(id=id,ex=str(ex)))
        return render(request,'database/db_sqlorder_run.html',{"user":request.user,"errinfo":"工单不存在，或者您没有权限处理这个工单"})
    try:
        inceptRbt = Inception(
                   host=incept.db_backup_host,
                   name=order.sql_audit_order.order_db.db_name,
                   user=order.sql_audit_order.order_db.db_user,
                   passwd=order.sql_audit_order.order_db.db_passwd,
                   port=order.sql_audit_order.order_db.db_port
                   )  
    except Exception,ex:
        return render(request,'database/db_sqlorder_run.html',{"user":request.user,"errinfo":"Inception配置错误"})
    if request.method == "GET":
        oscStatus = None
        sqlResultList = []
        rollBackSql = []
        order.order_user = User.objects.get(id=order.order_user).username
        order.order_executor = User.objects.get(id=order.order_executor).username  
        try:
            order.sql_audit_order.order_db.db_service = Service_Assets.objects.get(id=order.sql_audit_order.order_db.db_service)
        except Exception, ex:
            order.sql_audit_order.order_db.db_service = '未知'
        if order.order_status in [5,6,9] and order.sql_audit_order.order_type=='online':   
            sqlResultList = SQL_Order_Execute_Result.objects.filter(order=order.sql_audit_order)
            for ds in sqlResultList:
                if ds.backup_db.find('None') == -1:
                    result = inceptRbt.getRollBackTable(
                                                   host=incept.db_backup_host, user=incept.db_backup_user, 
                                                   passwd=incept.db_backup_passwd, dbName=ds.backup_db, 
                                                   port=incept.db_backup_port, sequence=str(ds.sequence).replace('\'','')
                                                   )
                    if len(ds.sqlsha) > 0:oscStatus = inceptRbt.getOscStatus(sqlSHA1=ds.sqlsha)
                    if result.get('status') == 'success' and result.get('data'):
                        tableName = result.get('data')[0]
                        rbkSql = inceptRbt.getRollBackSQL(
                                                       host=incept.db_backup_host, user=incept.db_backup_user, 
                                                       passwd=incept.db_backup_passwd, dbName=ds.backup_db, 
                                                       port=incept.db_backup_port, tableName=tableName,
                                                       sequence=str(ds.sequence).replace('\'',''),
                                                       )
                    else:
                        rollBackSql = ["Ops！数据库服务器 - {host} 可能未开启binlog或者未开启备份功能，获取回滚SQL失败。".format(host=order.sql_audit_order.order_db.db_host,dbname=order.sql_audit_order.order_db.db_name)]
                        return render(request,'database/db_sqlorder_run.html',{"user":request.user,"order":order,"sqlResultList":sqlResultList,"rollBackSql":rollBackSql,"rbkSql":0,"oscStatus":oscStatus})  
                    if rbkSql.get('status') == 'success' and rbkSql.get('data'): 
                        for sql in rbkSql.get('data'):
                            rollBackSql.append(sql[0])  
        elif  order.sql_audit_order.order_type=='file':
            filePath = os.getcwd() + '/upload/' + str(order.sql_audit_order.order_file)
            with open(filePath, 'r') as f:
                order.sql_audit_order.order_sql = f.read()              
        return render(request,'database/db_sqlorder_run.html',{"user":request.user,"order":order,"sqlResultList":sqlResultList,"rollBackSql":rollBackSql,"oscStatus":oscStatus}) 
    
    elif request.method == "POST":
        if request.POST.get('type') == 'exec' and order.order_status == 8 and order.prem == 1:
            try:
                count = SQL_Order_Execute_Result.objects.filter(order=order.sql_audit_order).count() 
                if count > 0:return JsonResponse({'msg':"该SQL已经被执行过，请勿重复执行","code":500,'data':[]})
            except Exception,ex:
                logger.warn(msg="执行SQL[{id}]错误: {ex}".format(id=id,ex=str(ex)))
            if  order.sql_audit_order.order_type == 'online':          
                try:
                    config = SQL_Audit_Control.objects.get(id=1)
                    incept = Inception(
                                       host=order.sql_audit_order.order_db.db_host,
                                       name=order.sql_audit_order.order_db.db_name,
                                       user=order.sql_audit_order.order_db.db_user,
                                       passwd=order.sql_audit_order.order_db.db_passwd,
                                       port=order.sql_audit_order.order_db.db_port
                                       )
                    if config.t_backup_sql == 0 and order.sql_audit_order.order_db.db_env == 'test':action = '--disable-remote-backup;'
                    elif config.p_backup_sql == 0 and order.sql_audit_order.order_db.db_env == 'prod':action = '--disable-remote-backup;'
                    else:action = None
                    result = incept.execSql(order.sql_audit_order.order_sql,action)
                    if result.get('status') == 'success':
                        count = 0
                        sList = []
                        for ds in result.get('data'):
                            try:                            
                                SQL_Order_Execute_Result.objects.create(
                                                                        order = order.sql_audit_order,
                                                                        errlevel = ds.get('errlevel'),
                                                                        stage = ds.get('stage'),
                                                                        stagestatus = ds.get('stagestatus'),
                                                                        errormessage = ds.get('errmsg'),
                                                                        sqltext =  ds.get('sql'),
                                                                        affectrow = ds.get('affected_rows'),
                                                                        sequence = ds.get('sequence'),
                                                                        backup_db = ds.get('backup_dbname'),
                                                                        execute_time = ds.get('execute_time'),
                                                                        sqlsha = ds.get('sqlsha1'),
                                                                        )
                            except Exception, ex:
                                logger.error(msg="记录SQL错误: {ex}".format(ex=str(ex)))
                            if ds.get('errlevel') > 0 and ds.get('errmsg'):count = count + 1
                            sList.append({'sql':ds.get('sql'),'row':ds.get('affected_rows'),'errmsg':ds.get('errmsg')})
                        if count > 0:
                            order.order_status = 9
                            order.save()      
                            sendOrderNotice.delay(order.id,mask='【执行失败】')                   
                            return JsonResponse({'msg':"执行失败，请检查SQL语句","code":500,'data':sList})
                        else:
                            order.order_status = 5
                            order.save()
                            sendOrderNotice.delay(order.id,mask='【已执行】') 
                            return JsonResponse({'msg':"SQL执行成功","code":200,'data':sList})
                    else:
                        return JsonResponse({'msg':result.get('errinfo'),"code":500,'data':[]}) 
                except Exception, ex:
                    logger.error(msg="执行SQL[{id}]错误: {ex}".format(id=id,ex=str(ex)))
                    return JsonResponse({'msg':str(ex),"code":200,'data':[]})  
            elif order.sql_audit_order.order_type == 'file':
                filePath = os.getcwd() + '/upload/' + str(order.sql_audit_order.order_file)
                rc,rs = mysql.loads(    
                                    host=order.sql_audit_order.order_db.db_host,
                                    dbname=order.sql_audit_order.order_db.db_name,
                                    user=order.sql_audit_order.order_db.db_user,
                                    passwd=order.sql_audit_order.order_db.db_passwd,
                                    port=order.sql_audit_order.order_db.db_port,
                                    sql=filePath
                                    )
                if rc == 0:
                    order.order_status = 8
                    order.save()                     
                    sendOrderNotice.delay(order.id,mask='【已执行】')
                    return JsonResponse({'msg':"SQL执行成功","code":200,'data':rs}) 
                else:
                    order.order_status = 9
                    order.save()                     
                    sendOrderNotice.delay(order.id,mask='【已失败】')
                    return JsonResponse({'msg':"SQL执行失败：{rs}".format(rs=str(rs)),"code":500,'data':[]})   
            
        elif  request.POST.get('type') == 'rollback' and order.order_status == 5 and order.prem == 1: 
            rollBackSql = []  
            sqlResultList = SQL_Order_Execute_Result.objects.filter(order=order.sql_audit_order)
            for ds in sqlResultList:
                if ds.backup_db.find('None') == -1:
                    result = inceptRbt.getRollBackTable(
                                                   host=incept.db_backup_host, user=incept.db_backup_user, 
                                                   passwd=incept.db_backup_passwd, dbName=ds.backup_db, 
                                                   port=incept.db_backup_port, sequence=str(ds.sequence).replace('\'','')
                                                   )
                    if result.get('status') == 'success':
                        tableName = result.get('data')[0]
                        rbkSql = inceptRbt.getRollBackSQL(
                                                       host=incept.db_backup_host, user=incept.db_backup_user, 
                                                       passwd=incept.db_backup_passwd, dbName=ds.backup_db, 
                                                       port=incept.db_backup_port, tableName=tableName,
                                                       sequence=str(ds.sequence).replace('\'',''),
                                                       ) 
                    if rbkSql.get('status') == 'success': 
                        for sql in rbkSql.get('data'):
                            rollBackSql.append(sql[0])                         
            if rollBackSql:
                rbkSql = Inception(
                                   host=order.sql_audit_order.order_db.db_host,
                                   name=order.sql_audit_order.order_db.db_name,
                                   user=order.sql_audit_order.order_db.db_user,
                                   passwd=order.sql_audit_order.order_db.db_passwd,
                                   port=order.sql_audit_order.order_db.db_port                                   
                                   )
                for sql in rollBackSql:
                    result = rbkSql.rollback(sql)
                    if result.get('status') == 'error':#回滚时如果其中一条出现错误就停止回滚 
                        return JsonResponse({'msg':"SQL回滚失败：" + result.get('errinfo'),"code":500,'data':[]})
                #回滚语句如果全部执行成功则修改状态
                order.order_status = 6
                order.save()         
                sendOrderNotice.delay(order.id,mask='【已回滚】')                     
                return JsonResponse({'msg':"SQL回滚成功","code":200,'data':[]})           
            else:    
                return JsonResponse({'msg':"没有需要执行的回滚SQL语句","code":500,'data':[]})    
        else:
            return JsonResponse({'msg':"SQL已经被执行","code":500,'data':[]})    
        
        
@login_required()
@permission_required('OpsManage.can_change_sql_audit_control',login_url='/noperm/')
def db_sql_control(request):
    if request.method == "POST":
        try:
            count = SQL_Audit_Control.objects.filter(id=1).count()
        except:
            count = 0
        gList = []
        for g in request.POST.getlist('audit_group',[]):
            gList.append(g)
        if count > 0:
            try:
                SQL_Audit_Control.objects.filter(id=1).update(
                                                            t_auto_audit = request.POST.get('t_auto_audit'),
                                                            t_backup_sql = request.POST.get('t_backup_sql'), 
                                                            t_email = request.POST.get('t_email'), 
                                                            p_auto_audit = request.POST.get('p_auto_audit'), 
                                                            p_backup_sql  = request.POST.get('p_backup_sql'), 
                                                            p_email = request.POST.get('p_email'),   
                                                            audit_group = json.dumps(gList),                                                                  
                                                            )
                return JsonResponse({'msg':"修改成功","code":200,'data':[]})
            except Exception, ex:
                logger.error(msg="更新数据表[opsmanage_sql_audit_control]错误: {ex}".format(ex=str(ex)))
                return JsonResponse({'msg':"修改失败："+str(ex),"code":500,'data':[]}) 
        else:
            try:
                SQL_Audit_Control.objects.create(
                                                t_auto_audit = request.POST.get('t_auto_audit'),
                                                t_backup_sql = request.POST.get('t_backup_sql'), 
                                                t_email = request.POST.get('t_email'), 
                                                p_auto_audit = request.POST.get('p_auto_audit'), 
                                                p_backup_sql  = request.POST.get('p_backup_sql'), 
                                                p_email = request.POST.get('p_email'), 
                                                audit_group = json.dumps(gList),  
                                                )   
                return JsonResponse({'msg':"修改成功","code":200,'data':[]})
            except Exception,ex:
                logger.error(msg="写入数据表[opsmanage_sql_audit_control]错误: {ex}".format(ex=str(ex)))
                return JsonResponse({'msg':"修改失败: "+str(ex),"code":500,'data':[]}) 
            
@login_required()
@permission_required('orders.can_read_sql_audit_order',login_url='/noperm/')
def db_sqlorder_osc(request,id):
    if request.method == "POST" and request.POST.get('model') == 'query':
        order = SQL_Audit_Order.objects.get(id=id)
        inceptRbt = Inception()           
        sqlResultList = SQL_Order_Execute_Result.objects.filter(order=order)
        for ds in sqlResultList:
            if ds.backup_db.find('None') == -1:
                if ds.sqlsha:
                    result = inceptRbt.getOscStatus(sqlSHA1=ds.sqlsha) 
                    if result.get('status') == 'success':
                        return JsonResponse({"code":200,"data":result.get('data')})
                    else:return JsonResponse({"code":500,"data":result.get('data')}) 
    elif request.method == "POST" and request.POST.get('model') == 'stop':
        order = SQL_Audit_Order.objects.get(id=id)
        inceptRbt = Inception()           
        sqlResultList = SQL_Order_Execute_Result.objects.filter(order=order)
        for ds in sqlResultList:
            if ds.backup_db.find('None') == -1:
                if ds.sqlsha:
                    result = inceptRbt.stopOsc(sqlSHA1=ds.sqlsha) 
                    if result.get('status') == 'success':
                        return JsonResponse({"code":200,"data":result.get('data')})
                    else:
                        return JsonResponse({"code":500,"data":result.get('errinfo')})
       
 
        
@login_required()
@permission_required('OpsManage.can_add_database_server_config',login_url='/noperm/')
def db_ops(request): 
    if request.method == "GET":
        dataBaseList = DataBase_Server_Config.objects.all()
        serviceList = Service_Assets.objects.all()
        projectList = Project_Assets.objects.all()
        return render(request,'database/db_ops.html',{"user":request.user,"dataBaseList":dataBaseList,"serviceList":serviceList,"projectList":projectList}) 
    
    elif request.method == "POST" and request.POST.get('model') == 'binlog':#通过获取数据库的binlog版本
        try:
            dbServer = DataBase_Server_Config.objects.get(id=request.POST.get('ops_db'))
        except:
            dbServer = None
        if dbServer:
            mysql = MySQLPool(host=dbServer.db_host,port=dbServer.db_port,user=dbServer.db_user,passwd=dbServer.db_passwd,dbName=dbServer.db_name)
            result = mysql.queryAll(sql='show binary logs;')
            binLogList = []
            if isinstance(result,tuple):
                for ds in result[1]:
                    binLogList.append(ds[0]) 
        return JsonResponse({'msg':"数据查询成功","code":200,'data':binLogList,'count':0})  

    elif request.method == "POST" and request.POST.get('model') == 'querydb':#根据业务类型查询数据库
        dataList = []
        dbSerlist = DataBase_Server_Config.objects.filter(db_env=request.POST.get('db_env'),db_service=request.POST.get('db_service'))
        for ds in dbSerlist:
            data = dict()
            data['id'] = ds.id
            data['db_name'] = ds.db_name
            data['db_host'] = ds.db_host
            data['db_mark'] = ds.db_mark
            dataList.append(data)
        return JsonResponse({'msg':"数据查询成功","code":200,'data':dataList})
    
    elif request.method == "POST" and request.POST.get('opsTag') == '1':#通过binlog获取DML
        sqlList = []
        try:
            dbServer = DataBase_Server_Config.objects.get(id=int(request.POST.get('dbId')))
        except Exception, ex:
            sqlList.append(ex)
            dbServer = None
        if dbServer:
            conn_setting = {'host': dbServer.db_host, 'port': dbServer.db_port, 'user': dbServer.db_user, 'passwd': dbServer.db_passwd, 'charset': 'utf8'}
            #flashback=True获取DML回滚语句
            binlog2sql = Binlog2sql(connection_settings=conn_setting,             
                                    back_interval=1.0, only_schemas=dbServer.db_name,
                                    end_file='', end_pos=0, start_pos=4,
                                    flashback=True,only_tables='', 
                                    no_pk=False, only_dml=True,stop_never=False, 
                                    sql_type=['INSERT', 'UPDATE', 'DELETE'], 
                                    start_file=request.POST.get('binlog'), 
                                    start_time=request.POST.get('startime'), 
                                    stop_time=request.POST.get('endtime'),)
            sqlList = binlog2sql.process_binlog()
        return JsonResponse({'msg':"获取binlog数据成功","code":200,'data':sqlList,'tag':1}) 
    elif request.method == "POST" and request.POST.get('opsTag') == '2':#优化建议
        try:
            dbServer = DataBase_Server_Config.objects.get(id=int(request.POST.get('dbId')))
        except Exception, ex:
            dbServer = None   
        if dbServer:    
            #先通过Inception审核语句
            incept = Inception(
                               host=dbServer.db_host,name=dbServer.db_name,
                               user=dbServer.db_user,passwd=dbServer.db_passwd,
                               port=dbServer.db_port
                               )
            result = incept.checkSql(request.POST.get('sql'))
            if result.get('status') == 'success':
                count = 0
                errStr = ''
                for ds in result.get('data'):
                    if ds.get('errlevel') > 0 and ds.get('errmsg'):
                        count = count + 1
                        errStr = errStr +ds.get('errmsg')
                if count > 0:return JsonResponse({'msg':"审核失败，请检查SQL语句","code":500,'data':errStr,'tag':2}) 
            else:
                return JsonResponse({'msg':"Inception审核失败","code":500,'data':result.get('errinfo'),'tag':2})             
            status,result = base.getSQLAdvisor(host=dbServer.db_host, user=dbServer.db_user,
                                               passwd=dbServer.db_passwd, dbname=dbServer.db_name, 
                                               sql=request.POST.get('sql'),port=dbServer.db_port)
            if status == 0:
                return JsonResponse({'msg':"获取SQL优化数据成功","code":200,'data':result,'tag':2}) 
            else:
                return JsonResponse({'msg':"获取SQL优化数据失败","code":500,'data':result,'tag':2}) 
        else:return JsonResponse({'msg':"获取SQL优化数据失败","code":500,'data':[],'tag':2})
        
    elif request.method == "POST" and request.POST.get('opsTag') == '3':#执行DQL
        if re.match(r"^(\s*)?select(\S+)?(.*)", request.POST.get('sql').lower()):            
            try:
                dbServer = DataBase_Server_Config.objects.get(id=int(request.POST.get('dbId')))
            except Exception, ex:
                dbServer = None 
            if dbServer:
                mysql = MySQLPool(host=dbServer.db_host,port=dbServer.db_port,user=dbServer.db_user,passwd=dbServer.db_passwd,dbName=dbServer.db_name)
                result = mysql.queryMany(sql=request.POST.get('sql'),num=1000)
                if isinstance(result,str):
                    recordSQL.delay(exe_user=str(request.user),exe_db=dbServer,exe_sql=request.POST.get('sql'),exec_status=0,exe_result=str) 
                    return JsonResponse({'msg':"数据查询失败","code":500,'data':result,'tag':3})  
            recordSQL.delay(exe_user=str(request.user),exe_db=dbServer,exe_sql=request.POST.get('sql'),exec_status=1,exe_result=None)  
            return JsonResponse({'msg':"数据查询成功","code":200,'data':{"colName":result[2],"dataList":result[1]},'count':result[0],'tag':3})  
        else:return JsonResponse({'msg':"数据查询失败","code":500,'data':"不是DQL类型语句",'tag':3}) 
        
    elif request.method == "POST" and request.POST.get('opsTag') == '4' and request.user.is_superuser:#执行原生SQL         
        try:
            dbServer = DataBase_Server_Config.objects.get(id=int(request.POST.get('dbId')))
        except Exception, ex:
            dbServer = None 
        if dbServer:
            mysql = MySQLPool(host=dbServer.db_host,port=dbServer.db_port,user=dbServer.db_user,passwd=dbServer.db_passwd,dbName=dbServer.db_name)
            result = mysql.execute(sql=request.POST.get('sql'),num=1000)
            if isinstance(result,str):
                recordSQL.delay(exe_user=str(request.user),exe_db=dbServer,exe_sql=request.POST.get('sql'),exec_status=0,exe_result=result) 
                return JsonResponse({'msg':"数据查询失败","code":500,'data':result,'tag':3}) 
            else:
                if result[0] == 0:return JsonResponse({'msg':"数据查询成功","code":200,'data':"SQL执行成功",'tag':3})
            recordSQL.delay(exe_user=str(request.user),exe_db=dbServer,exe_sql=request.POST.get('sql'),exec_status=1,exe_result=None)    
            return JsonResponse({'msg':"数据查询成功","code":200,'data':{"colName":result[2],"dataList":result[1]},'count':result[0],'tag':3}) 
        else:return JsonResponse({'msg':"数据查询失败","code":500,'data':str(ex),'tag':3}) 
    else:return JsonResponse({'msg':"数据操作失败","code":500,'data':"您可能没有权限操作此项目",'tag':3})       
    
    
@login_required()
@permission_required('OpsManage.can_read_sql_execute_histroy',login_url='/noperm/')
def db_sql_logs(request,page):  
    if request.method == "GET":
        allSqlLogsList = SQL_Execute_Histroy.objects.all().order_by('-id')[0:2000]
        paginator = Paginator(allSqlLogsList, 25)          
        try:
            sqlLogsList = paginator.page(page)
        except PageNotAnInteger:
            sqlLogsList = paginator.page(1)
        except EmptyPage:
            sqlLogsList = paginator.page(paginator.num_pages)        
        return render(request,'database/db_logs.html',{"user":request.user,"sqlLogsList":sqlLogsList}) 
    
@login_required()
def db_sql_dumps(request): 
    if request.method == "POST":#执行原生SQL  
        try:
            dbServer = DataBase_Server_Config.objects.get(id=int(request.POST.get('dbId')))
        except Exception, ex:
            dbServer = None 
        if dbServer:
            mysql = MySQLPool(host=dbServer.db_host,port=dbServer.db_port,user=dbServer.db_user,passwd=dbServer.db_passwd,dbName=dbServer.db_name)
            result = mysql.execute(sql=request.POST.get('sql'),num=1000)
            if isinstance(result,str):
                return JsonResponse({'msg':"不支持导出功能","code":500,'data':result,'tag':3}) 
            else:
                if result[0] == 0:return JsonResponse({'msg':"不支持导出功能","code":200,'data':"SQL执行成功",'tag':3})  
            file_name = "query_result.csv"    
            with open(file_name,"w") as csvfile: 
                writer = csv.writer(csvfile,dialect='excel')
                #先写入columns_name
                writer.writerow(result[2])
                #写入多行用writerows
                for ds in result[1]:
                    writer.writerows([list(ds)])               
            response = StreamingHttpResponse(base.file_iterator(file_name))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(file_name=file_name)
            return response                           