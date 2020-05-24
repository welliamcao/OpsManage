#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from libs.sqlpool import MySQLPool

class MySQLReplication(MySQLPool):

    def __init__(self, dbServer):
        self.replication_info = None
        try:
            sql = "show slave status;"
            self.replication_info = self.queryOne(sql)[1]
        except Exception as ex:
            pass

class MySQLReplicationIsRunning(MySQLReplication):
    """mysql replication 是否正常运行"""
    metric = None
    key_name = 'slave_running'
    def get_value(self):
        if self.replication_info == None:
            return "not running"
        else:
            slave_io_running=self.replication_info[10]
            slave_sql_running=self.replication_info[11]
            if slave_io_running == 'Yes' and slave_sql_running == 'Yes':
                return "running"
            return "not running"

class MySQLReplicationBehindMaster(MySQLReplication):
    """主从延迟多少 """
    metric = 500
    key_name = 'slave_behind_master'
    def get_value(self):
        if self.replication_info != None:
            return self.replication_info[32]
        else:
            return -1

