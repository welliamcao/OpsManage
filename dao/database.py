#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import os,json,queue
from databases.models import *
from utils.logger import logger
from .assets import AssetsBase 
from asset.models import *
from django.http import QueryDict
from datetime import datetime,timedelta,date
from django.contrib.auth.models import User
from dao.base import MySQLPool
from utils import base
from utils.binlog2sql import Binlog2sql


class MySQLARCH(object):
    def __init__(self,mysql,db_server):
        super(MySQLARCH,self).__init__()  
        self.mysql = mysql
        self.mysql_status = self.mysql.get_status()
        self.db_server = db_server
        self.arch_info = {
                    'title': self.db_server.db_mark,
                    'className': 'product-dept',
                    'children': []                   
                }
    
    def slave(self):
        slave_data = {}
        for ds in self.mysql.get_master_status():
            if ds.get('name') == 'Slave':slave_data[self.db_server.db_assets.server_assets.ip+':'+str(self.db_server.db_port)] = ds.get('value')  
        return slave_data
        
    def pxc(self):
        self.arch_info["name"] = 'PXC模式'
        pxc_server_list =  []
        for ds in self.mysql_status[1]:
            if ds.get('name') == 'Wsrep_incoming_addresses':pxc_server_list = ds.get('value').split(',')
        for s in pxc_server_list:
            data = {}
            host = s.split(':')[0]
            port = s.split(':')[1]
            data['name'] = host
            data['title'] = port
            data['children'] = []
            if self.slave().has_key(s):
                data['name'] = 'master'
                data['title'] = host+':'+port
                count = 1
                for d in self.slave().get(s):
                    x = {}
                    host = d.split(':')[0]
                    port = d.split(':')[1]
                    x['name'] = 'slave-' + str(count)
                    x['title'] =  host+':'+port
                    count = count + 1
                    data['children'].append(x)                                                             
            self.arch_info['children'].append(data) 
        return  self.arch_info  
    
    def master_slave(self):
        count = 1
        self.arch_info["name"] = '主从模式'
        for m in self.mysql.get_slave_status():
            if m.get('name') == 'Master_Host':
                self.arch_info['children'].append({"name":'Master-' + str(count),"title":m.get('value')})
                count = count + 1
        for ds in self.mysql.get_master_status():
            if ds.get('name') == 'Slave':
                count = 1
                for s in ds.get('value'):
                    x = {}
                    host = s.split(':')[0]
                    port = s.split(':')[1]
                    x['name'] = 'slave-' + str(count)
                    x['title'] =  host+':'+port 
                    count = count + 1  
                    self.arch_info['children'].append(x)   
        return  self.arch_info  
    
    def single(self):
        self.arch_info["name"] = '单例模式'
        return  self.arch_info 


class DBConfig(AssetsBase):
    def __init__(self):
        super(DBConfig,self).__init__() 
        
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="DBConfig没有{sub}方法".format(sub=sub))       
            return "参数错误"    
        
    def incept(self):
        try:
            return Inception_Server_Config.objects.get(id=1)
        except Exception as ex:
