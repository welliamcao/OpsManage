#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from libs.redispool import RedisPool
from utils.logger import logger

class RedisBase(RedisPool):

    def get_db_size(self):
        cnx = self._connect_remote()
        return cnx.info('keyspace')
       
    
    def get_info(self, section=None):
        cnx = self._connect_remote()
        return cnx.info(section)
    
    
class RedisInfo(RedisPool):
        
    def get_value(self, data):
        try:
            return data.get(self.key_name)
        except Exception as ex:
            logger.error(self.key_name + ': ' + ex.__str__())
            return -1    