#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import time, json
from jinja2 import Template
from databases.models import *
from utils import base
from utils.logger import logger
from .assets import AssetsBase 
from asset.models import *
from datetime import datetime
from service.mysql.mysql_base import MySQLBase
from libs.sqlparse import sql_parse
from utils.mysql.binlog2sql import Binlog2sql
from utils.mysql.const import SQL_PERMISSIONS,SQL_DICT_HTML
from apps.tasks.celery_sql import record_exec_sql, export_table, parse_binlog 
from account.models import User_Async_Task
from django.core.exceptions import PermissionDenied
from dao.base import AppsTree

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

    def __get_db_server_connect(self,dbServer):
        try:
            return MySQLBase(dbServer=dbServer.to_connect())
        except Exception as ex:
            logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
            return ex 

    def sync_db(self,dbServer):
        dataList  = self.__get_db_server_connect(dbServer).get_db_size()
        old_db_list = [ ds.db_name for ds in Database_MySQL_Detail.objects.filter(db_server=dbServer)]
        current_db_list = [ ds.get("db_name") for ds in dataList ]
        for ds in dataList:
            try:
                Database_MySQL_Detail.objects.get_or_create(
                                              db_server=dbServer,
                                              db_name=ds.get("db_name"),
                                              defaults = {
                                                  "db_size": ds.get("size"),
                                                  "total_table": ds.get("total_table")
                                                  }
                                              )
            except Exception as ex:
                logger.error(msg="同步数据库失败: {ex}".format(ex=ex))
        
        del_db_list = list(set(old_db_list).difference(set(current_db_list)))
        
        del_db = Database_MySQL_Detail.objects.filter(db_server=dbServer,db_name__in=del_db_list)

        Database_Table_Detail_Record.objects.filter(db__in= [ ds.id for ds in del_db]).delete() #清除数据库里面表记录
        Database_MySQL_User.objects.filter(db__in= [ ds.id for ds in del_db]).delete() #清除用户数据库里面表记录
        
        del_db.delete() 
        return Database_MySQL_Detail.objects.filter(db_server=dbServer)
    
    def sync_table(self,dbServer,db,dbname):
        dataList  = self.__get_db_server_connect(dbServer).get_db_table_info(dbname)
        current_db_table_list = [ ds.get("table_name") for ds in dataList ]
        old_db_table_list = [ ds.table_name for ds in Database_Table_Detail_Record.objects.filter(db=db) ]
        for ds in dataList:
            try:
                table, created = Database_Table_Detail_Record.objects.get_or_create(
                                              db = db,
                                              table_name = ds.get("table_name"),
                                              defaults = {
                                                  "table_size": ds.get("table_size"),
                                                  "table_row": ds.get("table_rows"),
                                                  "table_engine": ds.get("engine"),
                                                  "collation": ds.get('table_collation'),
                                                  "format": ds.get('row_format'),
                                                  "last_time": int(time.time())
                                              }
                                              )
            except Exception as ex:
                logger.error(msg="写入数据库表信息失败: {ex}".format(ex=ex))

            if created is False:
                try:
                    table.table_size = ds.get("table_size")
                    table.table_row = ds.get("table_rows")
                    table.table_engine = ds.get("engine")
                    table.collation = ds.get('table_collation')
                    table.format = ds.get('row_format')
                    table.last_time = int(time.time())
                    table.save()
                except Exception as ex:
                    logger.error(msg="更新数据库表信息失败: {ex}".format(ex=ex))                
        
        del_db_table_list = list(set(old_db_table_list).difference(set(current_db_table_list))) 
               
        Database_Table_Detail_Record.objects.filter(db=db,table_name__in=del_db_table_list).delete()
                  
        return Database_Table_Detail_Record.objects.filter(db=db)
    
    def get_user_db_tables(self,db,user):
        dataList = []
        try:
            return Database_MySQL_User.objects.get(db=db.id,user=user.id).tables.split(",")
        except:
            pass        
        return dataList
    
    def get_db_dict(self,dbServer, db, user_tables=None):
        js_db_server = dbServer.to_json()
        
        db_table_list = self.__get_db_server_connect(dbServer).get_db_tables(db.db_name)
        table_strs = ''
        for ds in db_table_list:
            
            if len(user_tables) > 0 and ds.get("TABLE_NAME") not in user_tables:continue
            
            table_columns_list = self.__get_db_server_connect(dbServer).get_db_table_columns(db.db_name,ds.get("TABLE_NAME"))
            tr_strs = ''
            
            for ts in table_columns_list:
                tr_str = """<tr>     
                                <td>{COLUMN_NAME}</td>
                                <td>{COLUMN_TYPE}</td>
                                <td>{COLUMN_DEFAULT}</td>
                                <td>{IS_NULLABLE}</td>
                                <td>{EXTRA}</td>
                                <td>{COLUMN_KEY}</td>
                                <td>{COLUMN_COMMENT}</td>
                            </tr>""".format(COLUMN_NAME=ts.get("COLUMN_NAME"),COLUMN_TYPE=ts.get("COLUMN_TYPE"),
                                            COLUMN_DEFAULT=ts.get("COLUMN_DEFAULT"),IS_NULLABLE=ts.get("IS_NULLABLE"),
                                            EXTRA=ts.get("EXTRA"),COLUMN_KEY=ts.get("COLUMN_KEY"),
                                            COLUMN_COMMENT=ts.get("COLUMN_COMMENT"))
                tr_strs = tr_str + tr_strs
            
            table_str = """
                        <table border="1" cellspacing="0" cellpadding="0" align="center">
                        <caption>表名：{TABLE_NAME}  总记录数：{TABLE_ROWS}</caption>
                        <caption>注释：{TABLE_COMMENT}</caption>
                            <tbody>
                                <tr>
                                    <th>字段名</th>
                                    <th>数据类型</th>
                                    <th>默认值</th>
                                    <th>允许非空</th>
                                    <th>自动递增</th>
                                    <th>是否主键</th>
                                    <th>备注</th>
                                </tr> 
                                    {TR_STR}                              
                            </tbody>
                        </table>
                        </br>""".format(TABLE_NAME=ds.get("TABLE_NAME"),TABLE_ROWS=ds.get("TABLE_ROWS"),TABLE_COMMENT=ds.get("TABLE_COMMENT"),TR_STR=tr_strs)
            table_strs = table_str + table_strs
        
        return Template(SQL_DICT_HTML).render(host=js_db_server.get("ip"),
                                             port=js_db_server.get("db_port"),
                                             db_name=db.db_name,
                                             export_time=datetime.now(),
                                             total_tables = len(db_table_list),
                                             dict_data=table_strs) 
    
