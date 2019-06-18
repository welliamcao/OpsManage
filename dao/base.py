# -*- coding=utf-8 -*-
'''
应用基类（每次应用启动时，都必须调用基类的初始化方法）
@author: welliam.cao<303350019@qq.com> 
@version:1.0 2017年4月12日
'''
import redis,os,threading
from django.conf import settings
import pymysql  
from pymysql.cursors import DictCursor  
from DBUtils.PooledDB import PooledDB  
from utils.logger import logger
from django.db import connection
from collections import namedtuple
from datetime import datetime,date


class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class DataHandle(object):
    def __init__(self):
        super(DataHandle,self).__init__()  
            
    def saveScript(self,content,filePath):
        if os.path.isdir(os.path.dirname(filePath)) is not True:os.makedirs(os.path.dirname(filePath))#判断文件存放的目录是否存在，不存在就创建
        with open(filePath, 'w') as f:
            f.write(content) 
        return filePath    
    
    def change(self,args):
        try:
            return int(args)
        except:
            return  0

    def convert_to_dict(self,model):      
        for fieldName in model._meta.get_fields():
            try:
                fieldValue = getattr(model,fieldName.name)
                if type(fieldValue) is date or type(fieldValue) is datetime:
                    fieldValue = datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                setattr(model, fieldName.name, fieldValue)    
            except Exception as ex:
                pass
        data = {}
        data.update(model.__dict__)
        data.pop("_state", None)
        data.pop("script_file",None)
        data.pop("cron_script",None)
        data.pop("_cron_server_cache",None)
        data.pop("playbook_file",None)
        data.pop('_assets_cache',None)
        data.pop('sudo_passwd',None)
        data.pop('passwd',None)  
        data.pop('codename',None)  
        data.pop('content_type_id',None)  
        data.pop('_project_cache',None)
        data.pop('_network_assets_cache',None)
        data.pop('_server_assets_cache',None)            
        return data
    
    def convert_to_dicts(self,models):
        obj_arr = []        
        for obj in models:
            for fieldName in obj._meta.get_fields():
                try:
                    fieldValue = getattr(obj,fieldName.name)
                    if type(fieldValue) is date or type(fieldValue) is datetime:
                        fieldValue = datetime.strftime(fieldValue, '%Y-%m-%d %H:%M:%S')
                    setattr(obj, fieldName.name, fieldValue)    
                except Exception as ex:
                    pass
            data = {}
            data.update(obj.__dict__)
            data.pop("_state", None)
            data.pop("script_file",None)
            obj_arr.append(dict)
        return obj_arr    

class DjangoCustomCursors(object):
    def __init__(self):
        super(DjangoCustomCursors, self).__init__()
        self.cursor = connection.cursor()
        
        
    def dictfetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]
    
    def namedtuplefetchall(self):
        desc = self.cursor.description
        nt_result = namedtuple('Result', [col[0] for col in desc])
        return [nt_result(*row) for row in self.cursor.fetchall()]
            
    def execute(self,sql):   
        self.cursor.execute(sql)  
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()           

class APBase(object):
    REDSI_POOL = 10000
    MYSQL_POOLS = dict()
    BASEKEYSLIST = [
                'uptime','slave_running','opened_files','opened_tables','connections','threads_connected',
                'binlog_format','expire_logs_days','log_bin','slow_query_log','connections','threads_connected',
                'slow_launch_time','version'
                ]   
    PXCKEYSLIST = [
                'wsrep_cluster_status','wsrep_connected','wsrep_incoming_addresses',
                'wsrep_cluster_size','wsrep_cluster_status','wsrep_ready','wsrep_local_recv_queue','wsrep_local_send_queue',
                'wsrep_local_state_comment',               
            ]  
    SLAVEKEYSLIST = [
                  'slave_io_state','master_host','master_user','master_port','connect_retry','master_log_file',
                  'read_master_log_pos','relay_master_log_file','exec_master_log_pos','seconds_behind_master',
                  'slave_io_running','slave_sql_running','replicate_do_db','slave_sql_running_state','replicate_ignore_db',
                  'relay_log_pos'
            ]
    @staticmethod
    def getRedisConnection(db):
        '''根据数据源标识获取Redis连接池'''
        if db==APBase.REDSI_POOL:
            args = settings.REDSI_KWARGS_LPUSH
            if settings.REDSI_LPUSH_POOL == None:
                settings.REDSI_LPUSH_POOL = redis.ConnectionPool(host=args.get('host'), port=args.get('port'), db=args.get('db'))
            pools = settings.REDSI_LPUSH_POOL  
        connection = redis.Redis(connection_pool=pools)
        return connection

   