#             logger.error(msg="Inception未配置: {ex}".format(ex=str(ex)))
            return None   
            
    def get_custom_sql(self,request=None):
        dataList = []
        for ds in Custom_High_Risk_SQL.objects.all():
            dataList.append(self.convert_to_dict(ds))
        return dataList
        
    def database(self,ids): 
        try:
            database = DataBase_Server_Config.objects.get(id=ids)
        except Exception as ex:
            return "查询数据库{ids}，失败{ex}".format(ids=ids,ex=ex) 
        return  json.dumps(self.convert_to_dict(database))       
    
    def get_all_db(self,request=None):
        dataList = []
        for ds in DataBase_Server_Config.objects.all():
            data = self.convert_to_dict(ds)
            try:
                data["ip"] = ds.db_assets.server_assets.ip
            except Exception as ex:
                logger.warn(msg="查询资产失败: {ex}".format(ex=ex))
                data["ip"] = "未知"
            try:
                data["project"] = Project_Assets.objects.get(id=ds.db_assets.project).project_name
            except Exception as ex:
                logger.warn(msg="查询项目失败: {ex}".format(ex=ex))
                data["project"] = "未知"   
            try:
                data["service"] = Service_Assets.objects.get(id=ds.db_assets.project).service_name
            except Exception as ex:
                logger.warn(msg="查询应用失败: {ex}".format(ex=ex))  
                data["service"] = "未知"                              
            data.pop("db_assets_id")
            data.pop("db_passwd")            
            dataList.append(data)
        return dataList
    
    def create_data_base(self,request):        
        try:
            DataBase_Server_Config.objects.create(
                                          db_env=request.POST.get('db_env'),
                                          db_type=request.POST.get('db_type'),
                                          db_name=request.POST.get('db_name'),
                                          db_host=request.POST.get('db_host'),
                                          db_mode=request.POST.get('db_mode'),
                                          db_user=request.POST.get('db_user'),
                                          db_port=request.POST.get('db_port'),
                                          db_service=request.POST.get('db_service'),
                                          db_project=request.POST.get('db_project'),
                                          db_mark=request.POST.get('db_mark')
                                          )
        except Exception as ex:
            logger.warn(msg="添加数据库失败: {ex}".format(ex=ex))  
            return "添加数据库失败: {ex}".format(ex=ex)
        return True
    
    def update_data_base(self,request): 
        try:   
            database = DataBase_Server_Config.objects.get(id=QueryDict(request.body).get('script_id'))
        except Exception as ex:
            return "更新数据库失败: {ex}".format(ex=ex)
        try:
            DataBase_Server_Config.objects.filter(id=database.id).update(
                                          db_env=QueryDict(request.body).get('db_env'),
                                          db_type=QueryDict(request.body).get('db_type'),
                                          db_name=QueryDict(request.body).get('db_name'),
                                          db_host=QueryDict(request.body).get('db_host'),
                                          db_mode=QueryDict(request.body).get('db_mode'),
                                          db_user=QueryDict(request.body).get('db_user'),
                                          db_port=QueryDict(request.body).get('db_port'),
                                          db_service=QueryDict(request.body).get('db_service'),
                                          db_project=QueryDict(request.body).get('db_project'),
                                          db_mark=QueryDict(request.body).get('db_mark'),                                          
                                          update_date = datetime.now()
                                          )
        except Exception as ex:
            logger.error(msg="更新数据库失败: {ex}".format(ex=str(ex)))
            return "更新数据库失败: {ex}".format(ex=str(ex))
        return True  
    
    def delete_data_base(self,request):
        try:   
            database = DataBase_Server_Config.objects.get(id=QueryDict(request.body).get('id'))
            database.delete()
        except Exception as ex:
            return "删除数据库配置失败: {ex}".format(ex=ex)             
        return True  
           
    
    def get_user_db(self,request=None):
        user_database_list = []
        for ds in Database_User.objects.all():
            try:
                dbConfig = DataBase_Server_Config.objects.get(id=ds.db)
                data = self.convert_to_dict(dbConfig)
                try:
                    data["ip"] = dbConfig.db_assets.server_assets.ip
                except Exception as ex:
                    data["ip"] = "未知"
                dbUser = User.objects.get(id=ds.user)
                data["username"] = dbUser.username
                data["uid"] = dbUser.id
                data.pop("db_assets_id")
                data.pop("db_passwd")
                data.pop("db_user")
                user_database_list.append(data)
            except Exception as ex:
                logger.error(msg="查询数据库失败: {ex}".format(ex=str(ex)))  
        return user_database_list
        

