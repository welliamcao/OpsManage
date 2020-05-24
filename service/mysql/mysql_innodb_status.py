#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from .mysql_status import MySQLStatus
from utils.logger import logger

class MySQInnodbRowLockWaits(MySQLStatus):
    """innodb行锁，太大可能是间隙锁造成的"""
    level = 'low'
    metric = None
    key_name = "Innodb_row_lock_waits" 

class MySQLInnodbAvailableUndoLogs(MySQLStatus):
    """innodb当前可用的undo段的数据"""
    level = 'mid'
    metric = None
    key_name = "innodb_available_undo_logs"

class MySQLInnodbNumOpenFiles(MySQLStatus):
    """innodb当前打开的文件数量"""
    level = 'mid'
    metric = None
    key_name = "innodb_num_open_files"

class MySQLInnodbRowsUpdated(MySQLStatus):
    """innodb层面执行的update所影响的行数"""
    level = 'low'
    metric = None
    key_name = "innodb_rows_updated"

class MySQLInnodbRowsRead(MySQLStatus):
    """innodb 层面受读操作所影响的行数"""
    level = 'low'
    metric = None
    key_name = "innodb_rows_read"

class MySQLInnodbRowsInserted(MySQLStatus):
    """innodb 层面受insert操作所影响的行数"""
    level = 'low'
    metric = None
    key_name = "innodb_rows_inserted"

class MySQLInnodbRowsDeleted(MySQLStatus):
    """innodb 层面受delete操作所影响的行数"""
    level = 'low'
    metric = None
    key_name = "innodb_rows_deleted"

class MySQLInnodbRowLockWaits(MySQLStatus):
    """innodb 行锁等待的次数"""
    level = 'high'
    metric = None
    key_name = "innodb_row_lock_waits"

class MySQLInnodbRowLockTimeMax(MySQLStatus):
    """innodb层面行锁等待的最大毫秒数"""
    level = 'mid'
    metric = None
    key_name = "innodb_row_lock_time_max"

class MySQLInnodbRowLockTimeAvg(MySQLStatus):
    """innodb层面行锁等待的平均毫秒数"""
    level = 'mid'
    metric = None
    key_name = "Innodb_row_lock_time_avg"

class MySQLInnodbRowLockTime(MySQLStatus):
    """innodb层面行锁等待的总毫秒数"""
    level = 'mid'
    metric = None
    key_name = "Innodb_row_lock_time"

class MySQLInnodbPagesWritten(MySQLStatus):
    """innodb层面写入磁盘的页面数"""
    level = 'low'
    metric = None
    key_name = "Innodb_pages_written"

class MySQLInnodbPagesRead(MySQLStatus):
    """从innodb buffer pool 中读取的页数"""
    level = 'low'
    metric = None
    key_name = "Innodb_pages_read"

class MySQLInnodbOsLogWritten(MySQLStatus):
    """innodb redo 写入字节数"""
    level = 'low'
    metric = None
    key_name = "Innodb_os_log_written"

class MySQLInnodbOsLogPendingWrites(MySQLStatus):
    """innodb redo log 被挂起的写操作次数"""
    level = 'low'
    metric = None
    key_name = "Innodb_os_log_pending_writes"

class MySQLInnodbOsLogPendingFsyncs(MySQLStatus):
    """innodb redo log 被挂起的fsync操作次数"""
    level = 'low'
    metric = None
    key_name = "Innodb_os_log_pending_fsyncs"

class MySQLInnodbOsLogFsyncs(MySQLStatus):
    """innodb redo log fsync的次数"""
    level = 'mid'
    metric = None
    key_name = "Innodb_os_log_fsyncs"

class MySQLInnodbLogWrites(MySQLStatus):
    """innodb redo log 物理写的次数"""
    level = 'mid'
    metric = None
    key_name = "innodb_log_writes"

class MySQLInnodbLogWriteRequests(MySQLStatus):
    """innodb redo log 逻辑写的次数"""
    level = 'low'
    metric = None
    key_name = "Innodb_log_write_requests"

