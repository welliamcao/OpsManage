#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import random, os, json
from dao.assets import AssetsSource,AssetsBase
from account.models import User
from orders.models import *
from databases.models import Database_MySQL_Detail
from libs.ansible.runner import ANSRunner
from utils import base
from utils.mysql import cmds
from django.http import QueryDict, Http404
from django.core.exceptions import PermissionDenied
from utils.mysql.inception import Inception
from utils.logger import logger
from OpsManage.settings import INCEPTION_CONFIG
from apps.tasks.celery_orders import order_notice

class OrdersCount():
    def __init__(self):
        super(OrdersCount, self).__init__()  
        self.dataList = []
    
    def get_range_day(self,maxNum=31):
        dataList = []
        count = 1
        while count < maxNum:
            dataList.append((base.changeTotimestamp(base.getDaysAgo(count,"%Y-%m-%d"),"%Y-%m-%d")))
            count = count + 1
        return dataList            
        
    def month_orders(self):
        dataList = []
        dateList = self.get_range_day()
        dateList.reverse()
        for startTime in dateList:
            endTime = startTime + 86400
            sql = """SELECT id,IFNULL(count(0),0) as count from opsmanage_order_system WHERE FROM_UNIXTIME(create_time,"%%Y%%m%%d") >= {startTime} and 
                    FROM_UNIXTIME(create_time,"%%Y%%m%%d") < {endTime}""".format(startTime=startTime,endTime=endTime)
            order = Order_System.objects.raw(sql)
            if  order[0].count == 0:dataList.append([startTime*1000,random.randint(1, 100) ])
            else:dataList.append([startTime*1000,order[0].count])       
        return dataList
    
    def get_orders_by_date(self,dateRange,order_type=1):
        dataList = []
        dateRange.reverse()
        for startTime in dateRange:
            endTime = startTime + 86400
            sql = """SELECT id,IFNULL(count(0),0) as count from opsmanage_order_system WHERE FROM_UNIXTIME(create_time,"%%Y%%m%%d") >= {startTime} and 
                    FROM_UNIXTIME(create_time,"%%Y%%m%%d") < {endTime} and order_type={order_type} """.format(startTime=startTime,endTime=endTime,order_type=order_type)
            order = Order_System.objects.raw(sql)
            if  order[0].count == 0:dataList.append(random.randint(1, 100))
            else:dataList.append(order[0].count)       
        return dataList        
    
    def get_orders_by_type(self,order_type=1):
        count = Order_System.objects.filter(order_type=order_type).count()
        if count > 0:return count
        else:return random.randint(1, 100) 
    
    def sql_orders(self):
        return {"all":self.get_orders_by_type(order_type=1),"dataList":self.get_orders_by_date(dateRange=self.get_range_day(),order_type=1)}
    
    def upload_orders(self):
        return {"all":self.get_orders_by_type(order_type=2),"dataList":self.get_orders_by_date(dateRange=self.get_range_day(),order_type=2)}
    
    def download_orders(self):
        return {"all":self.get_orders_by_type(order_type=3),"dataList":self.get_orders_by_date(dateRange=self.get_range_day(),order_type=3)}      
    
