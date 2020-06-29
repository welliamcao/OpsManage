# -*- coding:utf-8 -*-
import time
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from databases.models import *
from utils import base
from utils.logger import logger
from libs.redispool import RedisPool
from dao.redis import RedisManage


class RedisWebTerminal(WebsocketConsumer,RedisManage):
   

    def __init__(self, *args, **kwargs):
        super(RedisWebTerminal, self).__init__(*args, **kwargs)         
        self.status = True
        self.db = self.scope['url_route']['kwargs']['id']
        
    def _get_db(self, db):
        try:
            db_info = Database_Redis_Detail.objects.get(id=db)
            dbServer = db_info.db_server.to_connect()      
            dbServer["db_name"] = db_info.db_name
            return  dbServer
        except Exception as ex:
            self.send(text_data="403。。。。数据库未授权!")      
            self.close() 

    def _check_user_perms(self, db, perms='databases.database_query_redis_server_config'):
        
        dbServer = self._get_db(db)    

        if self.scope["user"].is_superuser and dbServer:
            return dbServer
        
        if dbServer and self.scope["user"].has_perm(perms):
            try:
                user_db = Database_Redis_User.objects.get(db=self.db, user=self.scope["user"].id) 
                if base.changeTotimestamp(str(user_db.valid_date)) - int(time.time()) > 0:#判断用户数据权限是否过期
                    return dbServer
            except Exception as ex:  
                self.send(text_data="403。。。。数据库未授权!")    
                
        self.send(text_data="403。。。。数据库未授权!")             
        self.close()       

    def _check_user_db_cmds(self):
        try:     
            userDbServer = Database_Redis_User.objects.get(db=self.db, user=self.scope["user"].id)
            if userDbServer.cmds:return userDbServer.cmds.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库权限失败: {ex}".format(ex=str(ex)))  
            
        return []      

    def _check_sql_parse(self, cmd, allow_cmd):   
        #提取SQL中的表名
        extract_cmds = self._extract_cmds_from_cmd(cmd)   
        
        if extract_cmds in allow_cmd:
            return True        
                          
        #查询用户是不是有授权命令
        grant_cmds = self._check_user_db_cmds()
        
        if extract_cmds in grant_cmds:
            return True
        
        self.send("命令未授权, 联系管理员授权\r\n") 
        self.send(self.redis_pool.prompt())
        return False                                     
    
    def connect(self):
           
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        self.accept()

        dbServer = self._check_user_perms(self.scope['url_route']['kwargs']['id'])

        if not dbServer:
            self.send(text_data="403。。。。数据库未授权!")   
            self.close()        
        
        
        #创建Redis连接
        self.redis_pool = RedisPool(dbServer).start_up()
        
        self.send(self.redis_pool.prompt())
    
           
    def receive(self, text_data=None, bytes_data=None):
        if self._check_sql_parse(text_data,self.get_cmd): 
            result = self.redis_pool.execute(text_data)
            #这里记录用户执行的命令
            self.send(self.redis_pool.format_result(result))
            self.send(self.redis_pool.prompt())

           
        
    def user_message(self, event):
        self.send(text_data=event["text"])      

    def disconnect(self, close_code):    
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.redis_pool.close()
        self.close()
        