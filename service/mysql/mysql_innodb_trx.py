#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from libs.sqlpool import MySQLPool
from utils.logger import logger

class MySQLInnodbTrx(MySQLPool):
    def get_locked_trx(self):
        """查看innodb存储引擎是否有锁等待"""
        try:
            sql = """select trx_id,trx_state,trx_started,trx_query,trx_tables_in_use,trx_tables_locked,trx_concurrency_tickets from information_schema.innodb_trx where trx_id in (select blocking_trx_id  from `information_schema`.`innodb_lock_waits`);"""
            return self.queryMany(sql)
        except Exception as ex:
            logger.error(ex.__str__())
            return []
    
    def get_block_trx(self, second=10):
        """阻塞超过10秒的sql"""
        try:
            sql = """select b.trx_mysql_thread_id as '被阻塞线程',b.trx_query as '被阻塞SQL',c.trx_mysql_thread_id as '阻塞线程',c.trx_query as '阻塞SQL',(UNIX_TIMESTAMP() - UNIX_TIMESTAMP(c.trx_started)) as '阻塞时间' 
                        from information_schema.innodb_lock_waits a 
                        join information_schema.innodb_trx b on a.requesting_trx_id=b.trx_id 
                        join information_schema.innodb_trx c 
                        on a.blocking_trx_id=c.trx_id 
                        where (UNIX_TIMESTAMP() - UNIX_TIMESTAMP(c.trx_started))>{second};""".format(second=second)
            return self.queryMany(sql)
        except Exception as ex:
            logger.error(ex.__str__())
            return []           
        