class OrderBase(AssetsBase):
    def __init__(self):
        super(OrderBase, self).__init__() 
        
    def get_db(self,order):
        try:
            db = order.sql_audit_order.order_db
            config = db.db_server.to_connect()
            config["db_name"] = db.db_name            
            return  db, config     
        except Exception as ex:
            logger.warn(msg="获取数据库信息失败: {ex}".format(ex=ex))
            raise Http404     
    
    def inception(self,config):
        return Inception(
                        host=config.get("ip"),name=config.get('db_name'),
                        user=config.get("db_user"),passwd=config.get("db_passwd"),
                        port=config.get("db_port")
                        )      

    def get_order(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        
        elif request.method == 'POST':cid = request.POST.get('id')
        
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        
        try:
            order = Order_System.objects.get(id=cid)
            return order
        except Exception as ex:
            logger.warn(msg="获取工单信息失败: {ex}".format(ex=ex))
            raise Http404       
    
    
    def check_perms(self,request):
        order = self.get_order(request)
        
        if request.user.is_superuser:
            return order
              
        if request.user.id == order.order_user:
            return order  
        
        raise PermissionDenied()

    def record_order_operation(self,order, audit_status, execute_status, user, operation_info=None):
        try:
            OrderLog.objects.create(
                                   order=order,
                                   audit_status = audit_status,
                                   execute_status = execute_status,
                                   operator = user.id,
                                   operation_info = operation_info,
                                ) 
        except Exception as ex:
            logger.error(msg="工单记录审核失败: {ex}".format(ex=str(ex)))
            return str(ex)
        

        if execute_status !=1 and audit_status==2:#创建工单时发送通知
            order_notice.apply_async((order,), queue='default', retry=True)
            
    
    def update_order_progress(self, data):
        if data.get("order_audit_status") == "1":      
            data["order_audit_status"] = 1
            data["order_execute_status"] = 4
        
        elif data.get("order_audit_status") == "2":    
            data["order_audit_status"] = 2
            data["order_execute_status"] = 0                    
        
        elif data.get("order_audit_status") == "3":
            data["order_audit_status"] = 3
            data["order_execute_status"] = 1
       
        return data        
    
    def get_incept_sql_result(self,order):
        return SQL_Order_Execute_Result.objects.filter(order=order.sql_audit_order)
    
    def order_detail(self, order):
        
        data = order.to_json()
        
        data["detail"] = {}
        
        if hasattr(order,'sql_audit_order'):   
            data["detail"] = order.sql_audit_order.to_json()
            if order.order_execute_status in [2,3,4] and order.sql_audit_order.order_type == 'online':
                data["detail"]["result"] = []
                
                for ds in self.get_incept_sql_result(order):
                    data["detail"]["result"].append(ds.to_json())
                    
                data["detail"]["backup_sql"] = self.get_rollback_sqls(order, order.sql_audit_order.order_db.db_server.to_connect())
                
        elif  hasattr(order,'fileupload_audit_order'):
            data["detail"] = order.fileupload_audit_order.to_json()
            data["detail"]["files"] = [ ds.to_json() for ds in order.fileupload_audit_order.uploadfiles.all() ]
            data["detail"]["server"] = [ ds.get('ip') for ds in self.idsList(json.loads(order.fileupload_audit_order.dest_server)) ]     

        elif  hasattr(order,'filedownload_audit_order'):             
            data["detail"] = order.filedownload_audit_order.to_json()
            data["detail"]["server"] = [ ds.get('ip') for ds in self.idsList(json.loads(order.filedownload_audit_order.dest_server)) ]                 
        
        elif  hasattr(order,'service_audit_order'):             
            data["detail"]= order.service_audit_order.to_json()
            
        return  data        
   
    
    def get_rollback_sqls(self, order, config):
        rollBackSql = {}
        rollBackSql["sql"] = []
        rollBackSql["osc"] = False
        if order.order_execute_status in [2,4] and order.sql_audit_order.order_type == 'online' and order.sql_audit_order.sql_backup == 1:
            incept = self.inception(config)
            for ds in self.get_incept_sql_result(order):                
                if ds.backup_db.find('None') == -1:
                    result = incept.getRollBackTable(
                                                   dbName=ds.backup_db, 
                                                   sequence=str(ds.sequence).replace('\'','')
                                                   )
                    if len(ds.sqlsha) > 0:rollBackSql["osc"] = True
                    if result.get('status') == 'success' and result.get('data'):
                        tableName = result.get('data')[0]
                        rbkSql = incept.getRollBackSQL(
                                                       dbName=ds.backup_db,tableName=tableName,
                                                       sequence=str(ds.sequence).replace('\'',''),
                                                       )  
                    if rbkSql.get('status') == 'success' and rbkSql.get('data'): 
                        for sql in rbkSql.get('data'):
                            rollBackSql["sql"].append(sql[0])
            else:
                return "可能原因：1.该工单未选择备份，2.sql类型不是在线编写，3.工单还未执行"
        return  rollBackSql                 

    
class ApplyManage(OrderBase): 
    def __init__(self):
        super(ApplyManage, self).__init__()  
    
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="ApplyManage没有{sub}方法".format(sub=sub))       
            raise Http404    
    
    def get_db(self,request):
        if request.method == 'GET':cid = request.GET.get('order_db')
        elif request.method == 'POST':cid = request.POST.get('order_db')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('order_db')
        try:
            db = Database_MySQL_Detail.objects.get(id=cid)
            config = db.db_server.to_connect()
            config["db_name"] = db.db_name
            return db, config
        except Exception as ex:
            logger.warn(msg="获取数据库信息失败: {ex}".format(ex=ex))
            raise Http404 
    
    def __inception(self,config):
        return Inception(
                        host=config.get("ip"),name=config.get('db_name'),
                        user=config.get("db_user"),passwd=config.get("db_passwd"),
                        port=config.get("db_port")
                        )
    
    def __audit_by_incept(self,config,sql):
        incept = self.__inception(config)
        return  incept.checkSql(sql=sql)
            
        
    def __create_orders_system(self, request, order_type=0):
        try:
            order_executor = User.objects.get(id=request.POST.get('order_executor'))
            order = Order_System.objects.create(
                                       order_user=request.user.id,
                                       order_subject = request.POST.get('order_desc'),
                                       order_level = 0,
                                       order_executor = order_executor.id,
                                       order_audit_status = 2,
                                       order_execute_status = 0,
                                       order_type = order_type,
                                       start_time = request.POST.get('start_time'),
                                       end_time = request.POST.get('end_time'),
                                       )                 
        except Exception as ex:
            logger.error(msg="SQL审核失败: {ex}".format(ex=str(ex)))
            raise  Http404
        
        self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, "申请工单")
        
        return order 
    
    def __create_orders_sql_online(self,db,request):
        order = self.__create_orders_system(request)       
        try:
            order_sql = SQL_Audit_Order.objects.create(
                                           order = order,
                                           order_db = db,   
                                           order_type = 'online',                                                            
                                           order_sql = request.POST.get('order_sql'),
                                           sql_backup = request.POST.get('sql_backup'),
                                           )
            
            return order_sql
        except Exception as ex:
            order.delete()
            logger.error(msg="SQL审核失败: {ex}".format(ex=str(ex)))
            return str(ex)

        
    def __create_orders_sql_human(self,db,request):
        order = self.__create_orders_system(request)      
        try:
            order_sql = SQL_Audit_Order.objects.create(
                                           order = order,
                                           order_db = db,   
                                           order_type = 'human',                                                            
                                           order_sql = request.POST.get('order_sql'),
                                           sql_backup = 0,
                                           )
            return order_sql
        except Exception as ex:
            order.delete()
            logger.error(msg="SQL审核失败: {ex}".format(ex=str(ex)))
            return str(ex)        
        
    def __create_orders_sql_file(self,db,request):
        order = self.__create_orders_system(request)       
        try:                                  
            order_sql = SQL_Audit_Order.objects.create(
                                            order = order,
                                            order_db = db,
                                            order_type = 'file',  
                                            order_sql = request.POST.get('order_sql'),
                                            order_file = request.FILES.get('order_file'),
                                        )  
