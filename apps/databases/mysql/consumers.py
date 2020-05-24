# -*- coding:utf-8 -*-
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from databases.models import *
from utils import base
from libs.sqlparse import sql_parse
from libs.sqlpool import SQLExecute
# from threading import Thread
   
class MySQLWebTerminal(WebsocketConsumer):
    dml_sql = ["INSERT","UPDATE","DELETE"]
    dql_sql = ["SELECT","SHOW","DESC","EXPLAIN"]
    ddl_sql = ["CREATE","DROP","ALTER","TRUNCATE"]     
    
    
    def __init__(self, *args, **kwargs):
        super(MySQLWebTerminal, self).__init__(*args, **kwargs)         
        self.status = True
        self.sql = None
        
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
        
        if dbServer and self.scope["user"].has_perm(perms):
            try:
                user_db = Database_MySQL_User.objects.get(db=db, user=self.scope["user"].id) 
                if base.changeTotimestamp(str(user_db.valid_date)) - int(time.time()) > 0:#判断用户数据权限是否过期
                    return dbServer
            except Exception as ex:  
                self.send(text_data="403。。。。数据库未授权!")    
        
        self.send(text_data="403。。。。数据库未授权!")             
        self.close()       
    

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
                
            if _first_token in allow_sql and sql_type in ["dml", "ddl"]: return True
                     
            return "SQL未授权, 联系管理员授权"
            
        return True 
    
    def connect(self):
           
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        self.accept()

        self.db = self._check_user_perms(self.scope['url_route']['kwargs']['id'])

        if not self.db:
            self.send(text_data="403。。。。数据库未授权!")   
            self.close()        
        try:
            self.sql = SQLExecute(self.db, self) 
        except Exception as ex:    
            self.send(ex.__str__())
            self.close()
                           
        # 创建channels group
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        
             
           
    def receive(self, text_data=None, bytes_data=None):   
        sql_parse = self.__check_sql_parse(text_data, allow_sql=self.dml_sql + self.ddl_sql + self.dql_sql)
        if isinstance(sql_parse, str):
            self.send(sql_parse)
        else:
            rs = self.sql.execute(statement=text_data)
            self.sql.pretty_result(rs) 

                       
        
    def user_message(self, event):
        self.send(text_data=event["text"])      

    def disconnect(self, close_code):
        self.sql.close()
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()
        