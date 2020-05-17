# -*- coding=utf-8 -*-
'''
应用基类（每次应用启动时，都必须调用基类的初始化方法）
@author: welliam.cao<303350019@qq.com> 
@version:1.0 2017年4月12日
'''
import redis, os
from redis.exceptions import  ConnectionError, RedisError
from django.conf import settings
import pymysql
from utils.logger import logger
from django.db import connection
from collections import namedtuple
from datetime import datetime,date
from utils.secret.aescipher import AESCipher
from django.db import models

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class DataHandle(object):
    def __init__(self):
        super(DataHandle,self).__init__()  
            
    def saveScript(self,content,filePath):
        if os.path.isdir(os.path.dirname(filePath)) is not True:os.makedirs(os.path.dirname(filePath))#判断文件存放的目录是否存在，不存在就创建
        with open(filePath, 'w') as f:
            f.write(content) 
        return filePath    
    
    def change(self,args):
        try:
            return int(args)
        except:
            return  0

    def convert_to_dict(self,model):      
        for fieldName in model._meta.get_fields():
            try:
                fieldValue = getattr(model,fieldName.name)
                if type(fieldValue) is date or type(fieldValue) is datetime:
                    fieldValue = datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                setattr(model, fieldName.name, fieldValue)    
            except Exception as ex:
                pass
        data = {}
        data.update(model.__dict__)
        data.pop("_state", None)
        data.pop("script_file",None)
        data.pop("cron_script",None)
        data.pop("_cron_server_cache",None)
        data.pop("playbook_file",None)
        data.pop('_assets_cache',None)
        data.pop('sudo_passwd',None)
        data.pop('passwd',None)  
        data.pop('codename',None)  
        data.pop('content_type_id',None)  
        data.pop('_project_cache',None)
        data.pop('_network_assets_cache',None)
        data.pop('_server_assets_cache',None)            
        return data
    
    def convert_to_dicts(self,models):
        obj_arr = []        
        for obj in models:
            for fieldName in obj._meta.get_fields():
                try:
                    fieldValue = getattr(obj,fieldName.name)
                    if type(fieldValue) is date or type(fieldValue) is datetime:
                        fieldValue = datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                    setattr(obj, fieldName.name, fieldValue)    
                except Exception as ex:
                    pass
            data = {}
            data.update(obj.__dict__)
            data.pop("_state", None)
            data.pop("script_file",None)
            obj_arr.append(dict)
        return obj_arr    

class DjangoCustomCursors(object):
    def __init__(self):
        super(DjangoCustomCursors, self).__init__()
        self.cursor = connection.cursor()
        
        
    def dictfetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]
    
    def namedtuplefetchall(self):
        desc = self.cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in self.cursor.fetchall()]
            
    def execute(self,sql):   
        self.cursor.execute(sql)  
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()           

class APBase(object):
    REDSI_POOL = 10000
    @staticmethod
    def getRedisConnection(db):
        '''根据数据源标识获取Redis连接池'''
        if db==APBase.REDSI_POOL:
            args = settings.REDSI_KWARGS_LPUSH
            if settings.REDSI_LPUSH_POOL == None:
                settings.REDSI_LPUSH_POOL = redis.ConnectionPool(host=args.get('host'), port=args.get('port'), db=args.get('db'))
            pools = settings.REDSI_LPUSH_POOL  
        connection = redis.Redis(connection_pool=pools)
        return connection

   