#             sendOrderNotice.delay(order.id,mask='【申请中】') 
            return order_sql                         
        except Exception as ex:
            logger.error(msg="SQL文件审核失败: {ex}".format(ex=str(ex)))       
            return str(ex)

    
    def __create_orders_upload_file(self,request):
        order = self.__create_orders_system(request=request,order_type=2)
        try:
            upload = FileUpload_Audit_Order.objects.create(
                                                           order = order,
                                                           dest_path=request.POST.get('dest_path'),
                                                           dest_server=json.dumps(request.POST.get('server').split(',')),
                                                           chown_user=request.POST.get('chown_user'),
                                                           chown_rwx=request.POST.get('chown_rwx'),
                                                           order_content=request.POST.get('order_content'),
                                                           )
        except Exception as ex:
            order.delete()
            logger.error(msg="文件上传失败: {ex}".format(ex=ex))
            return str(ex)  
            
        for files in request.FILES.getlist('order_files[]'): 
            try:
                upFile = UploadFiles.objects.create(file_order=upload,file_path=files)
                filePath = os.getcwd() + '/upload/' + str(upFile.file_path)
                upFile.file_type = base.getFileType(filePath)
                upFile.save()
            except Exception as ex:
                order.delete()
                upload.delete()
                logger.error(msg="文件上传保存失败: {ex}".format(ex=ex))
                return str(ex)                   

        
     
    def __create_orders_download_file(self,request):
        order = self.__create_orders_system(request=request,order_type=3)
        try:
            download = FileDownload_Audit_Order.objects.create(
                                                           order = order,
                                                           dest_path=request.POST.get('dest_path'),
                                                           dest_server=json.dumps(request.POST.get('server').split(',')),
                                                           order_content=request.POST.get('order_content'),
                                                           )
        except Exception as ex:
            order.delete()
            logger.error(msg="文件上传失败: {ex}".format(ex=ex))
            return str(ex)                  
    
    def __create_orders_service(self,request):      
        order = self.__create_orders_system(request=request,order_type=1)
 
        try:
            operation = Service_Audit_Order.objects.create(
                                                           order = order,
                                                           order_content=request.POST.get('order_content'),
                                                           file_path=request.FILES.get('order_files',None),
                                                           )
        except Exception as ex:
            order.delete()
            logger.error(msg="运维工单创建失败: {ex}".format(ex=ex))
            return str(ex)  
        
        if operation.file_path:
            try:
                filePath = os.getcwd() + '/upload/' + str(operation.file_path)
                operation.file_type = base.getFileType(filePath)
                operation.file_md5 = base.get_file_md5sum(filePath)
                operation.save()       
            except Exception as ex:
                operation.delete()
                order.delete()
                logger.error(msg="运维工单更新失败: {ex}".format(ex=ex))
                return str(ex)                   
            
    def __check_orders(self,request,order_type=0):
        return Order_System.objects.filter(order_subject=request.POST.get('order_desc'),order_type=order_type).count()
    
    def sql_audit(self,request):    
        
        db,config = self.get_db(request)
        
        count = self.__check_orders(request,0)
        if count >=1:return "请勿重复提交"

        if INCEPTION_CONFIG and request.POST.get("sql_type") == "online": #如果开启inception审核就走下面的流程
            result = self.__audit_by_incept(config, request.POST.get("order_sql"))

            if result.get('status') == 'success':
                order_sql = self.__create_orders_sql_online(db, request)
                if isinstance(order_sql,SQL_Audit_Order):return result.get('data')
                else:return order_sql
            else:
                return result.get('data')
            
        elif request.POST.get("sql_type") == "file":
            order_sql = self.__create_orders_sql_file(db, request)
            if isinstance(order_sql,SQL_Audit_Order):return 
            else:return order_sql 
             
        elif request.POST.get("sql_type") == "human":
            order_sql = self.__create_orders_sql_human(db, request)
            if isinstance(order_sql,SQL_Audit_Order):return  
            else:return order_sql  
        else:              
            return "请确认是否有配置Inception"

    
    def upload_audit(self,request):
        count = self.__check_orders(request,2)
        if count >=1:return "请勿重复提交"
        return self.__create_orders_upload_file(request)
    
    def download_audit(self,request):
        count = self.__check_orders(request,3)
        if count >=1:return "请勿重复提交"
        return self.__create_orders_download_file(request)    
         
    
    def service_audit(self, request):
        count = self.__check_orders(request,1)
        if count >=1:return "请勿重复提交"
        return self.__create_orders_service(request)         
    
