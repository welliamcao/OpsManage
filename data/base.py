# -*- coding=utf-8 -*-
'''
应用基类（每次应用启动时，都必须调用基类的初始化方法）
@author: welliam.cao<303350019@qq.com> 
@version:1.0 2017年4月12日
'''
import redis
from django.conf import settings

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