class MySQLPool(threading.Thread,APBase): 
    def __init__(self,dbServer,sql=None,num=1000,model=None,queues=None):
        threading.Thread.__init__(self)     
        self.queues = queues
        self.sql = sql
        self.num = num 
        self.model = model 
        self.dbServer = dbServer      
        self.host = dbServer.db_assets.server_assets.ip
        self.port = dbServer.db_port
        self.user = dbServer.db_user
        self.passwd = dbServer.db_passwd
        self.dbName = dbServer.db_name
        self.poolKeys = self.host + self.dbName + str(self.port)#host+dbName+str(port)
        
        
        if self.poolKeys not in MySQLPool.MYSQL_POOLS.keys():  
            self._conn = self._getTupleConn(self.host, self.port, self.user, self.passwd, self.dbName)  
            MySQLPool.MYSQL_POOLS[self.poolKeys] = self._conn
            
        self._conn = MySQLPool.MYSQL_POOLS.get(self.poolKeys)
        
        if not isinstance(self._conn,str):self._cursor = self._conn.cursor() 
                 
    
    def run(self):
        if hasattr(self,self.model):
            func= getattr(self,self.model)
            self.queues.put({"db":str(self.host)+":"+str(self.port),"dataList":func(self.sql, self.num),"dbId":self.dbServer.id})         
     
    def _getDictConn(self,host,port,user,passwd,dbName):
        '''返回字典类型结果集'''   
        if APBase.MYSQL_POOLS.get(self.poolKeys) is None:
            try:
                pool = PooledDB(creator=pymysql, mincached=1 , maxcached=20 ,  
                                      host=host , port=port , user=user , passwd=passwd ,  
                                      db=dbName,use_unicode=True,charset='utf8',
                                      cursorclass=DictCursor)  
                APBase.MYSQL_POOLS[self.poolKeys] = pool   
                return APBase.MYSQL_POOLS.get(self.poolKeys).connection()  
            except Exception as ex:
                logger.error(msg="创建字典类型连接池失败: {ex}".format(ex=ex))
                return str(ex)
            
    def _getTupleConn(self,host,port,user,passwd,dbName):
        '''返回列表类型结果集'''   
        if APBase.MYSQL_POOLS.get(self.poolKeys) is None:
            try:
                pool = PooledDB(creator=pymysql, mincached=1 , maxcached=20 ,  
                                      host=host , port=port , user=user , passwd=passwd ,  
                                      db=dbName,use_unicode=True,charset='utf8')  
                APBase.MYSQL_POOLS[self.poolKeys] = pool   
                return APBase.MYSQL_POOLS.get(self.poolKeys).connection()  
            except Exception as ex:
                logger.error(msg="创建列表类型连接池失败: {ex}".format(ex=ex))
                return str(ex)
   
    def queryAll(self,sql,num=1000):
        if isinstance(self._conn,str):return self._conn   
        try: 
            count = self._cursor.execute(sql)   
            result = self._cursor.fetchall()   
            return (count,result)  
        except Exception as ex:
            logger.error(msg="MySQL查询失败: {ex} sql:{sql}".format(ex=ex,sql=sql))
            return str(ex)

   
    def queryOne(self,sql,num=1000):  
        if isinstance(self._conn,str):return self._conn 
        try: 
            count = self._cursor.execute(sql)   
            result = self._cursor.fetchone()   
            return (count,result)  
        except Exception as ex:
            logger.error(msg="MySQL查询失败: {ex} sql:{sql}".format(ex=ex,sql=sql))
            return str(ex)

  
   
    def queryMany(self,sql,num,param=None):
        if isinstance(self._conn,str):return self._conn   
        """ 
        @summary: 执行查询，并取出num条结果 
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来 
        @param num:取得的结果条数 
        @return: result list/boolean 查询到的结果集 
        """  
        try:
            count = self._cursor.execute(sql,param)  
            index = self._cursor.description
            colName = []
            for i in index:
                colName.append(i[0])            
            result = self._cursor.fetchmany(size=num) 
            return (count,result,colName) 
        except Exception as ex:
