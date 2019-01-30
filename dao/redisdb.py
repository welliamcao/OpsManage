# -*- coding=utf-8 -*-
from .base import APBase
from utils.logger import logger

class DsRedis(object):
    class OpsDeploy(object):
        @staticmethod
        def lpush(redisKey,data):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.lpush(redisKey, data)
                redisConn = None 
            except Exception as ex:
                logger.warn(msg="Lpush data to redis failed: {ex}".format(ex=str(ex)))
                return False
        
        @staticmethod
        def rpop(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.rpop(redisKey) 
                redisConn = None
                return data    
            except Exception as ex:
                logger.warn(msg="Rpop redis key failed: {ex}".format(ex=str(ex)))
                return False        
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.delete(redisKey) 
                redisConn = None
                return data  
            except Exception as ex:
                logger.warn(msg="Delete redis key failed: {ex}".format(ex=str(ex)))
                return False      
            
    class OpsProject(object):   
        @staticmethod
        def set(redisKey,value):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.set(redisKey, value)
                redisConn.expire(redisKey, 300)
                redisConn = None 
            except Exception as ex:
                logger.warn(msg="Set redis key failed: {ex}".format(ex=str(ex)))
                return False
            
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.delete(redisKey)
                redisConn = None 
            except Exception as ex:
                logger.warn(msg="Delete redis key failed: {ex}".format(ex=str(ex)))    
                return False
            
        @staticmethod
        def get(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                result = redisConn.get(redisKey)
                redisConn = None 
                return result
            except Exception as ex:
                logger.warn(msg="Get redis key failed: {ex}".format(ex=str(ex))) 
                return False      
            
    class OpsAnsibleModel(object):
        @staticmethod
        def lpush(redisKey,data):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.lpush(redisKey, data)
                redisConn = None 
            except Exception as ex:
                logger.warn(msg="Lpush  redis data failed: {ex}".format(ex=str(ex))) 
                return False
        
        @staticmethod
        def rpop(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.rpop(redisKey) 
                redisConn = None
                return data    
            except Exception as ex:
                logger.warn(msg="Rpop redis data failed: {ex}".format(ex=str(ex))) 
                return False        
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.delete(redisKey) 
                redisConn = None
                return data  
            except Exception as ex:
                logger.warn(msg="Delete redis key failed: {ex}".format(ex=str(ex)))
                return False   
            
    class OpsAnsiblePlayBook(object):
        @staticmethod
        def lpush(redisKey,data):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.lpush(redisKey, data)
                redisConn = None 
            except Exception as ex:
                logger.warn(msg="Lpush  redis data failed: {ex}".format(ex=str(ex))) 
                return False
        
        @staticmethod
        def rpop(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.rpop(redisKey) 
                redisConn = None
                return data    
            except Exception as ex:
                logger.warn(msg="Rpop redis data failed: {ex}".format(ex=str(ex))) 
                return False        
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                data = redisConn.delete(redisKey) 
                redisConn = None
                return data  
            except Exception as ex:
                logger.warn(msg="Delete redis key failed: {ex}".format(ex=str(ex)))
                return False      
            
    class OpsAnsiblePlayBookLock(object):  
        @staticmethod
        def set(redisKey,value):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.set(redisKey, value)
                redisConn.expire(redisKey, 1800)
                redisConn = None 
            except Exception as ex:
                logger.warn(msg="Set redis key failed: {ex}".format(ex=str(ex)))
                return False                  
        @staticmethod
        def delete(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                redisConn.delete(redisKey)
                redisConn = None 
            except Exception as ex:
                logger.warn(msg="Delete redis key failed: {ex}".format(ex=str(ex)))
                return False     

        @staticmethod
        def get(redisKey):
            try:
                redisConn = APBase.getRedisConnection(APBase.REDSI_POOL)
                result = redisConn.get(redisKey)
                redisConn = None 
                return result
            except Exception as ex:
                logger.warn(msg="Get redis key failed: {ex}".format(ex=str(ex))) 
                return False                                         