class MySQLInnodbLogWaits(MySQLStatus):
    """innodb 写redo 之前必须等待的次数"""
    level = 'low'
    metric = None
    key_name = "Innodb_log_waits"

class MySQLInnodbDblwrWrites(MySQLStatus):
    """Innodb_log_waits值不等于0的话，表明 innodb log buffer 因为空间不足而等待"""
    level = 'high'
    metric = None
    key_name = "Innodb_dblwr_writes"

class MySQLInnodbDblwrPagesWritten(MySQLStatus):
    """innodb double write的页面数量"""
    level = 'mid'
    metric = None
    key_name = "Innodb_dblwr_pages_written"

class MySQLInnodbDoubleWriteLoader(MySQLStatus):
    """innodb double write 压力1~64、数值越大压力越大"""
    level = 'mid'
    metric = 32
    key_name = 'innodb_double_writes'
    def get_value(self, status=None):
        try:
            sql = """show global status like 'innodb_dblwr_pages_written';"""
            row = self.queryOne(sql)
            pages=float((row[1][1]))
            sql = """show global status like 'innodb_dblwr_writes';"""
            row = self.queryOne(sql)
            requests = float(row[1][1])
            if requests == 0:
                return 0
            return round(pages/requests,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLInnodbBufferPoolHitRate(MySQLStatus):
    """innodb buffer pool 命中率  计算公式：innodb_buffer_read_hits = (1 - innodb_buffer_pool_reads / innodb_buffer_pool_read_requests) * 100%"""
    level = 'high'
    metric = 90
    key_name = 'innodb_buffer_read_hits'
    def get_value(self, status=None):
        try:
            sql = """show global status like 'innodb_buffer_pool_read_requests';"""
            row = self.queryOne(sql)
            hit_read=float((row[1][1]))
            sql = """show global status like 'innodb_buffer_pool_reads';"""
            row = self.queryOne(sql)
            miss_read=float(row[1][1])
            total_read=(miss_read + hit_read)
            if total_read == 0:
                return 0
            return round((hit_read / total_read) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1
        
class MySQLInnodbBufferPoolFreePagePercent(MySQLStatus):
    """innodb buffer pool free page 百分比"""
    level = 'high'
    metric = 10
    key_name = 'innodb_buffer_pool_dirty_free_percent'
    def get_value(self, status=None):
        try:
            sql = """show global status like 'innodb_buffer_pool_pages_total';"""
            row = self.queryOne(sql)
            total_page=float((row[1][1]))
            sql = """show global status like 'innodb_buffer_pool_pages_free';"""
            row = self.queryOne(sql)
            free_page = float(row[1][1])
            return round((free_page / total_page) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1

class MySQLInnodbBufferPoolDirtyPercent(MySQLStatus):
    """innodb buffer pool dirty page 百分比"""
    level = 'high'
    metric = 10
    key_name = 'innodb_buffer_pool_dirty_page_percent'
    def get_value(self, status=None):
        try:
            sql = """show global status like 'innodb_buffer_pool_pages_total';"""
            row = self.queryOne(sql)
            total_page=float((row[1][1]))
            sql = """show global status like 'innodb_buffer_pool_pages_dirty';"""
            row = self.queryOne(sql)
            dirty_page = float(row[1][1])
            return round((dirty_page / total_page) * 100,2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1    
        
        
class MySQLInnodbMemUsed(MySQLStatus):
    """innodb参数配置占用的内存，返回值不超过服务器内存大小表示ok，单位是MB"""
    level = 'mid'
    metric = None
    key_name = 'innodb_args_config_mem_used'
    def get_value(self, status=None):
        try:
            sql = """SELECT ((@@key_buffer_size+@@innodb_buffer_pool_size+@@innodb_log_buffer_size)/1024/1024)+((@@read_rnd_buffer_size+@@read_buffer_size+@@myisam_sort_buffer_size+@@sort_buffer_size+@@join_buffer_size)/1024/1024*@@max_connections) as usedMem;"""
            row = self.queryOne(sql)
            return round(row[1][0],2)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1            