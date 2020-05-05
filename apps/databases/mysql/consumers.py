# -*- coding:utf-8 -*-
import time, paramiko, os
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from utils.logger import logger
from OpsManage.settings import config
from databases.models import *
from utils import base
from utils.sqlparse import sql_parse
# from threading import Thread
import threading

class WebTerminalBridge(threading.Thread):
    def __init__(self, websocket, filter_chars=None):
        super(WebTerminalBridge, self).__init__()
        self.websocket = websocket
        self._stop_event = threading.Event()
        self.filter_chars = filter_chars
 
    def stop(self):
        self._stop_event.set()
 
    def run(self):
        while not self._stop_event.is_set():
            try:
                data = self.websocket.chan.recv(1024)
                if data:
                    str_data = bytes.decode(data)
                    self.send_msg(str_data)
            except Exception as ex:
                pass
        self.websocket.ssh.close()
        self.stop()
 
    def send_msg(self, msg): 
        if self.filter_chars in msg:
            return 
               
        async_to_sync(self.websocket.channel_layer.group_send)(
            self.websocket.group_name,
            {
                "type": "user.message",
                "text": msg
            },
        )
   
class MySQLWebTerminal(WebsocketConsumer):
    dml_sql = ["INSERT","UPDATE","DELETE"]
    dql_sql = ["SELECT","SHOW","DESC","EXPLAIN"]
    ddl_sql = ["CREATE","DROP","ALTER","TRUNCATE"]     
    
    
    def __init__(self, *args, **kwargs):
        super(MySQLWebTerminal, self).__init__(*args, **kwargs)         
        self.status = True
        self.sql = ''
        
    def _get_db(self,db):
        try:
            db_info = Database_MySQL_Detail.objects.get(id=db)
            dbServer = db_info.db_server.to_connect()      
            dbServer["db_name"] = db_info.db_name
            return  dbServer
        except Exception as ex:
            self.send(text_data="403。。。。数据库未授权!")      
            self.close()  
    
    def _check_user_perms(self, db, perms='databases.database_webterminal_database_server_config'):
        
        dbServer = self._get_db(db)

        if self.scope["user"].is_superuser and dbServer:
            return dbServer
        
        if  dbServer and self.scope["user"].has_perm(perms):
            try:
                user_db = Database_MySQL_User.objects.get(db=db, user=self.scope["user"].id) 
                if base.changeTotimestamp(str(user_db.valid_date)) - int(time.time()) > 0:#判断用户数据权限是否过期
                    return dbServer
            except Exception as ex:  
                self.send(text_data="403。。。。数据库未授权!")    
        
        self.send(text_data="403。。。。数据库未授权!")             
        self.close()       
    
    def _build_mysql_conn_cmd(self,dbServer):
        return """clear;/usr/bin/mysql --prompt="\\u@\\h : [\\d] \\r:\\m:\\s> " -A -D {database} -h {host} -u{user} -p{password} -P {port} ;exit;exit\r""".format(host = dbServer.get('ip'), 
                                                                                                 user = dbServer.get('db_user'),
                                                                                                 password = dbServer.get('db_passwd'), 
                                                                                                 database = dbServer.get('db_name'),
                                                                                                 port = dbServer.get('db_port'))


    def _check_user_db_sql(self, db):
        try:     
            userDbServer = Database_MySQL_User.objects.get(db=db, user=self.scope["user"].id)
            if userDbServer.sqls:return userDbServer.sqls.split(",")
        except Exception as ex:
            pass 
        return []          

    def _check_user_db_tables(self, db):
        try:     
            userDbServer = Database_MySQL_User.objects.get(db=db, user=self.scope["user"].id)
            if userDbServer.tables:return userDbServer.tables.split(",")
        except Exception as ex:
            pass  
        return []  

    def _extract_keyword_from_sql(self, sql):
        return sql_parse.extract_sql_keyword(sql)
    
    def _extract_table_name_from_sql(self ,sql):
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

    def __check_sql_parse(self, sql,  allow_sql):                
        #查询用户是不是有授权表
        grant_tables = self._check_user_db_tables(self.scope['url_route']['kwargs']['id'])
        
        #提取SQL中的表名
        extract_table = self._extract_table_name_from_sql(sql)
        
        if isinstance(extract_table, list) and grant_tables:

            for tb in extract_table:
                if tb not in grant_tables:
                    return "操作的表未授权" 
                    
        elif isinstance(extract_table, str):
            return extract_table
                
        else:#如果提交的SQL里面没有包含授权的表，就检查SQL类型是否授权
            #查询用户授权的SQL类型
            grant_sql = self._check_user_db_sql(self.scope['url_route']['kwargs']['id'])
            
            sql_type, _first_token , keywords = self._extract_keyword_from_sql(sql)

            if len(keywords) > 1:
                if keywords[0] + '_'  + keywords[1] in grant_sql:
                    return True
