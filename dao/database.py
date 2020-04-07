#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import time
from jinja2 import Template
from databases.models import *
from utils.logger import logger
from .assets import AssetsBase 
from asset.models import *
from datetime import datetime
from dao.base import MySQLPool
from utils import base
from utils.mysql.binlog2sql import Binlog2sql
from utils.mysql.const import SQL_PERMISSIONS,SQL_DICT_HTML
from apps.tasks.celery_sql import record_exec_sql
from django.db.models import Count
from mptt.templatetags.mptt_tags import cache_tree_children  
from utils.base import getDayAfter

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

    def __get_db_server_connect(self,dbServer):
        try:
            return MySQLPool(dbServer=dbServer.to_connect())
        except Exception as ex:
            logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
            return ex 

    def sync_db(self,dbServer):
        dataList  = self.__get_db_server_connect(dbServer).get_db_size()
        old_db_list = [ ds.db_name for ds in Database_Detail.objects.filter(db_server=dbServer)]
        current_db_list = [ ds.get("db_name") for ds in dataList ]
        for ds in dataList:
            try:
                Database_Detail.objects.get_or_create(
                                              db_server=dbServer,
                                              db_name=ds.get("db_name"),
                                              db_size=ds.get("size"),
                                              total_table = ds.get("total_table")
                                              )
            except Exception as ex:
                logger.error(msg="同步数据库失败: {ex}".format(ex=ex))
        
        del_db_list = list(set(old_db_list).difference(set(current_db_list)))
        
        del_db = Database_Detail.objects.filter(db_server=dbServer,db_name__in=del_db_list)

        Database_Table_Detail_Record.objects.filter(db__in= [ ds.id for ds in del_db]).delete() #清除数据库里面表记录
        Database_User.objects.filter(db__in= [ ds.id for ds in del_db]).delete() #清除用户数据库里面表记录
        
        del_db.delete() 
        return Database_Detail.objects.filter(db_server=dbServer)
    
    def sync_table(self,dbServer,db,dbname):
        dataList  = self.__get_db_server_connect(dbServer).get_db_table_info(dbname)
        current_db_table_list = [ ds.get("table_name") for ds in dataList ]
        old_db_table_list = [ ds.table_name for ds in Database_Table_Detail_Record.objects.filter(db=db)]
        for ds in dataList:
            try:
                Database_Table_Detail_Record.objects.get_or_create(
                                              db=db,
                                              table_name=ds.get("table_name"),
                                              table_size=ds.get("table_size"),
                                              table_row = ds.get("table_rows"),
                                              last_time = int(time.time())
                                              )
            except Exception as ex:
                logger.error(msg="同步数据库失败: {ex}".format(ex=ex))
        
        del_db_table_list = list(set(old_db_table_list).difference(set(current_db_table_list))) 
               
        Database_Table_Detail_Record.objects.filter(db=db,table_name__in=del_db_table_list).delete()
                  
        return Database_Table_Detail_Record.objects.filter(db=db)
    
    def get_user_db_tables(self,db,user):
        dataList = []
        try:
            return Database_User.objects.get(db=db.id,user=user.id).tables.split(",")
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
        for ds in Database_User.objects.filter(user=user.id,**u_query_params):
            try:
                data = Database_Detail.objects.get(id=ds.db,**s_query_params).to_json()
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
        for ds in Database_Detail.objects.filter(db_server=db_server):
            data = ds.to_json()
            try:
                user_db = Database_User.objects.get(db=ds.id,user=user.id)
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
        for ds in Database_Detail.objects.filter(db_server=db_server):
            try:
                user_db = Database_User.objects.get(db=ds.id,user=user.id)
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
        all_user_db_list = [ ds.db for ds in Database_User.objects.filter(db__in=[ ds.id for ds in db_server.databases.all()],user=user.id)]

        update_user_db_list = [ int(ds) for ds in request.data.getlist('dbIds') ]

        update_list = list(set(update_user_db_list).difference(set(all_user_db_list)))        
        
        for dbIds in update_list:
            obj, created = Database_User.objects.update_or_create(db=dbIds, user=user.id,
                                                                  valid_date = getDayAfter(int(request.POST.get('valid_date',1)),format='%Y-%m-%d %H:%M:%S'))  
        
        #更新已有记录
        Database_User.objects.filter(db__in=update_user_db_list, user=user.id).update(valid_date = getDayAfter(int(request.POST.get('valid_date',1)),format='%Y-%m-%d %H:%M:%S'), 
                                                                                      is_write = int(request.POST.get('is_write',0))) 
                
              
        
             