class DBUser(object):
    def __init__(self):
        super(DBUser,self).__init__() 
        self.user_grants = ["create","drop","alter","truncate","insert","update","delete","select","show","desc","explain","rename"]
    
    def get_user_db(self, user, s_query_params={}, u_query_params={}):
        dataList = []  
        for ds in Database_MySQL_User.objects.filter(user=user.id,**u_query_params):
            try:
                data = Database_MySQL_Detail.objects.get(id=ds.db,**s_query_params).to_json()
                data["username"] = user.username
                data["uid"] = ds.user
                data["user_db_id"] = ds.id
                data["valid_date"] = ds.valid_date
                data["count"] = 1
                data["is_write"] = ds.is_write
                dataList.append(data)
            except Exception as ex: 
                continue               
        return  dataList    
    
    def get_user_db_sql(self, db):
        user_sql_list = []
        if db.sqls:
            user_sql_list = db.sqls.split(",")
        
        dataList = []    
        for k in SQL_PERMISSIONS.keys():
            count = 0
            if k in user_sql_list:count = 1
            dataList.append({"value":k,"desc":SQL_PERMISSIONS[k].get("desc"),"count":count})   
        
        return dataList
    
    def get_server_all_db(self, db_server, user):
        dataList = []
        for ds in Database_MySQL_Detail.objects.filter(db_server=db_server):
            data = ds.to_json()
            try:
                user_db = Database_MySQL_User.objects.get(db=ds.id,user=user.id)
                data["count"] = 1
                data["user_db_id"] = user_db.id
                data["uid"] = user_db.user
                data["valid_date"] = user_db.valid_date
                data["is_write"] = user_db.is_write
                data["username"] = user.username                
            except:
                pass
            dataList.append(data)
        return dataList        
    
    def get_user_server_db(self, db_server, user):
        dataList = []
        for ds in Database_MySQL_Detail.objects.filter(db_server=db_server):
            try:
                user_db = Database_MySQL_User.objects.get(db=ds.id,user=user.id)
            except:
                continue
            data = ds.to_json()
            data["uid"] = user_db.user
            data["count"] = 1
            data["valid_date"] = user_db.valid_date
            data["username"] = user.username
            data["user_db_id"] = user_db.id
            data["is_write"] = user_db.is_write
            dataList.append(data)
        return dataList
    
    
    def update_user_server_db(self, request, db_server, user):       
        all_user_db_list = [ ds.db for ds in Database_MySQL_User.objects.filter(db__in=[ ds.id for ds in db_server.databases.all()],user=user.id)]

        update_user_db_list = [ int(ds) for ds in request.data.getlist('dbIds') ]

        update_list = list(set(update_user_db_list).difference(set(all_user_db_list)))        
        
        for dbIds in update_list:
            obj, created = Database_MySQL_User.objects.update_or_create(db=dbIds, user=user.id,
                                                                  valid_date = base.getDayAfter(int(request.POST.get('valid_date',1)),format='%Y-%m-%d %H:%M:%S'))  
        
        #更新已有记录
        Database_MySQL_User.objects.filter(db__in=update_user_db_list, user=user.id).update(valid_date = base.getDayAfter(int(request.POST.get('valid_date',1)),format='%Y-%m-%d %H:%M:%S'), 
                                                                                      is_write = int(request.POST.get('is_write',0))) 
                
              
        
             

