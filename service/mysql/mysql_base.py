#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from libs.sqlpool import MySQLPool
from utils.logger import logger

class MySQLBase(MySQLPool):
    
    slave_key_list = [
                  'slave_io_state','master_host','master_user','master_port','connect_retry','master_log_file',
                  'read_master_log_pos','relay_master_log_file','exec_master_log_pos','seconds_behind_master',
                  'slave_io_running','slave_sql_running','replicate_do_db','slave_sql_running_state','replicate_ignore_db',
                  'relay_log_pos'
            ]
    
    def get_processlists(self):
        try:
            sql = """select id,user,host,db,time,state,command,info from information_schema.processlist;"""
            return self.queryMany(sql)
        except Exception as ex:
            logger.error(ex.__str__())
            return -1 
        
    def get_db_size(self):
        dataList = []
        db_size = self.execute_for_query(sql="""SELECT table_schema, Round(Sum(data_length + index_length) / 1024 / 1024, 1) as size,count(TABLE_NAME) as total_table
                                            FROM information_schema.tables where table_schema not in ("performance_schema","information_schema","mysql","sys")
                                            GROUP BY table_schema;""") 
        for ds in db_size[1]:
            dataList.append({"db_name":ds[0],"size":ds[1],"total_table":ds[2]})
        return dataList   
    
    def get_db_tables(self,dbname):
        dataList = []
        data = self.execute_for_query(sql="""SELECT TABLE_NAME,TABLE_COMMENT,ENGINE,ROW_FORMAT,CREATE_TIME,TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='{dbname}';""".format(dbname=dbname)) 
        for ds in data[1]:
            dataList.append({"TABLE_NAME":ds[0],"TABLE_COMMENT":ds[1],"ENGINE":ds[2],"ROW_FORMAT":ds[3],"CREATE_TIME":ds[4],"TABLE_ROWS":ds[5]})
        return dataList        
    
    def get_db_table_info(self,dbname):
        dataList = []
        data = self.execute_for_query(sql="""select table_schema,table_name,table_rows,round((DATA_LENGTH+INDEX_LENGTH)/1024/1024,2) as size,engine,row_format,table_collation  
                                            from information_schema.tables where table_schema = '{dbname}' order by table_rows desc;""".format(dbname=dbname))
        for ds in data[1]:
            dataList.append({"db_name":ds[0],"table_name":ds[1],"table_rows":ds[2],"table_size":ds[3],"engine":ds[4],"row_format":ds[5],"table_collation":ds[6]})
        return dataList  
    
    def get_db_table_columns(self,dbname, table_name):
        dataList = []
        data = self.execute_for_query(sql="""SELECT COLUMN_NAME,COLUMN_TYPE,ifnull(COLUMN_DEFAULT,''),IS_NULLABLE,EXTRA,COLUMN_KEY,COLUMN_COMMENT
                                             FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{dbname}' AND TABLE_NAME='{table_name}';""".format(dbname=dbname,table_name=table_name))
        for ds in data[1]:
            dataList.append({"COLUMN_NAME":ds[0],"COLUMN_TYPE":ds[1],"COLUMN_DEFAULT":ds[2],"IS_NULLABLE":ds[3],"EXTRA":ds[4],"COLUMN_KEY":ds[5],"COLUMN_COMMENT":ds[6]})
        return dataList      

    def get_tables(self):
        data = self.queryMany('show tables',10000) 
        return data        
    
    def get_table_schema(self, dbname, table): 
        data = self.queryMany(sql="""SELECT TABLE_SCHEMA,TABLE_NAME,TABLE_TYPE,ENGINE,VERSION,ROW_FORMAT,
                                                    TABLE_ROWS,concat(round(sum(DATA_LENGTH/1024/1024),2),'MB') AS DATA_LENGTH,
                                                    MAX_DATA_LENGTH,concat(round(sum(INDEX_LENGTH/1024/1024),2),'MB') AS INDEX_LENGTH,
                                                    DATA_FREE,AUTO_INCREMENT,CREATE_TIME,TABLE_COLLATION,TABLE_COMMENT FROM information_schema.TABLES 
                                                    WHERE  TABLE_SCHEMA='{db}' AND TABLE_NAME='{table}';""".format(db=dbname,table=table),num=1000)
        return data  
    
    def get_table_index(self, table):
        data = self.queryMany(sql="""SHOW index FROM `{table}`;""".format(table=table),num=1000)
        return data         
    
    
    def get_table_desc(self, table):
        data = self.queryMany(sql="""show create table `{table}`;""".format(table=table),num=1000)
        return data   
    
    def get_status(self):
        status = self.execute_for_query(sql='show status;')
        dataList = []
        for ds in status[1]:
            data = {}
            data['value'] = ds[1]
            data['name'] = ds[0].capitalize() 
            dataList.append(data)     
        return dataList

    def get_global_status(self):
        dataList = []
        logs = self.execute_for_query(sql='show global variables;')
        for ds in logs[1]:
            data = {}
            data['value'] = ds[1]
            data['name'] = ds[0].capitalize()
            dataList.append(data)        
        return dataList

    def get_master_status(self):
        masterList = []
        master_status = self.execute_for_query(sql='show master status;')
        slave_host = self.execute_for_query(sql="SELECT host FROM INFORMATION_SCHEMA.PROCESSLIST WHERE COMMAND='Binlog Dump';")
        if master_status[1]:
            count = 0
            for ds in master_status[2]:
                data = {}
                data["name"] = ds
                data["value"] = master_status[1][0][count]
                count = count + 1
                masterList.append(data)
        if slave_host[1]:
            sList = []
            for ds in slave_host[1]:
                sList.append(ds[0])
            masterList.append({"name":"Slave","value":sList})    
        return  masterList      
    
    def get_slave_status(self):
        slaveList = []
        slave_status = self.execute_for_query(sql="show slave status;")  
        if slave_status[1]:
            count = 0
            for ds in slave_status[2]:
                data = {}
                if ds.lower() in self.slave_key_list:
                    data["name"] = ds
                    data["value"] = slave_status[1][0][count]
                    slaveList.append(data)
                count = count + 1 
        return  slaveList                     
        
    