#             print(_first_token, keywords, grant_sql, allow_sql)
        
            if _first_token in allow_sql: return True
                     
            return "SQL未授权, 联系管理员授权"
            
        return True 
    
    def connect(self):
           
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        self.accept()

        self.db = self._check_user_perms(self.scope['url_route']['kwargs']['id'])

        if not self.db:
            self.send(text_data="403。。。。数据库未授权!")   
            self.close()        
         
        mysql_login_command = self._build_mysql_conn_cmd(self.db)     
    
        try:
            pkey = None
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 允许连接不在know_hosts文件中的主机
             
            if os.path.exists(config.get('ssh_proxy', 'public_key')):
                pkey = paramiko.RSAKey.from_private_key_file(config.get('ssh_proxy', 'public_key'))
                 
            self.ssh.connect(
                             hostname = config.get('ssh_proxy', 'host'), 
                             port=int(config.get('ssh_proxy', 'port')), 
                             username=config.get('ssh_proxy', 'username'),
                             password=config.get('ssh_proxy', 'password'),
                             pkey = pkey,
                             )
        except Exception as ex:
            self.send(text_data="MySQL代理服务器连接失败: {ex}".format(ex=ex))   
            self.close()                         
        # 创建channels group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        
        # 打开一个ssh通道并建立连接
        self.chan = self.ssh.invoke_shell(term='xterm', width=150, height=30)
        self.chan.settimeout(0)            
        self.ssh_bridge = WebTerminalBridge(self, mysql_login_command)
        self.ssh_bridge.setDaemon(True)
        self.ssh_bridge.start()
        
        #发送MySQL登陆命令
        self.chan.send(mysql_login_command)
        time.sleep(0.5)
        self.send("\033[33m \r\nWelcome to MySQL web terminal. Input exit or quit to close terminal. \r\n \033[0m") 
             
           
    def receive(self, text_data=None, bytes_data=None):   
        if  text_data != '\r':
            self.sql += text_data 
        else:
            self._check_sql(text_data)

        if self.status:  
            self.chan.send(text_data)          
    
    
    def _check_sql(self, text_data):
        if len(self.sql) >= 2:
            if text_data == '\r' and (self.sql[-1]==';' or self.sql[-2:]=='\G'):              
                sql_parse = self.__check_sql_parse(self.sql, self.dml_sql + self.ddl_sql + self.dql_sql)  
                try:
                    if isinstance(sql_parse, str):
                        self.status = False
                        self.send('\r\n\033[31m ' + sql_parse +"") 
                        self.send('\r\n\033[31m 终端关闭......\033[0m') 
                        self.disconnect(1000)
                    #else:
                        #记录通过的SQL
                        #print('sql: ',self.sql) 
                except Exception as ex:
                    pass
                finally:
                    self.sql = ''
            elif text_data == '\r':         
                self.sql = self.sql + ' ' 


                       
        
    def user_message(self, event):
        self.send(text_data=event["text"])      

    def disconnect(self, close_code):
        self.ssh_bridge.stop()       
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()
        