class OrderProgres(OrderBase):
    def __init__(self):
        super(OrderProgres, self).__init__()  
    
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="OrderStatus没有{sub}方法".format(sub=sub))       
            raise Http404      
    
    def get_osc(self,request):
        order = self.check_perms(request)
        db, config = self.get_db(order)   
        if db:
            if INCEPTION_CONFIG and order.sql_audit_order.order_type == "online":        
                incept = self.inception(config)
                for ds in self.get_incept_sql_result(order): 
                    if ds.backup_db.find('None') == -1:
                        if ds.sqlsha:return incept.getOscStatus(sqlSHA1=ds.sqlsha) 
#         return {"status":'success', "data":{"percent":random.randint(1, 120), "timeRemained":"{m}:{s}".format(m=random.randint(1, 60), s=random.randint(10, 60))}} 
        return {"status":'error', "data":{"percent":100, "timeRemained":"00:00"}}
                       
class OrderSQLManage(OrderBase): 
    def __init__(self):
        super(OrderSQLManage, self).__init__() 
       
        
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="OrderManage没有{sub}方法".format(sub=sub))       
            raise Http404             

    def __check_perms(self, request):
        
        order = self.get_order(request)
        
        if order.is_expired() and order.is_unexpired():  

            if order.order_execute_status not in [0, 1]: raise PermissionDenied()

            if order.order_audit_status != 3: raise PermissionDenied()               

            if request.user.is_superuser:
                return order
              
            if request.user.id == order.order_user:
                return order  
        
        raise PermissionDenied()
    
    def __exec_by_incept(self,config,sql,action):
        incept = self.inception(config)
        return incept.execSql(sql,action)

    
    def __create_sql_exec_result(self,order,data):
        try:                            
            SQL_Order_Execute_Result.objects.create(
                                                    order = order.sql_audit_order,
                                                    errlevel = data.get('errlevel'),
                                                    stage = data.get('stage'),
                                                    stagestatus = data.get('stagestatus'),
                                                    errormessage = data.get('errormessage'),
                                                    sqltext =  data.get('sqltext'),
                                                    affectrow = data.get('affectrow'),
                                                    sequence = data.get('sequence'),
                                                    backup_db = data.get('backup_dbname'),
                                                    execute_time = data.get('execute_time'),
                                                    sqlsha = data.get('sqlsha1'),
                                                    )
        except Exception as ex:
            logger.error(msg="记录SQL错误: {ex}".format(ex=str(ex)))               
    
    def __incept_sql(self, config, order, request):
        if order.sql_audit_order.sql_backup == 1:action = None
        else:action='--disable-remote-backup;'
        result = self.__exec_by_incept(config, order.sql_audit_order.order_sql,action)
        if result.get('status') == 'success':
            count = 0
            sList = []
            for ds in result.get('data'):
                self.__create_sql_exec_result(order, ds)
                if ds.get('errlevel') > 0 and ds.get('errormessage'):count = count + 1
                sList.append({'sqltext':ds.get('sqltext'),'affectrow':ds.get('affectrow'),'errormessage':ds.get('errormessage')})
            if count > 0:
                order.order_execute_status = 5
                order.save()  
                return {"status":5,"result":sList,"type":"incept"}       
            else:
                order.order_execute_status = 2
                order.save()
                return {"status":2,"result":sList,"type":"incept"}               
        else:
            return {"status":5,"result":result.get('msg'),"type":"incept"}             
    
    def __human_sql(self, config, order, request):
        incept = self.inception(config)
        for sql in order.sql_audit_order.order_sql.split('\n'):
            if sql.isspace():continue
            result = incept.exec_custom_sql(sql)
            if result.get('status') == 'error':#
                order.order_execute_status = 5
                order.sql_audit_order.order_err = result.get('errinfo')
                order.save() 
                order.sql_audit_order.save()  
                self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, result.get('errinfo'))         
                return {"status":5,"result":result.get('errinfo'),"type":"human"}        
        order.order_execute_status = 2
        order.save()    
        self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, "执行工单")
        return {"status":2,"result":"","type":"human"}              
    
    def __file_sql(self, config, order, request):
        filePath = os.getcwd() + '/upload/' + str(order.sql_audit_order.order_file)
        rc,rs = cmds.loads(    
                            host=config.db_assets.server_assets.ip,
                            dbname=config.db_name,
                            user=config.db_user,
                            passwd=config.db_passwd,
                            port=config.db_port,
                            sql=filePath
                            )
        if rc == 0:
            order.order_execute_status = 5
            order.save()   
            self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, "执行工单") 
            return {"status":5,"result":"","type":"file"}                  
