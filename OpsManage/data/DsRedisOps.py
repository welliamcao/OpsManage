# -*- coding=utf-8 -*-
from OpsManage.data.base import APBase

class DsRedis(object):
    class OpsDeploy(object):
        @staticmethod
        def lpush(redisKey,data):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.lpush(redisKey, data)
                redisConn = None 
            except:
                return False
        
        @staticmethod
        def rpop(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.rpop(redisKey) 
                redisConn = None
                return data    
            except:
                return False        
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.delete(redisKey) 
                redisConn = None
                return data  
            except:
                return False      
            
    class OpsProject(object):   
        @staticmethod
        def set(redisKey,value):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.set(redisKey, value)
                redisConn.expire(redisKey, 300)
                redisConn = None 
            except:
                return False
            
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.delete(redisKey)
                redisConn = None 
            except:
                return False     

        @staticmethod
        def get(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                result = redisConn.get(redisKey)
                redisConn = None 
                return result
            except:
                return False      
            
    class OpsAnsibleModel(object):
        @staticmethod
        def lpush(redisKey,data):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.lpush(redisKey, data)
                redisConn = None 
            except:
                return False
        
        @staticmethod
        def rpop(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.rpop(redisKey) 
                redisConn = None
                return data    
            except:
                return False        
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.delete(redisKey) 
                redisConn = None
                return data  
            except:
                return False   
            
    class OpsAnsiblePlayBook(object):
        @staticmethod
        def lpush(redisKey,data):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.lpush(redisKey, data)
                redisConn = None 
            except:
                return False
        
        @staticmethod
        def rpop(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.rpop(redisKey) 
                redisConn = None
                return data    
            except:
                return False        
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.delete(redisKey) 
                redisConn = None
                return data  
            except:
                return False      

            
    class OpsAnsiblePlayBookLock(object):  
        @staticmethod
        def set(redisKey,value):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.set(redisKey, value)
                redisConn.expire(redisKey, 1800)
                redisConn = None 
            except:
                return False                  
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.delete(redisKey)
                redisConn = None 
            except:
                return False     

        @staticmethod
        def get(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                result = redisConn.get(redisKey)
                redisConn = None 
                return result
            except:
                return False                                         