class DBUser(object):
    def __init__(self):
        super(DBUser,self).__init__() 

    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="DBUser没有{sub}方法".format(sub=sub))       
            return "参数错误" 

    def create_user_database(self,request):    
        for ds in request.POST.getlist('db'):   
            try:
                Database_User.objects.create(
                                              user=request.POST.get('user'),
                                              db=ds,
                                              )
            except Exception as ex:
                logger.warn(msg="用户分配数据库失败: {ex}".format(ex=ex))  
                return "添加数据库失败: {ex}".format(ex=ex)
        return True    

    def update_user_database(self,request):
        db_list = [ int(i) for i in QueryDict(request.body).getlist('db') ]
        user_db_list = [ ds.db for ds in self.query_db(request)]
        add_db_List = list(set(db_list).difference(set(user_db_list)))
        del_db_list = list(set(user_db_list).difference(set(db_list)))   
        #添加新增的db
        for db in add_db_List:
            try:
                Database_User.objects.create(user=QueryDict(request.body).get('user'),db=db)
            except Exception as ex:
                logger.warn(msg="更新用户数据库失败: {ex}".format(ex=ex))  
                return "更新用户数据库失败: {ex}".format(ex=ex)                
        #删除去掉的db
        try:
            Database_User.objects.filter(user=QueryDict(request.body).get('user'),db__in=del_db_list).delete()
        except Exception as ex:
            logger.warn(msg="更新用户数据库失败: {ex}".format(ex=ex)) 
            return "更新用户数据库失败: {ex}".format(ex=ex)
        return True
           
    def delete_user_database(self,request):
        try:
            Database_User.objects.get(id=QueryDict(request.body).get('id')).delete()
        except Exception as ex:
            logger.warn(msg="删除用户数据库失败: {ex}".format(ex=ex)) 
            return "删除用户数据库失败: {ex}".format(ex=ex)
        return True        
            
    def query_db(self,request):
        if User.objects.get(id=QueryDict(request.body).get('user')).is_superuser  == 1:
            return Database_User.objects.all()
        else:
            return Database_User.objects.filter(user=QueryDict(request.body).get('user'))
    
    
    def get_all_user_db(self,request):
        user_database_list = []        
        for ds in DataBase_Server_Config.objects.all():
            data = dict()
            data["id"] = ds.id
            data["db_env"] = ds.db_env
            data["ip"] = ds.db_assets.server_assets.ip
            data["db_name"] = ds.db_name
            data["db_mark"] = ds.db_mark 
            data["count"] = Database_User.objects.filter(user=request.GET.get('uid',request.user.id),db=ds.id).count()
            user_database_list.append(data)
        return user_database_list

    def get_user_db(self,request):
        user_database_list = []
        if request.user.is_superuser:
            dbList = DataBase_Server_Config.objects.filter(db_env=request.GET.get("env"))   
        else: 
            user_db_list = [ds.db for ds in Database_User.objects.filter(user=request.GET.get('uid',request.user.id))]     
            dbList = DataBase_Server_Config.objects.filter(id__in=user_db_list,db_env=request.GET.get("env"))   
        for ds in dbList:
            data = dict()
            data["id"] = ds.id
            data["db_env"] = ds.db_env
            data["ip"] = ds.db_assets.server_assets.ip
            data["db_name"] = ds.db_name
            data["db_mark"] = ds.db_mark 
            data["count"] = 1
            user_database_list.append(data)
        return  user_database_list            