#             sendOrderNotice.delay(order.id,mask='【已执行】')
        else:
            order.order_status = 9
            order.sql_audit_order.order_err = str(rs)
            order.save() 
            order.sql_audit_order.save()
            self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, "执行工单")
            return {"status":9,"result":str(rs),"type":"file"}                     
#             sendOrderNotice.delay(order.id,mask='【已失败】')
               
    def exec_sql(self,request):
        order = self.__check_perms(request)
        
        db, config = self.get_db(order)
        
        if INCEPTION_CONFIG and order.sql_audit_order.order_type == "online": #如果开启inception审核就走下面的流程
            return self.__incept_sql(config, order, request)      
                  
        elif order.sql_audit_order.order_type == "file":
            return self.__file_sql(config, order, request)  
        
        elif order.sql_audit_order.order_type == "human":        
            return self.__human_sql(config, order, request)
        else:
            return "工单SQL类型不正确"

            

    def sql(self,request):   
        return self.__check_perms(request)

    
    def stop_osc(self,request):
        order = self.__check_perms(request)
        
        db,config = self.get_db(order)   
        
        if INCEPTION_CONFIG and order.sql_audit_order.order_type == "online":        
            incept = self.inception(config)
            for ds in self.get_incept_sql_result(order): 
                if ds.backup_db.find('None') == -1:
                    if ds.sqlsha :return incept.stopOsc(sqlSHA1=ds.sqlsha) 
            return "任务已完成"
                       
    
    def rollback_sql(self,request):    
        order = self.__check_perms(request)   
         
        db, config = self.get_db(order)    
         
        incept = self.inception(config)
        
        sqlList= self.get_rollback_sqls(order,config)
        
        if isinstance(sqlList, dict):
            for sql in sqlList["sql"]:
                result = incept.exec_custom_sql(sql)
                if result.get('status') == 'error':#回滚时如果其中一条出现错误就停止回滚 
                    return result.get('errinfo')
            #回滚语句如果全部执行成功则修改状态
            order.order_execute_status = 3
            order.save()         
            self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, "回滚工单")
