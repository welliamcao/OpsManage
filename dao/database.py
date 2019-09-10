#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import os,json,queue,time
from databases.models import *
from utils.logger import logger
from .assets import AssetsBase 
from asset.models import *
from django.http import QueryDict
from datetime import datetime
from django.contrib.auth.models import User
from dao.base import MySQLPool
from utils import base
from utils.mysql.binlog2sql import Binlog2sql
from apps.tasks.celery_sql import record_exec_sql
from django.db.models import Count
from mptt.templatetags.mptt_tags import cache_tree_children  
from django.db.models import Q

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)  
    return "%02d:%02d:%02d" % (h, m, s)

class MySQLARCH(object):
    def __init__(self,mysql,db_server):
        super(MySQLARCH,self).__init__()  
        self.mysql = mysql
        self.mysql_status = self.mysql.get_status()
        self.db_server = db_server
        self.arch_info = {
                    'title': self.db_server.get("db_mark"),
                    'className': 'product-dept',
                    'children': []                   
                }
    
    def slave(self):
        slave_data = {}
        for ds in self.mysql.get_master_status():
            if ds.get('name') == 'Slave':slave_data[self.db_server.self.db_server.get("ip")+':'+str(self.db_server.get("db_port"))] = ds.get('value')  
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
            if s in self.slave().keys():
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
            dataList.append(ds.to_json())
        return dataList
    
    def create_data_base(self,request):        
        try:
            DataBase_Server_Config.objects.create(
                                          db_env=request.POST.get('db_env'),
                                          db_type=request.POST.get('db_type'),
                                          db_host=request.POST.get('db_host'),
                                          db_mode=request.POST.get('db_mode'),
                                          db_user=request.POST.get('db_user'),
                                          db_port=request.POST.get('db_port'),
                                          db_mark=request.POST.get('db_mark'),
                                          db_business=request.POST.get('db_business')
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
                                          db_host=QueryDict(request.body).get('db_host'),
                                          db_mode=QueryDict(request.body).get('db_mode'),
                                          db_user=QueryDict(request.body).get('db_user'),
                                          db_port=QueryDict(request.body).get('db_port'),
                                          db_business=QueryDict(request.body).get('db_business'),
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
                dbUser = User.objects.get(id=ds.user)
            except Exception as ex:
                logger.error(msg="查询数据库用户失败: {ex}".format(ex=str(ex)))  
                continue              
            try:
                dbConfig = DataBase_Server_Config.objects.get(id=ds.db)
                data = dbConfig.to_json()
                data["username"] = dbUser.username
                data["uid"] = dbUser.id
                user_database_list.append(data)
            except Exception as ex:
                logger.error(msg="查询数据库失败: {ex}".format(ex=str(ex)))  
        return user_database_list
        

class DBUser(object):
    def __init__(self):
        super(DBUser,self).__init__() 
        self.user_grants = ["create","drop","alter","truncate","insert","update","delete","select","show","desc","explain","rename"]
        
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
        db_list = [ int(i) for i in QueryDict(request.body).getlist('db[]') ]
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

    def modf_user_tables(self,request):
        table_list =  request.POST.getlist('table_name[]')

        try:
            userDbServer = Database_User.objects.get(id=request.POST.get('id',0))
        except Exception as ex:
            logger.warn(msg="查询用户数据库失败: {ex}".format(ex=ex)) 
            return '用户数据库未分配'  

        try:
            userDbServer.tables = ",".join(table_list)
            userDbServer.save()
        except Exception as ex:
            msg="修改用户数据库表失败: {ex}".format(ex=ex)
            logger.warn(msg=msg) 
            return msg         
    
    def modf_user_grants(self,request):
        grants_list =  request.POST.getlist('grants[]')

        try:
            userDbServer = Database_User.objects.get(id=request.POST.get('id',0))
        except Exception as ex:
            logger.warn(msg="查询用户数据库失败: {ex}".format(ex=ex)) 
            return '用户数据库未分配'  

        try:
            userDbServer.privs = ",".join(grants_list)
            userDbServer.save()
        except Exception as ex:
            msg="修改用户数据库表权限失败: {ex}".format(ex=ex)
            logger.warn(msg=msg) 
            return msg        
           
    def delete_user_database(self,request):
        try:
            Database_User.objects.get(db=QueryDict(request.body).get('id'),user=QueryDict(request.body).get('uid')).delete()
        except Exception as ex:
            logger.warn(msg="删除用户数据库失败: {ex}".format(ex=ex)) 
            return "删除用户数据库失败: {ex}".format(ex=ex)
        return True        
            
    def query_db(self,request):
        return Database_User.objects.filter(user=QueryDict(request.body).get('user'))
    
    
    def get_all_user_db(self,request):
        user_database_list = []        
        for ds in DataBase_Server_Config.objects.all():
            data = ds.to_json()
            data["count"] = Database_User.objects.filter(user=request.GET.get('uid',request.user.id),db=ds.id).count()
            user_database_list.append(data)
        return user_database_list
    
    def get_user_db_tables(self,request):  
        user_table_list = []
        try:
            userDbServer = Database_User.objects.get(id=request.GET.get('id',0))
        except Exception as ex:
            logger.warn(msg="查询用户数据库失败: {ex}".format(ex=ex)) 
            return '用户数据库未分配'
        
        try:
            dbServer = DataBase_Server_Config.objects.get(id=userDbServer.db)
        except Exception as ex:
            logger.warn(msg="查询数据库失败: {ex}".format(ex=ex)) 
            return '数据库不存在'  
              
        result= MySQLPool(dbServer=dbServer).queryMany('show tables',10000) 
        
        if not isinstance(result, str):
            count,tableList,colName = result[0],result[1],result[2]
            try:
                if userDbServer.tables:grant_tables = userDbServer.tables.split(",")
                else:grant_tables = []
            except Exception as ex:
                logger.warn(msg="查询用户授权表失败: {ex}".format(ex=ex)) 
                grant_tables = []

            if count > 0:
                for ds in tableList:
                    data = dict()
                    data["name"] = ds[0]
                    if ds[0] not in grant_tables:                    
                        data["count"] = 0
                    else:
                        data["count"] = 1
                    user_table_list.append(data)

        return user_table_list

    def get_user_db_grants(self,request):  
        user_grants_list = []
        try:
            userDbServer = Database_User.objects.get(id=request.GET.get('id',0))
        except Exception as ex:
            logger.warn(msg="查询用户数据库失败: {ex}".format(ex=ex)) 
            return '用户数据库未分配'

        try:
            if userDbServer.privs:user_grants = userDbServer.privs.split(",")
            else:user_grants = []
        except Exception as ex:
            logger.warn(msg="查询用户权限失败: {ex}".format(ex=ex)) 
            user_grants = []        
        for tb in self.user_grants:
            data = dict()
            data["name"] = tb
            if tb not in user_grants:                    
                data["count"] = 0
            else:
                data["count"] = 1
            user_grants_list.append(data)            
        return user_grants_list

    def get_user_db(self,request,**query_params):
        if request.user.is_superuser:
            dbList = DataBase_Server_Config.objects.filter(**query_params)   
        else: 
            user_db_list = [ds.db for ds in Database_User.objects.filter(user=request.user.id)]     
            dbList = DataBase_Server_Config.objects.filter(id__in=user_db_list,**query_params)   
        return  dbList     
             

class DBManage(AssetsBase):  
    dml_sql = ["insert","update","delete"]
    dql_sql = ["select","show","desc","explain"]
    ddl_sql = ["create","drop","alter","truncate"]
    
    def __init__(self):
        super(DBManage,self).__init__() 
        self.stime = int(time.time()) 
        
    def allowcator(self,sub,request):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(request)
        else:
            logger.error(msg="DBManage没有{sub}方法".format(sub=sub))       
            return "参数错误" 
    
    def __check_user_perms(self,request,perms='databases.databases_read_database_server_config'):
        
        dbServer = self.__get_db(request)

        if request.user.is_superuser and dbServer:
            return dbServer
        
        if  dbServer and request.user.has_perm(perms): 
            try:     
                if Database_User.objects.get(user=request.user.id,db=dbServer.get("id")):return dbServer
            except Exception as ex:
                logger.warn(msg="查询用户数据库信息失败: {ex}".format(ex=str(ex)))  
                return False    
            
        return False
    
    def __check_user_db_tables(self,request):
        if request.user.is_superuser:
            return []
        try:     
            userDbServer = Database_User.objects.get(user=request.user.id,db=request.POST.get('db'))
            if userDbServer.tables:return userDbServer.tables.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库表信息失败: {ex}".format(ex=str(ex)))  
            
        return []    
    
    def __check_user_db_privs(self,request):
        if request.user.is_superuser:
            return []
        try:     
            userDbServer = Database_User.objects.get(user=request.user.id,db=request.POST.get('db'))
            if userDbServer.privs:return userDbServer.privs.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库权限失败: {ex}".format(ex=str(ex)))  
            
        return []              
    
    def __check_sql_parse(self,request, allow_sql,dbname):
        
        try:
            sqlCmd = request.POST.get('sql').split(' ')[0].lower()
        except Exception as ex:
            logger.error(msg="解析SQL失败: {ex}".format(ex=ex)) 
            return '解析SQL失败'        

        if sqlCmd not in allow_sql: return 'SQL类型不支持'
        
        #查询用户是不是有授权表
        grant_tables = self.__check_user_db_tables(request)
        
        #提取SQL中的表名
        extract_table = base.extract_table_name_from_sql(request.POST.get('sql'))

        if extract_table:
            if grant_tables:
                for tb in extract_table:
                    if tb.find('.') >= 0:
                        db,tb = tb.split('.')[0],tb.split('.')[1]                        
                        if db != dbname:return "不支持跨库查询" 
                    if tb not in grant_tables:return "操作的表未授权"           
        else:
            return "SQL解析失败，无法获取表名"
            
        return True 
                  
    
    def __get_db(self,request):
        try:
            db_info = Database_Detail.objects.get(id=self.change(request.POST.get('db')))
            dbServer = db_info.db_server.to_connect()      
            dbServer["db_name"] = db_info.db_name
            return  dbServer
        except Exception as ex:
            logger.error(msg="获取DB实例失败: {ex}".format(ex=ex))       
            return False   
                                   
    
    def __get_db_server(self,request):
        try:
            dbServer = self.__get_db(request)
            return MySQLPool(dbServer=dbServer)
        except Exception as ex:
            logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
            return ex          
    
    def exec_sql(self, request):
        
        dbServer = self.__check_user_perms(request,'databases.databases_dml_database_server_config')
        if not dbServer:return "您没有权限操作此项"        
               
        sql_parse = self.__check_sql_parse(request, allow_sql=self.dml_sql + self.ddl_sql + self.dql_sql,dbname=dbServer.get('db_name'))

        if not isinstance(sql_parse, str):              
            result = self.__get_db_server(request).execute(request.POST.get('sql'),1000)
            time_consume = int(time.time())-self.stime
            self.__record_operation(request, dbServer,time_consume ,result)
            return [{"dataList":result,"time":format_time(time_consume)}]            
        else:
            return sql_parse   
        
    def query_sql(self, request):
        dbServer = self.__check_user_perms(request,'databases.databases_query_database_server_config')

        if not dbServer:return "您没有权限操作此项"
        
        if dbServer.get('db_rw') not in ["read","r/w"]:return "请勿在主库上面执行查询操作"
        
        sql_parse = self.__check_sql_parse(request, allow_sql=["select","show","desc","explain"],dbname=dbServer.get('db_name'))

        if not isinstance(sql_parse, str):    
            result = self.__get_db_server(request).queryMany(request.POST.get('sql'),1000)
            time_consume = int(time.time())-self.stime
            self.__record_operation(request, dbServer,time_consume ,result)
            return [{"dataList":result,"time":format_time(time_consume)}]
        return sql_parse
            
    
    def binlog_sql(self,request):
        if not  self.__check_user_perms(request,'databases.databases_binlog_database_server_config'):return "您没有权限操作此项"
        result = self.__get_db_server(request).queryAll(sql='show binary logs;')
        binLogList = []
        if isinstance(result,tuple):
            for ds in result[1]:
                binLogList.append(ds[0]) 
        return binLogList
    
    def table_list(self,request):
        if not self.__check_user_perms(request,'databases.databases_query_database_server_config'):return "您没有权限操作此项"
        result = self.__get_db_server(request).queryAll(sql='show tables;')
        grant_tables = self.__check_user_db_tables(request)
        tableList = []
        if isinstance(result,tuple):
            if grant_tables:
                for ds in result[1]:
                    if ds[0] in grant_tables:
                        tableList.append(ds[0])  
            else:               
                for ds in result[1]:
                    tableList.append(ds[0])                      
        return tableList
    
    def table_schema(self,request):
        if not self.__check_user_perms(request,'databases.databases_schema_database_server_config'):return "您没有权限操作此项"
        table_data = {}
        dbInfo = self.__get_db(request)
        dbRbt  = self.__get_db_server(request)
        grant_tables = self.__check_user_db_tables(request)
        if grant_tables and request.POST.get('table_name') not in grant_tables:return "操作的表未授权"
        table_data["schema"] = dbRbt.queryMany(sql="""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_TYPE,ENGINE,VERSION,ROW_FORMAT,
                                                    TABLE_ROWS,concat(round(sum(DATA_LENGTH/1024/1024),2),'MB') AS DATA_LENGTH,
                                                    MAX_DATA_LENGTH,concat(round(sum(INDEX_LENGTH/1024/1024),2),'MB') AS INDEX_LENGTH,
                                                    DATA_FREE,AUTO_INCREMENT,CREATE_TIME,TABLE_COLLATION,TABLE_COMMENT FROM information_schema.TABLES 
                                                    WHERE  TABLE_SCHEMA='{db}' AND TABLE_NAME='{table}';""".format(db=dbInfo.get("db_name"),table=request.POST.get('table_name')),num=1000)
        table_data["index"] = dbRbt.queryMany(sql="""SHOW index FROM `{table}`;""".format(db=dbInfo.get("db_name"),table=request.POST.get('table_name')),num=1000)
        table_data["desc"] = dbRbt.queryOne(sql="""show create table `{table}`;""".format(db=dbInfo.get("db_name"),table=request.POST.get('table_name')),num=1)[1][1]
        return table_data
            
    def parse_sql(self,request):
        if not self.__check_user_perms(request,'databases.databases_binlog_database_server_config'):return "您没有权限操作此项"
        sqlList = []
        try:
            dbServer = self.__get_db(request)
            timeRange =  request.POST.get('binlog_time').split(' - ') 
            conn_setting = {'host': dbServer.get("ip"), 'port': dbServer.get("db_port"), 
                            'user': dbServer.get("db_user"), 'passwd': dbServer.get("db_passwd"),
                            'charset': 'utf8'}
            binlog2sql = Binlog2sql(connection_settings=conn_setting,             
                                    back_interval=1.0, only_schemas=dbServer.get("db_name"),
                                    end_file='', end_pos=0, start_pos=4,
                                    flashback=True,only_tables=request.POST.get('binlog_table',''), 
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
        if not self.__check_user_perms(request,'databases.databases_optimize_database_server_config'):return "您没有权限操作此项"
        dbServer = self.__get_db(request)
        status,result = base.getSQLAdvisor(host=dbServer.get("ip"), user=dbServer.get("db_user"),
                                           passwd=dbServer.get("db_passwd"), dbname=dbServer.get("db_name"), 
                                           sql=request.POST.get('sql'),port=dbServer.get("db_port"))
        return [result]        
    
    def __record_operation(self,request,dbServer,time_consume,result):
        
        if isinstance(result, str):
            record_exec_sql.apply_async((request.user.username,dbServer.get('id'),request.POST.get('sql'),time_consume,1,result),queue='default')
        else:
            record_exec_sql.apply_async((request.user.username,dbServer.get('id'),request.POST.get('sql'),time_consume,0),queue='default')        
        
    def __query_user_db_server(self,request=None):
        if request.user.is_superuser:
            dbList = DataBase_Server_Config.objects.all()      
        else: 
            user_db_list = [ ud.db for ud in Database_User.objects.filter(user=request.user.id) ]
            dbList = [ ds.db_server for ds in Database_Detail.objects.filter(id__in=user_db_list)]
        return dbList

    def recursive_node_to_dict(self,node,request,user_db_server_list):
        json_format = node.to_json()
        children = [self.recursive_node_to_dict(c,request,user_db_server_list) for c in node.get_children()]
        if children:
            json_format['children'] = children
        else:
            json_format['icon'] = 'fa fa-minus-square-o'
        
        #获取业务树下面的数据库服务器    
        if json_format["last_node"] == 1: 
            db_children = []    
            for ds in DataBase_Server_Config.objects.filter(id__in=user_db_server_list,db_business=json_format["id"],db_rw__in=request.query_params.getlist('db_rw')):  
                data = ds.to_tree()
                data["user_id"] = request.user.id
                db_children.append(data)
            json_format['children'] = db_children
            json_format["icon"] = "fa fa-plus-square"
            json_format["last_node"] = 0
            
        return json_format
    
    def business_paths_id_list(self,business):
        tree_list = []
        
        dataList = Business_Tree_Assets.objects.raw("""SELECT id FROM opsmanage_business_assets WHERE tree_id = {tree_id} AND  lft < {lft} AND  rght > {rght} ORDER BY lft ASC;""".format(tree_id=business.tree_id,lft=business.lft,rght=business.rght))
        
        for ds in dataList:
            tree_list.append(ds.id)
            
        tree_list.append(business.id)
        
        return tree_list
       
    def tree(self,request):
        
        user_db_server_list =  [ ds.id for ds in self.__query_user_db_server(request) ] 
        
        if request.user.is_superuser:
            user_business = [ ds.get("db_business") for ds in DataBase_Server_Config.objects.values('db_business').annotate(dcount=Count('db_business')) ] 
                     
        else:    
            user_business = [ ds.get("db_business") for ds in DataBase_Server_Config.objects.filter(id__in=user_db_server_list).values('db_business').annotate(dcount=Count('db_business')) ]
   
        business_list = []

        for business in Business_Tree_Assets.objects.filter(id__in=user_business):
            business_list += self.business_paths_id_list(business)
            
        business_list = list(set(business_list))
        
        business_node = Business_Tree_Assets.objects.filter(id__in=business_list)
        
        root_nodes = cache_tree_children(business_node)
        
        dataList = []
        for n in root_nodes:
            dataList.append(self.recursive_node_to_dict(n,request,user_db_server_list))         
        return dataList          