class DBManage(AssetsBase):  
    def __init__(self):
        super(DBManage,self).__init__() 
        
    def allowcator(self,sub,request):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(request)
        else:
            logger.error(msg="DBManage没有{sub}方法".format(sub=sub))       
            return "参数错误"
    
    def __get_db(self,request):
        try:
            return  DataBase_Server_Config.objects.get(id=self.change(request.POST.get('db')))
        except Exception as ex:
            logger.error(msg="获取DB实例失败: {ex}".format(ex=ex))       
            return False   
                                   
    
    def __get_db_server(self,request):
        try:
            dbServer = self.__get_db(request)
            return MySQLPool(host=dbServer.db_assets.server_assets.ip,
                              port=dbServer.db_port,user=dbServer.db_user,
                              passwd=dbServer.db_passwd,dbName=dbServer.db_name)
        except Exception as ex:
            logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
            return ex      

    def __get_db_servers(self,request,queues):
        dataList = []
        for db in request.POST.getlist('db[]'):
            try:
                dbServer = DataBase_Server_Config.objects.get(id=self.change(db))
                dbRbt = MySQLPool(host=dbServer.db_assets.server_assets.ip,
                                  port=dbServer.db_port,user=dbServer.db_user,
                                  passwd=dbServer.db_passwd,dbName=dbServer.db_name,
                                  sql=request.POST.get('sql'),model='queryMany',
                                  queues=queues)
                dbRbt.start()              
            except Exception as ex:
                logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
                return "数据库不存在"  
        while True:
            while not queues.empty():
                dataList.append(queues.get())
            if  0 < len(dataList) >= len(request.POST.getlist('db[]')):break   
        return dataList      
        
    def query_sql(self, request):
        if not request.user.has_perm('databases.database_query_database_server_config'):return "您没有权限操作此项"
        queues = queue.Queue(maxsize=100)
        try:
            sqlCmd = request.POST.get('sql').split(' ')[0].lower()
        except Exception as ex:
            logger.error(msg="解析SQL失败: {ex}".format(ex=ex)) 
            return '解析SQL失败'
        if sqlCmd in ["select","show"]:return self.__get_db_servers(request,queues)
        else:return 'SQL类型不支持'
            
    
    def binlog_sql(self,request):
        if not request.user.has_perm('databases.database_binlog_database_server_config'):return "您没有权限操作此项"
        result = self.__get_db_server(request).queryAll(sql='show binary logs;')
        binLogList = []
        if isinstance(result,tuple):
            for ds in result[1]:
                binLogList.append(ds[0]) 
        return binLogList
    
    def table_list(self,request):
        result = self.__get_db_server(request).queryAll(sql='show tables;')
        tableList = []
        if isinstance(result,tuple):
            for ds in result[1]:
                tableList.append(ds[0]) 
        return tableList
    
    def table_schema(self,request):
        if not request.user.has_perm('databases.database_schema_database_server_config'):return "您没有权限操作此项"
        table_data = {}
        dbInfo = self.get_db(request)
        dbRbt  = self.__get_db_server(request)
        table_data["schema"] = dbRbt.queryMany(sql="""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_TYPE,ENGINE,VERSION,ROW_FORMAT,
                                                    TABLE_ROWS,concat(round(sum(DATA_LENGTH/1024/1024),2),'MB') AS DATA_LENGTH,
                                                    MAX_DATA_LENGTH,concat(round(sum(INDEX_LENGTH/1024/1024),2),'MB') AS INDEX_LENGTH,
                                                    DATA_FREE,AUTO_INCREMENT,CREATE_TIME,TABLE_COLLATION,TABLE_COMMENT FROM information_schema.TABLES 
                                                    WHERE  TABLE_SCHEMA='{db}' AND TABLE_NAME='{table}';""".format(db=dbInfo.db_name,table=request.POST.get('table_name')),num=1000)
        table_data["index"] = dbRbt.queryMany(sql="""SHOW index FROM `{table}`;""".format(db=dbInfo.db_name,table=request.POST.get('table_name')),num=1000)
        table_data["desc"] = dbRbt.queryOne(sql="""show create table `{table}`;""".format(db=dbInfo.db_name,table=request.POST.get('table_name')),num=1)[1][1]
        return table_data
            
    def parse_sql(self,request):
        if not request.user.has_perm('databases.database_binlog_database_server_config'):return "您没有权限操作此项"
        sqlList = []
        try:
            dbServer = self.get_db(request)
            timeRange =  request.POST.get('binlog_time').split(' - ') 
            conn_setting = {'host': dbServer.db_assets.server_assets.ip, 'port': dbServer.db_port, 'user': dbServer.db_user, 'passwd': dbServer.db_passwd, 'charset': 'utf8'}
            binlog2sql = Binlog2sql(connection_settings=conn_setting,             
                                    back_interval=1.0, only_schemas=dbServer.db_name,
                                    end_file='', end_pos=0, start_pos=4,
                                    flashback=True,only_tables='', 
                                    no_pk=False, only_dml=True,stop_never=False, 
                                    sql_type=['INSERT', 'UPDATE', 'DELETE'], 
                                    start_file=request.POST.get('binlog_db_file'), 
                                    start_time=timeRange[0], 
                                    stop_time=timeRange[1],)
            sqlList = binlog2sql.process_binlog()    
        except Exception as ex:
            logger.error(msg="binglog解析失败: {ex}".format(ex=ex)) 
        return sqlList
    
    def optimize_sql(self,request):
        if not request.user.has_perm('databases.database_optimize_database_server_config'):return "您没有权限操作此项"
        dbServer = self.get_db(request)
        status,result = base.getSQLAdvisor(host=dbServer.db_assets.server_assets.ip, user=dbServer.db_user,
                                           passwd=dbServer.db_passwd, dbname=dbServer.db_name, 
                                           sql=request.POST.get('sql'),port=dbServer.db_port)
        return [result]        
        
    def query_user_db(self,request=None):
        user_database_list = []
        if request.user.is_superuser:
            dbList = DataBase_Server_Config.objects.all()      
        else: 
            dbList = DataBase_Server_Config.objects.filter(id__in=[ ds.db for ds in Database_User.objects.filter(user=request.user.id)]) 
        for ds in dbList:
            try:
                data = self.convert_to_dict(ds)
                try:
                    data["ip"] = ds.db_assets.server_assets.ip
                except Exception as ex:
                    data["ip"] = "未知"
                data.pop("db_assets_id")
                data.pop("db_passwd")
                data.pop("db_user")
                user_database_list.append(data)
            except Exception as ex:
                logger.error(msg="查询数据库失败: {ex}".format(ex=str(ex)))  
        return user_database_list  