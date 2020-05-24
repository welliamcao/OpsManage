#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from libs.sqlpool import MySQLPool
from utils.logger import logger
from .mysql_status import MySQLStatus
from utils import base

class MySQLVariables(MySQLPool):
        
    def get_value(self, variables):
        try:
#             sql = """show global variables like '{0}';""".format(self.key_name)
#             row = self.queryOne(sql)
#             return row[1][1]
            return variables.get(self.key_name.lower())
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLUptime(MySQLStatus):
    """数据库启动多久"""
    level = 'low'
    metric = None
    key_name = "Uptime"

    def get_value(self, variables=None):
        try:
            sql = """show global status like 'Uptime';"""
            row = self.queryOne(sql)
            return base.format_time(int(row[1][1]))
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLDiskUsed(MySQLPool):
    """硬盘使用情况(单位:MB)"""
    level = 'mid'
    metric = None
    key_name = "disk_used"
    
    def get_value(self, variables=None):
        try:
            sql = "select TABLE_SCHEMA, concat(truncate(sum(data_length)/1024/1024,2)) as data_size,concat(truncate(sum(index_length)/1024/1024,2)) as index_size from information_schema.tables group by TABLE_SCHEMA order by data_length desc;" #单位MB
            row = self.queryAll(sql)
            disk_size = 0
            for i in row[1]:
                for j in i[1:]:
                    disk_size += float(j)            
            disk_used_percent = disk_size
            return int(disk_used_percent)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLMemUsed(MySQLPool):
    """内存使用情况(单位:MB)"""
    level = 'mid'
    metric = None
    key_name = "mem_used"
    def get_value(self, variables=None):
        try:
            sql = "select (@@key_buffer_size + @@query_cache_size + @@tmp_table_size +@@innodb_buffer_pool_size +@@innodb_additional_mem_pool_size +@@innodb_log_buffer_size +@@max_connections * (@@read_buffer_size +@@read_rnd_buffer_size +@@sort_buffer_size + @@join_buffer_size +@@binlog_cache_size +@@thread_stack)) /1024/1024/1024 AS MAX_MEMORY_GB;"
            row = self.queryOne(sql)
            mem_used_GB = 0
            mem_used_GB = float(row[1][0])
            return round(mem_used_GB,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLBasedir(MySQLVariables):
    """MySQL安装目录所在位置"""
    metric = None
    key_name = "basedir"

class MySQLDatadir(MySQLVariables):
    """MySQL数据目录所在位置"""
    metric = None
    key_name = "datadir"

class MySQLVersion(MySQLVariables):
    """MySQL版本号"""
    metric = None
    key_name = "version"

class MySQLServerId(MySQLVariables):
    """MySQL的server_id"""
    metric = None
    key_name = "server_id"

class MySQLLogBin(MySQLVariables):
    """binlog 是否有开启"""
    key_name = "log_bin"

class MySQLLogexor(MySQLVariables):
    """exorlog文件名"""
    metric = None
    key_name = "log_exor"

class MySQLPerformanceSchema(MySQLVariables):
    """performance_schema是否有开启"""
    metric = None
    key_name = "performance_schema"

class MySQLInnodbBufferPoolSize(MySQLVariables):
    """MySQL innodb_buffer_pool的大小(GB)"""
    metric = None
    key_name = "innodb_buffer_pool_size"
    
    def get_value(self, variables=None):
        try:
            sql = "show global variables like 'innodb_buffer_pool_size';"
            row = self.queryOne(sql)
            poolSize = int(row[1][1]) / 1024/ 1024 /1024
            return poolSize
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLMaxConnections(MySQLVariables):
    """最大连接数"""
    metric = None
    key_name = "max_connections"   