#             logger.error(msg="MySQL查询失败: {ex} sql:{sql}".format(ex=ex,sql=sql))
            return str(ex)   
    
    def execute(self,sql,num=1000):
        if isinstance(self._conn,str):return self._conn 
        try:
            count = self._cursor.execute(sql)
            index = self._cursor.description
            colName = []
            if index:
                for i in index:
                    colName.append(i[0]) 
            result = self._cursor.fetchmany(size=num)           
            self._conn.commit()
            return (count,result,colName) 
        except Exception as ex:
#             logger.error(msg="MySQL执行sql失败: {ex} sql:{sql}".format(ex=ex,sql=sql))
            return str(ex)
    
    def get_status(self):
        status = self.execute(sql='show status;')
        baseList = []
        pxcList = []
        if isinstance(status, tuple):
            for ds in status[1]:
                data = {}
                data['value'] = ds[1]
                data['name'] = ds[0].capitalize()
                if ds[0].lower() in APBase.BASEKEYSLIST:baseList.append(data)
                if ds[0].lower() in APBase.PXCKEYSLIST:pxcList.append(data)         
        return baseList,pxcList

    def get_global_status(self):
        baseList = []
        logs = self.execute(sql='show global variables;')
        if isinstance(logs, tuple):
            for ds in logs[1]:
                data = {}
                if ds[0].lower() in APBase.BASEKEYSLIST:
                    data['value'] = ds[1]
                    data['name'] = ds[0].capitalize()
                    baseList.append(data)        
        return baseList
    
    def get_master_status(self):
        masterList = []
        master_status = self.execute(sql='show master status;')
        slave_host = self.execute(sql="SELECT host FROM INFORMATION_SCHEMA.PROCESSLIST WHERE COMMAND='Binlog Dump';")
        if isinstance(master_status, tuple):
            if master_status[1]:
                count = 0
                for ds in master_status[2]:
                    data = {}
                    data["name"] = ds
                    data["value"] = master_status[1][0][count]
                    count = count + 1
                    masterList.append(data)
        if isinstance(slave_host, tuple):
            if slave_host[1]:
                sList = []
                for ds in slave_host[1]:
                    sList.append(ds[0])
                masterList.append({"name":"Slave","value":sList})    
        return  masterList      
    
    def get_slave_status(self):
        slaveList = []
        slave_status = self.execute(sql="show slave status;") 
        if isinstance(slave_status, tuple):   
            if slave_status[1]:
                count = 0
                for ds in slave_status[2]:
                    data = {}
                    if ds.lower() in APBase.SLAVEKEYSLIST:
                        data["name"] = ds
                        data["value"] = slave_status[1][0][count]
                        slaveList.append(data)
                    count = count + 1 
        return  slaveList                     
    
    def close(self,isEnd=1):  
        """ 
        @summary: 释放连接池资源 
        """  
        try:
            self._cursor.close()  
            self._conn.close() 
        except:
            pass
        
