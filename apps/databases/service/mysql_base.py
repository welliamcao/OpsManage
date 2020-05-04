#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from dao.base import MySQLPool
from utils.logger import logger

class MySQLBase(MySQLPool):
    
    def get_processlists(self):
        try:
            sql = """select id,user,host,db,time,state,command,info from information_schema.processlist;"""
            return self.queryMany(sql)
        except Exception as ex:
            logger.exor(ex.__str__())
            return -1 