#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import subprocess,os,sys

def loads(host,user,passwd,port,dbname,sql):
    cmd = "mysql -h {host} -u {user} -p{passwd}  {dbname} -P {port} --default-character-set=utf8 < {sql}".format(host=host,user=user,passwd=passwd,dbname=dbname,sql=sql,port=port)
    return subprocess.getstatusoutput(cmd)    

def dumps(host,user,passwd,port,dbname,sql,tables=None):
    if tables:cmd = "mysqldump -h {host} -u {user} -p{passwd} -P {port} {dbname}  {tables }> {sql}".format(host=host,user=user,passwd=passwd,port=port,dbname=dbname,sql=sql,tables=tables)
    else:cmd = "mysqldump -h {host} -u {user} -p{passwd} -P {port} {dbname} > {sql}".format(host=host,user=user,passwd=passwd,port=port,dbname=dbname,sql=sql)
    return subprocess.getstatusoutput(cmd)     