class DBManage(AssetsBase):  
    dml_sql = ["INSERT","UPDATE","DELETE"]
    dql_sql = ["SELECT","DESC","EXPLAIN"]
    ddl_sql = ["CREATE","DROP","ALTER","TRUNCATE"]
    
    def __init__(self):
        super(DBManage,self).__init__() 
        
    def allowcator(self,sub,request):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(request)
        else:
            logger.error(msg="DBManage没有{sub}方法".format(sub=sub))       
            return "参数错误" 
    
    def __check_user_perms(self,request,perms='databases.database_read_database_server_config'):
        
        dbServer = self.__get_db(request)

        if request.user.is_superuser and dbServer:
            return dbServer
        
        if  dbServer and request.user.has_perm(perms):
            try:
                user_db = Database_MySQL_User.objects.get(db=request.POST.get('db'),user=request.user.id) 
                if base.changeTotimestamp(str(user_db.valid_date)) - int(time.time()) > 0:#判断用户数据权限是否过期
                    return dbServer
            except Exception as ex:
                logger.warn(msg="查询用户数据库信息失败: {ex}".format(ex=str(ex)))  
                 
        raise PermissionDenied  

    def __check_user_db_tables(self,request):
        try:     
            userDbServer = Database_MySQL_User.objects.get(user=request.user.id,db=request.POST.get('db'))
            if userDbServer.tables:return userDbServer.tables.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库表信息失败: {ex}".format(ex=str(ex)))  
            
        return []    
    
    def __check_user_db_sql(self,request):
        try:     
            userDbServer = Database_MySQL_User.objects.get(user=request.user.id,db=request.POST.get('db'))
            if userDbServer.sqls:return userDbServer.sqls.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库权限失败: {ex}".format(ex=str(ex)))  
            
        return []              
    
    def __extract_keyword_from_sql(self, sql):
        return sql_parse.extract_sql_keyword(sql)
    
    def __extract_table_name_from_sql(self ,sql):
        schema = []
        tables = []
        for ds in sql_parse.extract_tables(sql):

            if ds.schema and ds.schema not in schema: 
                schema.append(ds.schema)
                
            if ds.name and ds.name not in tables: 
                tables.append(ds.name)
                
        if len(schema) > 0:
            return "不支持跨数据库类型SQL" 
        
        return tables
    
    def __check_sql_parse(self, request, allow_sql, sql, read_only=True):                
        #查询用户是不是有授权表
        grant_tables = self.__check_user_db_tables(request)
        
        #提取SQL中的表名
        extract_table = self.__extract_table_name_from_sql(sql)
        
        if isinstance(extract_table, list) and grant_tables:

            for tb in extract_table:
                if tb not in grant_tables:
                    return "操作的表未授权" 
                    
        elif isinstance(extract_table, str):
            return extract_table
                
        else:#如果提交的SQL里面没有包含授权的表，就检查SQL类型是否授权
            #查询用户授权的SQL类型
            grant_sql = self.__check_user_db_sql(request)
            
            sql_type, _first_token , keywords = self.__extract_keyword_from_sql(sql)

            if len(keywords) > 1:
                if keywords[0] + '_'  + keywords[1] in grant_sql:
                    return True
