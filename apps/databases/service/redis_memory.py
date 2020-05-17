#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from .redis_base import RedisInfo


                
class RedisUsedMemoryHuman(RedisInfo):    
    """Redis分配的内存总量"""
    level = 'high'
    metric = None
    section = "Memory"
    key_name = "used_memory_human"     
    

class RedisUsedMemoryRssHuman(RedisInfo):    
    """从操作系统的角度，返回 Redis已分配的内存总量(俗称常驻集大小)。这个值和 top/ps等命令的输出一致"""
    level = 'high'
    metric = None
    section = "Memory"
    key_name = "used_memory_rss_human"        
    
class RedisMaxmemoryHuman(RedisInfo):    
    """Redis实例的最大内存配置"""
    level = 'high'
    metric = None
    section = "Memory"
    key_name = "maxmemory_human"     
    
class RedisMemoryPolicy(RedisInfo):    
    """当达到maxmemory时的淘汰策略:
        noeviction(默认策略)：对于写请求不再提供服务，直接返回错误（DEL请求和部分特殊请求除外）
        allkeys-lru：从所有key中使用LRU算法进行淘汰
        volatile-lru：从设置了过期时间的key中使用LRU算法进行淘汰
        allkeys-random：从所有key中随机淘汰数据
        volatile-random：从设置了过期时间的key中随机淘汰
        volatile-ttl：在设置了过期时间的key中，根据key的过期时间进行淘汰，越早过期的越优先被淘汰
    """
    level = 'high'
    metric = None
    section = "Memory"
    key_name = "maxmemory_policy"   
