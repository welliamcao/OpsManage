#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from .redis_base import RedisInfo


                
class RedisSyncFull(RedisInfo):    
    """Redis主机和从机进行完全同步的次数。如果值太大需要注意"""
    level = 'high'
    metric = None
    section = "Stats"
    key_name = "sync_full"     
    

class RedisEvictedKeys(RedisInfo):    
    """由于maxmemory限制，而被回收内存的键的总数。如果值太大需要注意"""
    level = 'high'
    metric = None
    section = "Stats"
    key_name = "evicted_keys"        
    
class RedisExpiredKeys(RedisInfo):    
    """Redis键过期事件的总数"""
    level = 'low'
    metric = None
    section = "Stats"
    key_name = "expired_keys"     
    
class RedisInstantaneousOpsPerSec(RedisInfo):    
    """每秒钟处理的命令数量。"""
    level = 'mid'
    metric = None
    section = "Stats"
    key_name = "instantaneous_ops_per_sec"   
    
class RedisInstantaneousInputKbps(RedisInfo):    
    """每秒钟接收数据的速率，以kbps为单位。"""
    level = 'mid'
    metric = None
    section = "Stats"
    key_name = "instantaneous_input_kbps"     
    
class RedisInstantaneousOutputKbps(RedisInfo):    
    """每秒钟发送数据的速率，以kbps为单位。"""
    level = 'mid'
    metric = None
    section = "Stats"
    key_name = "instantaneous_output_kbps"       


class RedisKeyspaceHits(RedisInfo):    
    """成功查找到键的次数。"""
    level = 'mid'
    metric = None
    section = "Stats"
    key_name = "keyspace_hits"  
    
    
class RedisKeyspaceMisses(RedisInfo):    
    """未能成功查找到键的次数。"""
    level = 'high'
    metric = None
    section = "Stats"
    key_name = "keyspace_misses"    
    
class RedisLatestForkUsec(RedisInfo):    
    """最近一次fork操作消耗的时间，以微秒为单位。"""
    level = 'high'
    metric = None
    section = "Stats"
    key_name = "latest_fork_usec"       
    