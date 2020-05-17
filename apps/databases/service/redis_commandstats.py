#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from .redis_base import RedisInfo


                
class RedisCmdstatSet(RedisInfo):    
    """Set 命令统计"""
    level = 'low'
    metric = None
    section = "Commandstats"
    key_name = "cmdstat_set"    


class RedisCmdstatPing(RedisInfo):    
    """Ping 命令统计"""
    level = 'low'
    metric = None
    section = "Commandstats"
    key_name = "cmdstat_ping" 
    
    
class RedisCmdstatDel(RedisInfo):    
    """Del 命令统计"""
    level = 'low'
    metric = None
    section = "Commandstats"
    key_name = "cmdstat_del" 
    
class RedisCmdstatPsync(RedisInfo):    
    """Psync 命令统计"""
    level = 'low'
    metric = None
    section = "Commandstats"
    key_name = "cmdstat_psync"    
    
class RedisCmdstatKeys(RedisInfo):    
    """Keys 命令统计"""
    level = 'low'
    metric = None
    section = "Commandstats"
    key_name = "cmdstat_keys"     
    
class RedisCmdstatHmset(RedisInfo):    
    """Hmset命令统计"""
    level = 'low'
    metric = None
    section = "Hmset命令统计"
    key_name = "cmdstat_hmset"     
    
class RedisCmdstatCommand(RedisInfo):    
    """Command命令统计"""
    level = 'low'
    metric = None
    section = "Hmset命令统计"
    key_name = "cmdstat_command"      
    
class RedisCmdstatInfo(RedisInfo):    
    """Info命令统计"""
    level = 'low'
    metric = None
    section = "info命令统计"
    key_name = "cmdstat_info"      
    
class RedisCmdstatReplconf(RedisInfo):    
    """Replconf命令统计"""
    level = 'low'
    metric = None
    section = "info命令统计"
    key_name = "cmdstat_replconf"     
    
class RedisCmdstatClient(RedisInfo):    
    """Client命令统计"""
    level = 'low'
    metric = None
    section = "info命令统计"
    key_name = "cmdstat_client"   
    
class RedisCmdstatHgetall(RedisInfo):    
    """Client命令统计"""
    level = 'low'
    metric = None
    section = "info命令统计"
    key_name = "cmdstat_hgetall"        