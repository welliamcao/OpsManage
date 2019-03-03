#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import re, pymysql
from databases.models import Custom_High_Risk_SQL
from utils.logger import logger 
from OpsManage.settings import INCEPTION_CONFIG
from dao.base import Struct


class Inception():
    def __init__(self,host=None,name=None,user=None,passwd=None,port=None):
        self.db_host = host
        self.db_name = name
        self.db_user = user
        self.db_passwd = passwd
        self.db_port = port
        self.incept = Struct(**INCEPTION_CONFIG)
        
    def run(self,action,auditSql):
        sql='''/*--user={db_user};--password={db_passwd};--host={db_host};{action}--port={db_port};*/\
            inception_magic_start;
            use {db_name};
            set names utf8;
            {auditSql}
            inception_magic_commit;'''.format(
                                              db_user=self.db_user,db_host=self.db_host,
                                              db_passwd = self.db_passwd,db_port = self.db_port,
                                              db_name=self.db_name,
                                              action=action,auditSql=auditSql
                                              )
        try:
            conn = pymysql.connect(host=self.incept.host,user='',passwd='',db='',port=int(self.incept.port))
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()
            dataList = []
            for row in result:
                data = dict()
                data['stage'] = row[1]
                data['errlevel'] = row[2]
                data['stagestatus'] = row[3]
                data['errormessage'] = row[4]
                data['sqltext'] = row[5]
                data['affectrow'] = row[6]
                data['sequence'] = row[7]
                data['backup_dbname'] = row[8]
                data['execute_time'] = row[9]
                data['sqlsha1'] = row[10]
                dataList.append(data)
            cur.close()
            conn.close()
            return {"status":'success','data':dataList}
        except pymysql.Error as e:
            logger.error(msg="Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return {"status":'error',"errinfo":"Mysql Error %d: %s" % (e.args[0], e.args[1])}        
        
    def checkSql(self,sql):
        #检查alert语句是否符合规则
        result = self.alterSqlCheck(sql)
        if isinstance(result, dict):return result
        #检查自定义规则的语句是否符合规则
        result = self.customSql(sql)
        if isinstance(result, dict):return result
        return self.run(action='--enable-check;', auditSql=sql)
    
    def customSql(self,sql):
        sqlList = Custom_High_Risk_SQL.objects.all()
        if sqlList.count() > 0:
            c_sql = ''
            for ds in sqlList:
                c_sql += ds.sql.lower() + '|'
            c_sql = c_sql[0:-1]
            for row in sql.rstrip(';').split(';'):
                if re.match(r"{custom_sql}".format(custom_sql=c_sql), row.lower()):
                    return {"status":'error',"errinfo":"SQL语法错误', '{row};符合高危SQL规则。".format(row=row)}
        else:
            return []
    
    def execSql(self,sql,action=None):
        if action:action = '--enable-execute;' + action
        else:action = '--enable-execute;'
        return self.run(action=action, auditSql=sql)
    
    def incQuery(self,sql):   
        try:
            conn = pymysql.connect(host=self.incept.host,user='',passwd='',db='',port=int(self.incept.port))
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.close()
            return {"status":'success','data':result}
        except pymysql.Error as e:
            logger.error(msg="Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return {"status":'error',"errinfo":"Mysql Error %d: %s" % (e.args[0], e.args[1])}         
    
    def getOscStatus(self,sqlSHA1):
        """根据SHA1值，去inception里查看OSC进度"""
        sql = "inception get osc_percent '{sqlSHA1}';".format(sqlSHA1=sqlSHA1)
        result = self.incQuery(sql)
        if result.get('data'):
            percent = result[0][3]
            timeRemained = result[0][4]
            result = {"status":"success","data":{"percent":percent, "timeRemained":timeRemained}}
        else:
            result = {"status":'error', "data":{"percent":100, "timeRemained":"00:00"}}
        return result      
    
    def stopOsc(self, sqlSHA1):
        sql = "inception stop alter '%s'" % sqlSHA1
        result = self.incQuery(sql)
        return result
    
    def exec_custom_sql(self,sql):
        try:
            conn = pymysql.connect(
                                   host=self.db_host,user=self.db_user,
                                   passwd=self.db_passwd,db=self.db_name,
                                   port=int(self.db_port),
                                   use_unicode=True,
                                   charset='utf8'                                   
                                   )
        except Exception as e:
            logger.error(msg="Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return {"status":'error',"errinfo":"Mysql Error %d: %s" % (e.args[0], e.args[1])}        
        try:
            cur = conn.cursor()
            ret = cur.execute(sql)
            # 提交到数据库执行
            conn.commit()
            result = cur.fetchall()
            cur.close()
            conn.close()
            return {"status":'success','data':result}
        except pymysql.Error as e:
            #遇到错误就回滚
            conn.rollback()
            return {"status":'error',"errinfo":"Mysql Error %d: %s" % (e.args[0], e.args[1])}         
    
    def alterSqlCheck(self, sql):
        for row in sql.rstrip(';').split(';'):
            if re.match(r"(\s*)alter(\s+)table(\s+)(\S+)(\s*);|(\s*)alter(\s+)table(\s+)(\S+)\.(\S+)(\s*);", row.lower() + ";"):            
                return {"status":'error',"errinfo":"SQL语法错误', 'ALTER TABLE 必须带有选项"}
        return []


        
    def getRollBackSQL(self,dbName,tableName,sequence):
        sql='''select rollback_statement from {tableName} where opid_time="{sequence}";'''.format(tableName=tableName,sequence=sequence)       
        try:
            conn = pymysql.connect(
                                   host=self.incept.backup_host,user=self.incept.backup_user,
                                   passwd=self.incept.backup_passwd,db=dbName,
                                   port=int(self.incept.backup_port),
                                   use_unicode=True,
                                   charset='utf8'
                                   )
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.close()
            return {"status":'success','data':result}
        except pymysql.Error as e:
            logger.error(msg="Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return {"status":'error',"errinfo":"Mysql Error %d: %s" % (e.args[0], e.args[1])}
               
    def getRollBackTable(self,dbName,sequence):
        sql='''SELECT tablename from  $_$inception_backup_information$_$ where opid_time = '{sequence}';'''.format(sequence = sequence)      
        try:
            conn = pymysql.connect(
                                   host=self.incept.backup_host,user=self.incept.backup_user,
                                   passwd=self.incept.backup_passwd,db=dbName,
                                   port=int(self.incept.backup_port),
                                   use_unicode=True,
                                   charset='utf8'                                   
                                   )
            cur = conn.cursor()
            ret = cur.execute(sql)
            result = cur.fetchone()
            cur.close()
            conn.close()
            return {"status":'success','data':result}
        except pymysql.Error as e:
            logger.error(msg="Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return {"status":'error',"errinfo":"Mysql Error %d: %s" % (e.args[0], e.args[1])}                  