class DBManage(AssetsBase):  
    dml_sql = ["INSERT","UPDATE","DELETE"]
    dql_sql = ["SELECT","SHOW","DESC","EXPLAIN"]
    ddl_sql = ["CREATE","DROP","ALTER","TRUNCATE"]
    
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
    
    def __check_user_perms(self,request,perms='databases.database_read_database_server_config'):
        
        dbServer = self.__get_db(request)

        if request.user.is_superuser and dbServer:
            return dbServer
        
        if  dbServer and request.user.has_perm(perms):
            try:
                user_db = Database_User.objects.get(db=request.POST.get('db'),user=request.user.id) 
                if base.changeTotimestamp(str(user_db.valid_date)) - int(time.time()) > 0:#判断用户数据权限是否过期
                    return dbServer
            except Exception as ex:
                logger.warn(msg="查询用户数据库信息失败: {ex}".format(ex=str(ex)))  
                return False    
            
        return False

    def __check_user_db_tables(self,request):
        try:     
            userDbServer = Database_User.objects.get(user=request.user.id,db=request.POST.get('db'))
            if userDbServer.tables:return userDbServer.tables.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库表信息失败: {ex}".format(ex=str(ex)))  
            
        return []    
    
    def __check_user_db_sql(self,request):
        try:     
            userDbServer = Database_User.objects.get(user=request.user.id,db=request.POST.get('db'))
            if userDbServer.sqls:return userDbServer.sqls.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库权限失败: {ex}".format(ex=str(ex)))  
            
        return []              
    
    def __check_sql_parse(self,request, allow_sql, dbname):
        try:
            sql = request.POST.get('sql').split(' ')
            sqlCmd,sqlCmds = sql[0].upper(),(sql[0]+'_'+sql[1]).upper().replace(";","")
        except Exception as ex:
            logger.error(msg="解析SQL失败: {ex}".format(ex=ex)) 
            return '解析SQL失败'        
        
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
        else:#如果提交的SQL里面没有包含授权的表，就检查SQL类型是否授权
            #查询用户授权的SQL类型
            grant_sql = self.__check_user_db_sql(request)
            
            if sqlCmd.upper() in grant_sql or sqlCmds in grant_sql:return True
            
            if sqlCmd not in allow_sql: return 'SQL类型不支持'            
            
            return "SQL未授权, 联系管理员授权"
            
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
        
        dbServer = self.__check_user_perms(request,'databases.database_dml_database_server_config')
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
        dbServer = self.__check_user_perms(request,'databases.database_query_database_server_config')

        if not dbServer:return "您没有权限操作此项"
        
        if dbServer.get('db_rw') not in ["read","r/w"]:return "请勿在主库上面执行查询操作"
        
        sql_parse = self.__check_sql_parse(request, allow_sql=self.dql_sql,dbname=dbServer.get('db_name'))
        
        if not isinstance(sql_parse, str):    
            result = self.__get_db_server(request).queryMany(request.POST.get('sql'),1000)
            time_consume = int(time.time())-self.stime
            self.__record_operation(request, dbServer,time_consume ,result)
            return [{"dataList":result,"time":format_time(time_consume)}]
        return sql_parse
            
    
    def binlog_sql(self,request):
        if not  self.__check_user_perms(request,'databases.database_binlog_database_server_config'):return "您没有权限操作此项"
        result = self.__get_db_server(request).queryAll(sql='show binary logs;')
        binLogList = []
        if isinstance(result,tuple):
            for ds in result[1]:
                binLogList.append(ds[0]) 
        return binLogList
    
    def table_list(self,request):
        if not self.__check_user_perms(request,'databases.database_query_database_server_config'):return "您没有权限操作此项"
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
        if not self.__check_user_perms(request,'databases.database_schema_database_server_config'):return "您没有权限操作此项"
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
        if not self.__check_user_perms(request,'databases.database_binlog_database_server_config'):return "您没有权限操作此项"
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
        if not self.__check_user_perms(request,'databases.database_optimize_database_server_config'):return "您没有权限操作此项"
        dbServer = self.__get_db(request)
        status,result = base.getSQLAdvisor(host=dbServer.get("ip"), user=dbServer.get("db_user"),
                                           passwd=dbServer.get("db_passwd"), dbname=dbServer.get("db_name"), 
                                           sql=request.POST.get('sql'),port=dbServer.get("db_port"))
        return [result]        
    
        
    def __record_operation(self,request,dbServer,time_consume,result):
        if isinstance(result, str):
            record_exec_sql.apply_async((request.user.username,request.POST.get('db'), request.POST.get('sql'), time_consume, 1,result), queue='default')
        else:
            record_exec_sql.apply_async((request.user.username,request.POST.get('db'), request.POST.get('sql'), time_consume, result[0], 0),queue='default')        
        
    def __query_user_db_server(self,request=None):
        if request.user.is_superuser:
            dbList = DataBase_Server_Config.objects.all()      
        else: 
            user_db_list = [ ud.db for ud in Database_User.objects.filter(user=request.user.id) ]

            dbLists = [ ds.db_server for ds in Database_Detail.objects.filter(id__in=user_db_list) ]

            dbList = list(dict.fromkeys(dbLists)) #去除重复
            
        return dbList

    def recursive_node_to_dict(self, node, request, user_db_server_list):
        json_format = node.to_json()
        children = [self.recursive_node_to_dict(c, request, user_db_server_list) for c in node.get_children()]
        if children:
            json_format['children'] = children
        else:
            json_format['icon'] = 'fa fa-minus-square-o'
        
        #获取业务树下面的数据库服务器    
        if json_format["last_node"] == 1: 
            db_children = []    
            for ds in DataBase_Server_Config.objects.filter(id__in=user_db_server_list, db_business=json_format["id"], db_rw__in=request.query_params.getlist('db_rw')):  
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
            
            dataList.append(self.recursive_node_to_dict(n, request, user_db_server_list))   
                  
        return dataList          
