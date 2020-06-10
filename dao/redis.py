#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import time, json
from databases.models import *
from utils import base
from utils.logger import logger
from .assets import AssetsBase 
from asset.models import *
from service.redis.redis_base import RedisBase
from utils.redis.const import CMD_PERMISSIONS
from account.models import User_Async_Task
from django.core.exceptions import PermissionDenied
from dao.base import AppsTree

class RedisConfig(AssetsBase):
    def __init__(self):
        super(RedisConfig,self).__init__() 
        
    def allowcator(self,sub,args):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args)
        else:
            logger.error(msg="RedisConfig没有{sub}方法".format(sub=sub))       
            return "参数错误"      

    def __get_db_server_connect(self,dbServer):
        try:
            return RedisBase(dbServer=dbServer.to_connect())
        except Exception as ex:
            logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
            return ex 

    def sync_db(self,dbServer):
        data  = self.__get_db_server_connect(dbServer).get_db_size()
        old_db_list = [ ds.db_name for ds in Database_Redis_Detail.objects.filter(db_server=dbServer)]
        current_db_list = [ ds for ds in data.keys() ]
        for k,v in data.items():
            try:
                detail, created = Database_Redis_Detail.objects.get_or_create(
                                              db_server = dbServer,
                                              db_name = k,
                                              defaults = {
                                                  "total_keys": v.get("keys"),
                                                  "expires": v.get("expires")                                                  
                                                  }
                                              )
            except Exception as ex:
                logger.error(msg="同步数据库失败: {ex}".format(ex=ex))
            
            if detail:
                detail.total_keys = v.get("keys")
                detail.expires = v.get("expires")
                detail.save()
            
        del_db_list = list(set(old_db_list).difference(set(current_db_list)))
        
        del_db = Database_Redis_Detail.objects.filter(db_server=dbServer,db_name__in=del_db_list)

        Database_Redis_User.objects.filter(db__in= [ ds.id for ds in del_db]).delete() #清除用户数据库里面表记录
        
        del_db.delete() 
        return Database_Redis_Detail.objects.filter(db_server=dbServer)
    
    

class RedisUser(object):
    def __init__(self):
        super(RedisUser,self).__init__() 
        
    
    def get_user_db(self, user, s_query_params={}, u_query_params={}):
        dataList = []  
        for ds in Database_Redis_User.objects.filter(user=user.id,**u_query_params):
            try:
                data = Database_Redis_Detail.objects.get(id=ds.db,**s_query_params).to_json()
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
        if db.cmds:
            user_sql_list = db.cmds.split(",")
        
        dataList = []    
        for k in CMD_PERMISSIONS.keys():
            count = 0
            if k in user_sql_list:count = 1
            dataList.append({"value":k,"desc":k + " - " +CMD_PERMISSIONS[k].get("desc"),"count":count})   
        
        return dataList
    
    def get_server_all_db(self, db_server, user):
        dataList = []
        for ds in Database_Redis_Detail.objects.filter(db_server=db_server):
            data = ds.to_json()
            try:
                user_db = Database_Redis_User.objects.get(db=ds.id,user=user.id)
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
        for ds in Database_Redis_Detail.objects.filter(db_server=db_server):
            try:
                user_db = Database_Redis_User.objects.get(db=ds.id,user=user.id)
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
        all_user_db_list = [ ds.db for ds in Database_Redis_User.objects.filter(db__in=[ ds.id for ds in db_server.redis_server.all()],user=user.id)]

        update_user_db_list = [ int(ds) for ds in request.data.getlist('dbIds') ]

        update_list = list(set(update_user_db_list).difference(set(all_user_db_list)))        
        
        for dbIds in update_list:
            obj, created = Database_Redis_User.objects.update_or_create(db=dbIds, user=user.id,
                                                                  valid_date = base.getDayAfter(int(request.POST.get('valid_date',1)),format='%Y-%m-%d %H:%M:%S'))  
        
        #更新已有记录
        Database_Redis_User.objects.filter(db__in=update_user_db_list, user=user.id).update(valid_date = base.getDayAfter(int(request.POST.get('valid_date',1)),format='%Y-%m-%d %H:%M:%S'), 
                                                                                      is_write = int(request.POST.get('is_write',0))) 
                
              
        
             

class RedisManage:  
    get_cmd = ["SCAN","INFO","GET","GETBIT","GETRANGE","GETSET","HGET","HGETALL","HMGET","MGET","EXISTS","HEXISTS","DEBUG"]
    
    def __init__(self):
        super(RedisManage,self).__init__() 
        
    def allowcator(self,sub,request):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(request)
        else:
            logger.error(msg="RedisManage没有{sub}方法".format(sub=sub))       
            return "参数错误" 
    
    def __check_user_perms(self,request,perms='databases.database_read_redis_server_config'):
        
        dbServer = self.__get_db(request)

        if request.user.is_superuser and dbServer:
            return dbServer
        
        if  dbServer and request.user.has_perm(perms):
            try:
                user_db = Database_Redis_User.objects.get(db=request.POST.get('db'),user=request.user.id) 
                if base.changeTotimestamp(str(user_db.valid_date)) - int(time.time()) > 0:#判断用户数据权限是否过期
                    return dbServer
            except Exception as ex:
                logger.warn(msg="查询用户数据库信息失败: {ex}".format(ex=str(ex)))  
                 
        raise PermissionDenied  

    
    def _check_user_db_cmds(self,request):
        try:     
            userDbServer = Database_Redis_User.objects.get(user=request.user.id,db=request.POST.get('db'))
            if userDbServer.cmds:return userDbServer.cmds.split(",")
        except Exception as ex:
            logger.warn(msg="查询用户数据库权限失败: {ex}".format(ex=str(ex)))  
            
        return []              

    def _extract_cmds_from_cmd(self, cmd):        
        return cmd.split(" ")[0].upper()    
    
    def _check_sql_parse(self, request, allow_sql, sql, read_only=True):                
        #查询用户是不是有授权表
        grant_cmds = self._check_user_db_cmds(request)
        
        #提取SQL中的表名
        extract_cmds = self._extract_cmds_from_cmd(sql)
        
        if extract_cmds not in grant_cmds:
            return "命令未授权, 联系管理员授权"  
                                       
        return True 
                  
    
    def __get_db(self,request):
        try:
            db_info = Database_Redis_Detail.objects.get(id=self.change(request.POST.get('db')))
            dbServer = db_info.db_server.to_connect()      
            dbServer["db_name"] = db_info.db_name
            return  dbServer
        except Exception as ex:
            logger.error(msg="获取DB实例失败: {ex}".format(ex=ex))       
            raise PermissionDenied   
                                   
    
    def __get_db_server(self,dbServer):
        try:
            return RedisBase(dbServer=dbServer)
        except Exception as ex:
            logger.error(msg="数据库不存在: {ex}".format(ex=ex)) 
            return ex          
            
        
    def __record_operation(self, username, db, time_consume, result, sql):
        if isinstance(result, str):
            record_exec_sql.apply_async((username, db, sql, time_consume, 0, 1, result), queue='default')
        else:
            record_exec_sql.apply_async((username, db, sql, time_consume, result[0], 0),queue='default')        
       
    def tree(self,request):
        return AppsTree(Business_Tree_Assets,
                        DataBase_Redis_Server_Config, 
                        Database_Redis_User, 
                        Database_Redis_Detail,
                        request).db_tree()       