#             print(_first_token, keywords, grant_sql, allow_sql)
            
            if read_only and _first_token == 'SELECT' and 'INTO' in keywords:return "当前操作，不允许写入"
            
            if _first_token in allow_sql: return True
                     
            return "SQL未授权, 联系管理员授权"
            
        return True 
                  
    
    def __get_db(self,request):
        try:
            db_info = Database_MySQL_Detail.objects.get(id=self.change(request.POST.get('db')))
            dbServer = db_info.db_server.to_connect()      
            dbServer["db_name"] = db_info.db_name
            return  dbServer
        except Exception as ex:
            logger.error(msg="获取DB实例失败: {ex}".format(ex=ex))       
            raise PermissionDenied   
                                   
    
    def __get_db_server(self,dbServer):
        try:
            return MySQLBase(dbServer=dbServer)
        except Exception as ex:
            logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
            return ex          
    
    def exec_sql(self, request):
        dbServer = self.__check_user_perms(request,'databases.database_dml_database_server_config')
        
        result_list = []
        try:
            sql_list = request.POST.get('sql').lower().split(";")
        except Exception as ex:
            logger.error(msg="解析SQL失败: {ex}".format(ex=ex))
            return '解析SQL失败'
        
        time_consume = 0
        for sql in sql_list:
            stime = int(time.time()) 
            sql = sql.strip('\n') + ';'
            sql_parse = self.__check_sql_parse(request, sql=sql, allow_sql=self.dml_sql + self.ddl_sql + self.dql_sql, read_only=False)

            if not isinstance(sql_parse, str):
                result = self.__get_db_server(dbServer).execute(sql, 1000)
                if not isinstance(result, str):
                    time_consume = int(time.time()) - stime
                    result_list += [{"sql": sql, "dataList": result, "time": base.format_time(time_consume)}]
                else:
                    result_list += [{"sql": sql, "msg": result, "time": 0}]
                self.__record_operation(request.user.username, request.POST.get('db'), time_consume, result, sql)
            else:
                result_list += [{"sql": sql, "msg": sql_parse}]
                
        return result_list        
        
    def query_sql(self, request):
        dbServer = self.__check_user_perms(request,'databases.database_query_database_server_config')
        
        if dbServer.get('db_rw') not in ["read", "r/w"]: return "请勿在主库上面执行查询操作"
        
        result_list = []
        try:
            sql_list = request.POST.get('sql').lower().split(";")
        except Exception as ex:
            logger.error(msg="解析SQL失败: {ex}".format(ex=ex))
            return '解析SQL失败'
        
        time_consume = 0
        for sql in sql_list:
            stime = int(time.time()) 
            sql = sql.strip('\n') + ';'
            sql_parse = self.__check_sql_parse(request, sql=sql, allow_sql=self.dql_sql, read_only=True)
            if not isinstance(sql_parse, str):
                result = self.__get_db_server(dbServer).queryMany(sql, 1000)
                if not isinstance(result, str):
                    time_consume = int(time.time()) - stime
                    result_list += [{"sql": sql, "dataList": result, "time": base.format_time(time_consume)}]
                else:
                    result_list += [{"sql": sql, "msg": result, "time": 0}]
                self.__record_operation(request.user.username, request.POST.get('db'), time_consume, result, sql)    
            else:
                result_list += [{"sql": sql, "msg": sql_parse, "time": 0}]
                
        return result_list
            
    
    def binlog_sql(self,request):
        dbServer =  self.__check_user_perms(request,'databases.database_binlog_database_server_config')
        result = self.__get_db_server(dbServer).queryAll(sql='show binary logs;')
        binLogList = []
        if isinstance(result,tuple):
            for ds in result[1]:
                binLogList.append(ds[0]) 
        return binLogList
    
    def table_list(self,request):
        dbServer = self.__check_user_perms(request,'databases.database_query_database_server_config')
        result = self.__get_db_server(dbServer).queryAll(sql='show tables;')
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
        dbServer = self.__check_user_perms(request,'databases.database_schema_database_server_config')
        table_data = {}
        database  = self.__get_db_server(dbServer)
        grant_tables = self.__check_user_db_tables(request)
        if grant_tables and request.POST.get('table_name') not in grant_tables:return "操作的表未授权"
        table_data["schema"] = database.get_table_schema( dbServer.get("db_name"), request.POST.get('table_name'))
        table_data["index"] = database.get_table_index(request.POST.get('table_name'))
        table_data["desc"] = database.get_table_desc(request.POST.get('table_name'))[1]
        return table_data
            
    def parse_sql(self,request):
        flashback = False
        dbServer = self.__check_user_perms(request,'databases.database_binlog_database_server_config')
        sqlList = []
        try:
            timeRange =  request.POST.get('binlog_time').split(' - ') 
            if int(request.POST.get('flashback')) == 1: flashback = True            
            conn_setting = {'host': dbServer.get("ip"), 'port': dbServer.get("db_port"), 
                            'user': dbServer.get("db_user"), 'passwd': dbServer.get("db_passwd"),
                            'charset': 'utf8'}
            binlog2sql = Binlog2sql(connection_settings=conn_setting,             
                                    back_interval=1.0, only_schemas=dbServer.get("db_name"),
                                    end_file='', end_pos=0, start_pos=4,
                                    flashback=flashback,only_tables=request.POST.get('binlog_table',''), 
                                    no_pk=False, only_dml=True,stop_never=False, 
                                    sql_type=['INSERT', 'UPDATE', 'DELETE'], 
                                    start_file=request.POST.get('binlog_db_file'), 
                                    start_time=timeRange[0], 
                                    stop_time=timeRange[1],)
            if int(request.POST.get('async',0)) == 1:#如果开启异步导出，执行下面流程
                
                try:
                    args = {
                            "id":request.POST.get('db'),
                            "user":request.user.name,
                            "value":dbServer.get('db_name')+ '|' + request.POST.get('binlog_db_file'),
                            "vars":request.POST.get('binlog_table')
                        }
                except Exception as ex:
                    logger.error(msg="binglog解析失败: {ex}".format(ex=ex)) 
                    return "参数错误"
                #通过参数计算唯一token，防止提交大量重复任务
                token_args = args.copy()
                token_args.pop("vars")
                token_args.pop("value")
                 
                #去除不必要参数
                args.pop("id")
                args.pop("user")
        #         
                token = base.makeToken(str(token_args).encode('utf-8'))
                binlog = binlog2sql.__dict__.copy()
                for k in list(binlog.keys()):
                    if k in ["connection","server_id","eof_file","eof_pos"]:
                        binlog.pop(k)
                return self.__create_aysnc_task(request, token, args, 2, binlog)                
                
            sqlList = binlog2sql.process_binlog()   
        except Exception as ex:
            logger.error(msg="binglog解析失败: {ex}".format(ex=ex)) 
            return "binglog解析失败: {ex}".format(ex=str(ex))
        return sqlList
    
    def optimize_sql(self,request):
        dbServer = self.__check_user_perms(request,'databases.database_optimize_database_server_config')
        status,result = base.getSQLAdvisor(host=dbServer.get("ip"), user=dbServer.get("db_user"),
                                           passwd=dbServer.get("db_passwd"), dbname=dbServer.get("db_name"), 
                                           sql=request.POST.get('sql'),port=dbServer.get("db_port"))
        return [result]        
            
    
    def dump_table(self,request):
        dbServer = self.__check_user_perms(request,'databases.database_dumptable_database_server_config')
        try:
            args = {
                    "id":request.POST.get('db'),
                    "user":request.user.name,
                    "value":dbServer.get('db_name')+ '|' + request.POST.get('table_name'),
                    "email":request.POST.get('email'), 
                    "vars":request.POST.get('where')
                }
        except Exception as ex:
            logger.error(msg="导出表数据失败: {ex}".format(ex=ex)) 
            return "参数错误"
        #通过参数计算唯一token，防止提交大量重复任务
        token_args = args.copy()
        token_args.pop("vars")
        token_args.pop("email")
         
        #去除不必要参数
        args.pop("id")
        args.pop("user")
        