class MySQLThread(threading.Thread):
    def __init__(self,host,port,dbname,user,passwd,sql=None,num=1000,queue=None):
        threading.Thread.__init__(self)
        self._conn = self.connect(host, port, dbname, user, passwd)
        self._cursor = self._conn.cursor()
        self.queue = queue
        self.sql = sql
        self.num = num
    
    def run(self):
        self.queue.put(self.execute(self.sql, self.num))    
        
    def connect(self,host,port,dbname,user,passwd):
        try:
            conn = pymysql.connect(host,user,passwd,dbname,port)          
            return conn
        except pymysql.Error as ex:  
            print(ex)
            return False
                 
    def execute(self,sql,num=1000): 
        try:           
            count = self._cursor.execute(sql)
            index = self._cursor.description
            colName = []
            if index:
                for i in index:
                    colName.append(i[0]) 
            result = self._cursor.fetchmany(size=num)           
            self._conn.commit()
            return (count,result,colName) 
        except Exception as ex:
            logger.error(msg="MySQL执行失败: {ex} sql:{sql}".format(ex=ex,sql=sql))
            self.conn.rollback()
            count = 0 
            result = None
        finally:
            return count,result
                
    
    def queryAll(self,sql):  
        try: 
            count = self._cursor.execute(sql)   
            result = self._cursor.fetchall()   
            return count,result
        except Exception as ex:
            logger.error(msg="MySQL查询失败: {ex} sql:{sql}".format(ex=ex,sql=sql))
            count = 0
            result = None
        finally:
            return count, result
    
    def queryOne(self,sql):
        try: 
            count = self._cursor.execute(sql)   
            result = self._cursor.fetchone()   
            return count,result 
        except Exception as ex:
            logger.error(msg="MySQL查询失败: {ex} sql:{sql}".format(ex=ex,sql=sql))
            result = None
        finally:
            return result
    
    def get_variables(self):
        rc, rs =  self.queryAll(sql='show global variables;')
        dataList = []
        if rc != 0 and rs != None:
            for rcd in rs:
                dataList.append(rcd)        
        data_dict={}
        for item in dataList:
            data_dict[item[0]] = item[1]
        return data_dict            
    
    def get_status(self):
        rc, rs = self.queryAll(sql='show global status;')    
        dataList = []
        if rc != 0 and rs != None:
            for rcd in rs:
                dataList.append(rcd)
        data_dict={}
        for item in dataList:
            data_dict[item[0]] = item[1]
        return data_dict           

    def get_wait_threads(self):
        rs = self.queryOne(sql="select count(1) as count from information_schema.processlist where state <> '' and user <> 'repl' and time > 2;")        
        if rs != None:return rs
        else:return {} 

    def get_master_satus(self):
        rs = self.queryOne(sql="show master status;")          
        if rs != None:return rs
        else:return {}
    
    def get_repl_status(self):
        rs = self.queryOne(sql='show slave status;')             
        if rs != None:return rs
        else:return {}    
    
    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as ex:
            print(ex)

              
            
if __name__=='__main__':   
    import Queue
    rs = []
#     mysql234 = MySQLThread('192.168.88.234',3306,'vmanage','root','welliam')
#     print mysql234.execute(sql='show tables;', num=1000)
    queue = Queue.Queue(maxsize=100)
#     mysql234 = MySQLThread('192.168.88.234',3306,'vmanage','root','welliam','show tables;',1000,queue)
#     mysql230 = MySQLThread('192.168.88.230',3306,'opsmanage','root','welliam','show tables;',1000,queue)
#     mysql234.start()
#     mysql230.start()
#     while True:
#         while not queue.empty():
#             rs.append(queue.get())
#         '''等待结果返回'''
#         if  0 < len(rs) >= 2:break    
#     print rs

    mysql234 = MySQLPool('192.168.88.234',3306,'root','welliam','vmanage','show tables;',1000,'queryMany',queue)
    mysql230 = MySQLPool('192.168.88.230',3306,'root','welliam','opsmanage','show tables;',1000,'queryMany',queue)
    mysql234.start()
    mysql230.start()
    while True:
        while not queue.empty():
            rs.append(queue.get())
        '''等待结果返回'''
        if  0 < len(rs) >= 2:break    
    print(rs)    