class MySQLARCH(object):
    def __init__(self, mysql, db_server):
        super(MySQLARCH,self).__init__()  
        self.mysql = mysql
        self.mysql_status = self.mysql.get_status()
        self.db_server = db_server
        self.arch_info = {
                    'title': self.db_server.get("db_mark"),
                    'className': 'product-dept',
                    'children': []                   
                }
    
    def slave(self):
        slave_data = {}
        for ds in self.mysql.get_master_status():
            if ds.get('name') == 'Slave':slave_data[self.db_server.self.db_server.get("ip")+':'+str(self.db_server.get("db_port"))] = ds.get('value')  
        return slave_data
        
    def pxc(self):
        self.arch_info["name"] = 'PXC模式'
        pxc_server_list =  []
        for ds in self.mysql_status[1]:
            if ds.get('name') == 'Wsrep_incoming_addresses':pxc_server_list = ds.get('value').split(',')
        for s in pxc_server_list:
            data = {}
            host = s.split(':')[0]
            port = s.split(':')[1]
            data['name'] = host
            data['title'] = port
            data['children'] = []
            if s in self.slave().keys():
                data['name'] = 'master'
                data['title'] = host+':'+port
                count = 1
                for d in self.slave().get(s):
                    x = {}
                    host = d.split(':')[0]
                    port = d.split(':')[1]
                    x['name'] = 'slave-' + str(count)
                    x['title'] =  host+':'+port
                    count = count + 1
                    data['children'].append(x)                                                             
            self.arch_info['children'].append(data) 
        return  self.arch_info  
    
    def master_slave(self):
        count = 1
        self.arch_info["name"] = '主从模式'
        for m in self.mysql.get_slave_status():
            if m.get('name') == 'Master_Host':
                self.arch_info['children'].append({"name":'Master-' + str(count),"title":m.get('value')})
                count = count + 1
        for ds in self.mysql.get_master_status():
            if ds.get('name') == 'Slave':
                count = 1
                for s in ds.get('value'):
                    x = {}
                    host = s.split(':')[0]
                    port = s.split(':')[1]
                    x['name'] = 'slave-' + str(count)
                    x['title'] =  host+':'+port 
                    count = count + 1  
                    self.arch_info['children'].append(x)   
        return  self.arch_info  
    
    def single(self):
        self.arch_info["name"] = '单例模式'
        return  self.arch_info    