class MySQLPool: 
    def __init__(self,dbServer, sql=None ,num=1000, model=None, queues=None):    
        self.sql = sql
        self.num = num 
        self.model = model   
        self.dbServer = dbServer

    def __connect_remote(self):
        try:
            return pymysql.connect(
                                   host=self.dbServer["ip"],
                                   user=self.dbServer["db_user"],
                                   password=self.dbServer["db_passwd"],
                                   port=self.dbServer["db_port"],
                                   db=self.dbServer["db_name"],
                                   max_allowed_packet=1024 * 1024 * 1024,
                                   charset='utf8')   
        except pymysql.Error as ex:
            logger.error("连接数据库失败: {ex}".format(ex=ex.__str__()))
            raise pymysql.Error(ex.__str__())        
        
    def queryAll(self,sql, num=1000):  
        
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)   
                result = cursor.fetchall()   
                return (count,result) 
        except pymysql.Error as ex:
            logger.error("数据库查询失败: {ex}".format(ex=str(ex))) 
            return ex.__str__()  
                    
        finally:
            cnx.close()  
   
    def queryOne(self,sql,num=1000):  
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)   
                result = cursor.fetchone()   
                return (count,result) 
        except pymysql.Error as ex:
            logger.error("数据库查询失败: {ex}".format(ex=str(ex)))
            return ex.__str__()
                      
        finally:
            cnx.close()  
  
   
    def queryMany(self,sql, num=1000, param=None):
        
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)
                index = cursor.description
                colName = []
                for i in index:
                    colName.append(i[0])            
                result = cursor.fetchmany(size=num) 
                return (count,result,colName)
        except pymysql.Error as ex:
            logger.error("数据库查询失败: {ex}".format(ex=str(ex)))  
            return ex.__str__()
                       
        finally:
            cnx.close()        
    
    def execute_for_query(self,sql,num=1000):
        
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)
                index = cursor.description
                colName = []
                if index:
                    for i in index:
                        colName.append(i[0]) 
                result = cursor.fetchmany(size=num)           
                return (count,result,colName) 
        except pymysql.Error as ex:
            logger.error("数据库操作失败: {ex}".format(ex=str(ex))) 
            return ex.__str__()
        
        finally:
            cnx.close()
       
         
    def execute(self,sql,num=1000):
               
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)
                index = cursor.description
                colName = []
                if index:
                    for i in index:
                        colName.append(i[0]) 
                result = cursor.fetchmany(size=num)           
                cnx.commit()
                return (count,result,colName) 
        except pymysql.Error as ex:
            logger.error("数据库操作失败: {ex}".format(ex=str(ex))) 
            return ex.__str__()
                        
        finally:
            cnx.close()
    
    def get_value(self):
        pass
                

class RedisPool: 
    def __init__(self, dbServer): 
        self.dbServer = dbServer
          
    def _connect_remote(self):
        try:
            return redis.StrictRedis(host=self.dbServer["ip"], port=self.dbServer["db_port"],db=self.dbServer["db_name"].replace("db",""), password=self.dbServer["db_passwd"])   
        except redis.ConnectionError as ex:
            logger.error("连接数据库失败: {ex}".format(ex=ex.__str__()))
            raise redis.ConnectionError(ex)        
        

    def execute(self, cmd):
        cnx = self._connect_remote()       
        try:
            return cnx.execute_command(cmd)
        except redis.RedisError as ex:
            logger.error("数据库操作失败: {ex}".format(ex=ex.__str__())) 
            return ex.__str__()
        #会自动释放，不需要再显示关闭连接                
#         finally:
#             cnx.close()
    
    def format_result(self, result):
                
        if isinstance(result, bytes):
            return result.decode('utf-8').replace('\n','\n\r')
            
        elif isinstance(result, list):
            results, count = '', 1
            for rs in result:
                rresults, rcount = '', 1
                if isinstance(rs, list):
                    s = ' '
                    for rr in rs:  
                        if isinstance(rr, bytes):
                            rr = rr.decode('utf-8')
                        else:
                            rr = str(rr)
                        if rcount > 1: s = '    '
                        rresults =  rresults + s + str(rcount) +") \""  + rr  + '"\n\r'
                        rcount = rcount + 1
                    if len(rresults) > 0:
                        results = results  + str(count) +") " + rresults
                else:
                    results = results + str(count) +") \"" + rs.decode('utf-8')  + '"\n\r'
                count = count + 1
                
            return results 
                
        else:            
            return str(result) 

class AESCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        if 'prefix' in kwargs:
            self.prefix = kwargs['prefix']
            del kwargs['prefix']
        else:
            self.prefix = "aes:::"
        self.cipher = AESCipher(settings.SECRET_KEY)
        super(AESCharField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(AESCharField, self).deconstruct()
        if self.prefix != "aes:::":
            kwargs['prefix'] = self.prefix
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        if value.startswith(self.prefix):
            value = value[len(self.prefix):]
            value = self.cipher.decrypt(value)
        return value

    def to_python(self, value):
        if value is None:
            return value
        elif value.startswith(self.prefix):
            value = value[len(self.prefix):]
            value = self.cipher.decrypt(value)
        return value

    def get_prep_value(self, value):
        if isinstance(value, str) or isinstance(value, bytes):
            value = self.cipher.encrypt(value)
            value = self.prefix + value.decode('utf-8')
        elif value is not None:
            raise TypeError(str(value) + " is not a valid value for AESCharField")
        return value

            
if __name__=='__main__':   
    pass