#                 sendOrderNotice.delay(order.id,mask='【已回滚】')                     
        else:
            return sqlList
             
        
class OrderFileUploadManage(OrderBase,AssetsSource): 
    def __init__(self):
        super(OrderFileUploadManage, self).__init__() 
       
        
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="OrderFileUploadManage没有{sub}方法".format(sub=sub))       
            raise Http404           

    def __check_perms(self, request):
                
        order = self.get_order(request)
 
        if order.is_expired() and order.is_unexpired():  

            if order.order_execute_status not in [0, 1]: raise PermissionDenied()

            if order.order_audit_status != 3: raise PermissionDenied()               

            if request.user.is_superuser:
                return order
              
            if request.user.id == order.order_user:
                return order   
                    
        raise PermissionDenied()
    
    def __check_assets(self,request,order):
        assets_list = []
        try:
            dest_server = [ self.assets(ds) for ds in json.loads(order.fileupload_audit_order.dest_server) ]
            assetsList = [ ds.id for ds in self.query_user_assets(request, dest_server) ]
            if assetsList:
                for aid in request.POST.getlist('server[]'):
                    if int(aid) in assetsList:assets_list.append(int(aid))
                    else:return "您选择的资产与工单资产不一致"
                return assets_list
            else:
                return "您选择了没有分配给你的资产"
        except Exception as ex:
            logger.error(msg="检查文件分发资产失败:{ex}".format(ex=ex))       
            return str(ex)
    
    def __check_files(self,order,request):
        filesList = []
        try:
            fileList = [ ds.id for ds in order.fileupload_audit_order.uploadfiles.all() ]
        except Exception as ex:
            return str(ex)
        
        try:
            for files in request.POST.getlist('files[]'):
                if int(files) in fileList:filesList.append(int(files))
                else:return "您选择了工单不存在文件"
            if filesList: return filesList
            else:return "文件不存在"
        except Exception as ex:
            return str(ex)
        
    def __run_fileupload_by_ansible(self, order, assetsList, fileList, request):
        dataList = [] 
        sList, resource  = self.idSourceList(assetsList)
        
#         if order.order_execute_status not in [0, 1]: return "工单状态已经被处理"
        
        if len(sList) == 0: return "资产信息不存在"
        
        ANS = ANSRunner(resource)  
           
        for files in fileList:
            file = UploadFiles.objects.get(id=files)     
            filePath = os.getcwd() + '/upload/' + str(file.file_path)        
            module_args = "src={src} dest={dest} mode={chown_rwx} owner={chown_user} group={chown_user} backup={backup}".format(src=filePath,backup="yes",
                                                                                                                           dest=order.fileupload_audit_order.dest_path,
                                                                                                                           chown_user=order.fileupload_audit_order.chown_user,
                                                                                                                           chown_rwx=order.fileupload_audit_order.chown_rwx
                                                                                                       )      
            ANS.run_model(host_list=sList,module_name='copy',module_args=module_args) 
            
            result = json.loads(ANS.get_model_result())
            
            if result.get('success'):
                for k,v in result.get('success').items():
                    data = dict()
                    data['host'] = k
                    data["fname"] = str(file.file_path).split("/")[-1]
                    data["changed"] = v.get('changed')
                    data["dest"] = v.get('dest')
                    data["size"] = v.get("size")/1024/1024
                    data["status"] = "success"
                    data["msg"] = None
                    dataList.append(data) 
                    
            if result.get('unreachable'):
                for k,v in result.get('unreachable').items():
                    data = dict()
                    data['host'] = k
                    data["fname"] = str(file.file_path).split("/")[-1]
                    data["changed"] = "false"
                    data["dest"] = order.fileupload_audit_order.dest_path
                    data["size"] = "未知"
                    data["status"] = "falied"
                    data["msg"] = v.get("msg")
                    dataList.append(data)  
            if result.get('failed'):
                
                for k,v in result.get('failed').items():
                    data = dict()
                    data['host'] = k
                    data["fname"] = str(file.file_path).split("/")[-1]
                    data["changed"] = "false"
                    data["dest"] = order.fileupload_audit_order.dest_path
                    data["size"] = "未知"
                    data["status"] = "falied"
                    data["msg"] = v.get("msg")
                    dataList.append(data) 
                    
        self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, "执行工单")
                                           
        return dataList                         
    
    def fileupload(self,request):
        return self.__check_perms(request)   
   
     
    def exec_fileupload(self,request):
        order = self.__check_perms(request)
        
        assetsList = self.__check_assets(request, order)
        
        if isinstance(assetsList, str):return assetsList        
        
        filesList = self.__check_files(order, request)

        if isinstance(filesList, str):return filesList
        
        return self.__run_fileupload_by_ansible( order, assetsList, filesList, request)

    
            
