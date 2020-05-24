#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from libs.sqlpool import MySQLPool
from utils.logger import logger

class MySQLStatus(MySQLPool):
        
    def get_value(self, status):
        try:
            return status.get(self.key_name.lower())
        except Exception as ex:
            logger.error(self.key_name + ': ' + ex.__str__())
            return -1
        
class MySQLCurrentClient(MySQLStatus):
    """当前打开连接数"""
    level = 'high'
    metric = None
    key_name = "Threads_connected"

class MySQLTableOpenCacheHitRate(MySQLStatus):
    """表缓存命中率"""
    level = 'high'
    metric = 90
    key_name = "table_open_cache_hits"
    
    def get_value(self, status=None):
        try:
            sql = """show global status like 'table_open_cache_hits';"""
            row = self.queryOne(sql)
            hit = float((row[1][1]))
            sql = """show global status like 'table_open_cache_misses';"""
            row = self.queryOne(sql)
            miss = float(row[1][1])
            return round((hit/(hit + miss)) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1


class MySQLTableOpenCacheOverflows(MySQLStatus):
    """表缓存溢出次数，如果大于0,可以增大table_open_cache和table_open_cache_instances."""
    level = 'low'
    metric = None
    key_name = "Table_open_cache_overflows"

class MySQLTableLocksWaited(MySQLStatus):
    """因不能立刻获得表锁而等待的次数"""
    level = 'high'
    metric = None
    key_name = "table_locks_waited"

class MySQLSlowQueries(MySQLStatus):
    """执行时间超过long_query_time的查询次数，不管慢查询日志有没有打开"""
    level = 'high'
    metric = None
    key_name = "slow_queries"

class MySQLSortScan(MySQLStatus):
    """全表扫描之后又排序(排序键不是主键)的次数"""
    level = 'high'
    metric = None
    key_name = "sort_scan"

class MySQLSortRows(MySQLStatus):
    """与sortscan差不多，前者指的是sortscan的次数，srotrows指的是sort操作影响的行数"""
    level = 'high'
    metric = None
    key_name = "sort_rows"

class MySQLSortRange(MySQLStatus):
    """根据索引进行范围扫描之后再进行排序(排序键不能是主键)的次数"""
    level = 'high'
    metric = None
    key_name = "sort_range"

class MySQLSortMergePasses(MySQLStatus):
    """排序时归并的次数，如果这个值比较大(要求高一点大于0)那么可以考虑增大sort_buffer_size的大小"""
    level = 'low'
    metric = None
    key_name = "Sort_merge_passes"

class MySQLSelectRangeCheck(MySQLStatus):
    """如果值是非零说明语句可能没用上索引"""
    level = 'mid'
    metric = None
    key_name = "select_range_check"

class MySQLQuestions(MySQLStatus):
    """server端执行的语句数量"""
    level = 'low'
    metric = None
    key_name = "Questions"

class MySQLQcacheFreeMemory(MySQLStatus):
    """query cache的可用内存大小"""
    level = 'low'
    metric = None
    key_name = "qcache_free_memory"

class MySQLPreparedStmtCount(MySQLStatus):
    """当前的预处理语句的数量"""
    level = 'low'
    metric = None
    key_name = "prepared_stmt_count"

class MySQLOpenedTables(MySQLStatus):
    """mysql数据库打开过的表，如果这个值过大，应该适当的增大table_open_cache的值"""
    level = 'low'
    metric = None
    key_name = "opened_tables"

class MySQLOpenTables(MySQLStatus):
    """当前mysql数据库打开的表数量"""
    level = 'mid'
    metric = None
    key_name = "open_tables"

class MySQLServerLevelOpenFiles(MySQLStatus):
    """mysql数据库的server层当前正打开的文件数据"""
    level = 'mid'
    metric = None
    key_name = "open_files"



class MySQLQueryCacheHitRate(MySQLStatus):
    """Query Cache 命中率 计算公式：Query_cache_hits = (Qcahce_hits / (Qcache_hits + Qcache_inserts )) * 100%"""
    level = 'low'
    metric = 90
    key_name = 'Query_cache_hits'
    def get_value(self, status=None):
        try:
            sql = """show global status like 'Qcache_hits';"""
            row = self.queryOne(sql)
            qcache_hits = float((row[1][1]))
            sql = """show global status like 'Qcache_inserts';"""
            row = self.queryOne(sql)
            qcache_inserts = float(row[1][1])
            total_qcache = qcache_hits  + qcache_inserts 
            if total_qcache == 0:
                return 0
            return round((qcache_hits / total_qcache) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLThreadCacheHitRate(MySQLStatus):
    """Thread Cache 命中率 计算公式：Thread_cache_hits = (1 - Threads_created / connections ) * 100%"""
    level = 'high'
    metric = 90
    key_name = 'Thread_cache_hits'
    
    def get_value(self, status=None):
        try:
            sql = """show global status like 'Threads_created';"""
            row = self.queryOne(sql)
            threads_created = float((row[1][1]))
            sql = """show global status like 'connections';"""
            row = self.queryOne(sql)
            connections = float(row[1][1])
            return round((1 - threads_created / connections ) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1


class MySQLTableLocksPercent(MySQLStatus):
    """Table_locks_waited/Table_locks_immediate 如果这个比值比较大的话，说明表锁造成的阻塞比较严重"""
    level = 'high'
    metric = 20
    key_name = 'Table_locks_waited'
    
    def get_value(self, status=None):
        try:
            sql = """show global status like 'Table_locks_waited';"""
            row = self.queryOne(sql)
            table_locks_waited = float((row[1][1]))
            sql = """show global status like 'Table_locks_immediate';"""
            row = self.queryOne(sql)
            table_locks_immediate = float(row[1][1])
            return round((table_locks_waited / table_locks_immediate) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLTmpDiskTablesPercent(MySQLStatus):
    """Created_tmp_disk_tables/Created_tmp_tables比值最好不要超过10%，如果Created_tmp_tables值比较大，可能是排序子句过多或者是连接子句不够优化"""
    level = 'high'
    metric = 10
    key_name = 'created_tmp_tables_percent'
    def get_value(self, status=None):
        try:
            sql = """show global status like 'Created_tmp_disk_tables';"""
            row = self.queryOne(sql)
            created_tmp_disk_tables = float((row[1][1]))
            sql = """show global status like 'Created_tmp_tables';"""
            row = self.queryOne(sql)
            created_tmp_tables = float(row[1][1])
            return round((created_tmp_disk_tables / created_tmp_tables) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLConnectionsPercent(MySQLStatus):
    """max_used_connections / max_connections * 100% = 99.6% （理想值 ≈ 85%）"""
    level = 'mid'
    metric = 85
    key_name = 'connections_status'
    
    def get_value(self, status=None):
        try:
            sql = """show global status like 'max_used_connections';"""
            row = self.queryOne(sql)
            max_used_connections = float((row[1][1]))
            sql = """show global variables like 'max_connections';"""
            row = self.queryOne(sql)
            max_connections = float(row[1][1])
            return round((max_used_connections / max_connections) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLHandlexeadRnd(MySQLStatus):
    """如果 Handler_read_rnd太大 ，说明SQL语句里很多查询都是要扫描整个表"""
    level = 'mid'
    metric = None
    key_name = "Handler_read_rnd"

class MySQLHandlexeadFirst(MySQLStatus):
    """如果较高，它表明服务器正执行大量全索引扫描"""
    level = 'high'
    metric = None
    key_name = "Handler_read_first"

class MySQLHandlexeadRndNext(MySQLStatus):
    """该值较高说明你的表索引不正确或写入的查询没有利用索引"""
    level = 'mid'
    metric = None
    key_name = "Handler_read_rnd_next"

class MySQLSelectFullJoin(MySQLStatus):
    """没有使用索引的联接的数量"""
    level = 'mid'
    metric = None
    key_name = "Select_full_join"
    

class MySQLComSelect(MySQLStatus):
    """select 语句执行的次数"""
    level = 'low'
    metric = None
    key_name = "Com_select"

class MySQLComInsert(MySQLStatus):
    """insert 语句执行的次数"""
    level = 'low'
    metric = None
    key_name = "Com_insert"

class MySQLComDelete(MySQLStatus):
    """delete 语句执行的次数"""
    level = 'low'
    metric = None
    key_name = "Com_delete"

class MySQLComUpdate(MySQLStatus):
    """update 语句执行的次数"""
    level = 'low'
    metric = None
    key_name = "Com_update"

class MySQLComCommit(MySQLStatus):
    """事物提交执行的次数"""
    level = 'low'
    metric = None
    key_name = "Com_commit"    

class MySQLComRollback(MySQLStatus):
    """事物回滚 执行的次数"""
    level = 'low'
    metric = None
    key_name = "Com_rollback"  

class MySQLkeyReadRequests(MySQLStatus):
    """Key Buffer 读命中次数  计算公式：key_buffer_read_hits = (1-key_reads / key_read_requests) * 100%"""
    level = 'high'
    metric = 90
    key_name = "key_read_requests"    
    
    def get_value(self, status=None):
        try:
            sql = """show global status like 'key_reads';"""
            row = self.queryOne(sql)
            key_reads = float((row[1][1]))
            sql = """show global status like 'key_read_requests';"""
            row = self.queryOne(sql)
            key_read_requests = float(row[1][1])
            return round((key_reads / key_read_requests) * 100, 2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1    

class MySQLkeyWriteRequests(MySQLStatus):
    """Key Buffer 写命中次数 计算公式：key_buffer_write_hits = (1-key_writes / key_write_requests) * 100%"""
    level = 'high'
    metric = 90
    key_name = "key_write_requests"

    def get_value(self, status=None):
        try:
            sql = """show global status like 'key_writes';"""
            row = self.queryOne(sql)
            key_writes = float((row[1][1]))
            sql = """show global status like 'key_write_requests';"""
            row = self.queryOne(sql)
            key_write_requests = float(row[1][1])
            return round((key_writes / key_write_requests) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1  

class MySQLBinlogCacheDiskUse(MySQLStatus):
    """事务引擎因binlog缓存不足而用到临时文件的次数，如果这个值过大，可以通过增大binlog_cache_size来解决"""
    level = 'low'
    metric = None
    key_name = "Binlog_cache_disk_use"

class MySQLBinlogStmtCacheDiskUse(MySQLStatus):
    """非事务引擎因binlog缓存不足而用到临时文件的次数，如果这个值过大，可以通过增大binlog_stmt_cache_size来解决"""
    level = 'low'
    metric = None
    key_name = "Binlog_stmt_cache_disk_use"
    
    