#         
        token = base.makeToken(str(token_args).encode('utf-8'))
        
        return self.__create_aysnc_task(request, token, args, 1)

    
    def __create_aysnc_task(self, request, token, args, type, binlog=None):    
        if User_Async_Task.objects.filter(token=token, user=request.user.id, type=type, status=0).count() == 0:
            try:
                task = User_Async_Task.objects.create(
                        task_name = request.POST.get('task_name'), 
                        extra_id = request.POST.get('db'), 
                        task_id = int(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))),
                        user = request.user.id,
                        type = type,
                        status = 0,
                        args = json.dumps(args),
                        token =token
                    )
            except Exception as ex:
                return str(ex)
            if type == 1:
                c_task = export_table.apply_async((task.task_id,), queue='default')
            elif type == 2:
                c_task = parse_binlog.apply_async((task.task_id, binlog), queue='default')  
            else:
                task.delete()
                return "任务不支持"  
            
            task.ctk = c_task.id
            task.save()

        else:
            return "有相同任务正在进行，请勿重复提交"        
        
        
    def __record_operation(self, username, db, time_consume, result, sql):
        if isinstance(result, str):
            record_exec_sql.apply_async((username, db, sql, time_consume, 0, 1, result), queue='default')
        else:
            record_exec_sql.apply_async((username, db, sql, time_consume, result[0], 0),queue='default')        
                
    def tree(self,request):
        return AppsTree(Business_Tree_Assets,
                        DataBase_MySQL_Server_Config, 
                        Database_MySQL_User, 
                        Database_MySQL_Detail,
                        request).db_tree()         