class OrderFileDownloadManage(OrderBase,AssetsSource): 
    def __init__(self):
        super(OrderFileDownloadManage, self).__init__() 
       
        
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="OrderFileDownloadManage没有{sub}方法".format(sub=sub))       
            return "参数错误"           
    
    def __check_perms(self, request):
        
        order = self.get_order(request)
            
        if order.is_expired() and order.is_unexpired():  
              
            if order.order_execute_status not in [0, 1]: raise PermissionDenied()

            if order.order_audit_status != 3: raise PermissionDenied()               

            if request.user.is_superuser:
                return order
              
            if request.user.id == order.order_user:
                return order  
        
        raise PermissionDenied()
    
    def __check_assets(self,request,order):
        assets_list = []
        try:
            dest_server = [ self.assets(ds) for ds in json.loads(order.filedownload_audit_order.dest_server) ]
            
            assetsList = [ ds.id for ds in self.query_user_assets(request, dest_server) ]
            
            if assetsList:
                for aid in request.POST.getlist('server[]'):
                    if int(aid) in assetsList:assets_list.append(int(aid))
                    else:return "您选择的资产与工单资产不一致"
                return assets_list
            else:
                return "您选择了没有分配给你的资产"
        except Exception as ex:
            logger.error(msg="检查文件下载资产失败:{ex}".format(ex=ex))       
            return str(ex) 
    
        
    def __run_filedownload_find_by_ansible(self, order, assetsList, request): 
        assets_data,dataList = {},[]
                
        sList, resource  = self.idSourceList(assetsList)
        
        if len(sList) == 0: return "资产信息不存在"
        
        for aid in assetsList:
            try:
                assets_data[self.assets(aid).server_assets.ip] = aid
            except Exception as ex:
                logger.error(msg="检查文件下载资产失败:{ex}".format(ex=ex))    
                return str(ex)  
            
        ANS = ANSRunner(resource)                
        module_args = "paths={dest}".format( dest=order.filedownload_audit_order.dest_path)
        
        ANS.run_model(host_list=sList,module_name='find',module_args=module_args)
        
        filesData = json.loads(ANS.get_model_result())
        for k,v in filesData.get('success').items():
            for ds in v.get('files'):
                data = {}
                data["id"] = order.id
                data["aid"] = assets_data.get(k)
                data['host'] = k
                data['path'] = ds.get('path')
                data['size'] = ds.get('size')/1024/1024
                data['islnk'] = ds.get('islnk')
                dataList.append(data)  
                
        self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, "执行工单")    
                               
        return dataList    

    def __run_filedownload_by_ansible(self,order,assetsList):         
        if order.order_status != 8: return "工单状态已经被处理"
        
        sList,resource  = self.idSourceList(assetsList)
        
        if len(sList) == 0: return "资产信息不存在"
        
        ANS = ANSRunner(resource) 
        
        return sList,ANS  

    
    def filedownload(self,request):
                
        return self.__check_perms(request)
           
    def file_downloads(self,request):
        
        order = self.__check_perms(request)

        assetsList = self.__check_assets(request, order)
                       
        return self.__run_filedownload_by_ansible(order,assetsList)

            
     
    def exec_filedownload(self,request):

        order = self.__check_perms(request)

        assetsList = self.__check_assets(request, order)

        if isinstance(assetsList, str):return assetsList   
        
        return self.__run_filedownload_find_by_ansible(order, assetsList, request)
             
            
ORDERS_COUNT_RBT =  OrdersCount()  
            