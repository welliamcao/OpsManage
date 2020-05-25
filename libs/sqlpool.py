# -*- coding=utf-8 -*-
import sqlparse, pymysql, time
from utils.logger import logger
from pymysql.constants import FIELD_TYPE
from pymysql.converters import (convert_mysql_timestamp, convert_datetime,
                                convert_timedelta, convert_date, conversions,
                                decoders)
from prettytable import PrettyTable
from prettytable import DEFAULT
FIELD_TYPES = decoders.copy()
FIELD_TYPES.update({
    FIELD_TYPE.NULL: type(None)
})

class MySQLPool: 
    def __init__(self,dbServer, sql=None, num=1000):    
        self.sql = sql
        self.num = num 
        self.dbServer = dbServer

    def __connect_remote(self):
        try:
            return pymysql.connect(
                                   host=self.dbServer["ip"],
                                   user=self.dbServer["db_user"],
                                   password=self.dbServer["db_passwd"],
                                   port=self.dbServer["db_port"],
                                   db=self.dbServer["db_name"],
                                   max_allowed_packet=1024 * 1024 * 1024,
                                   charset='utf8')   
        except pymysql.Error as ex:
            logger.error("连接数据库失败: {ex}".format(ex=ex.__str__()))
            raise pymysql.Error(ex.__str__())        
        
    def queryAll(self,sql, num=1000):  
        
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)   
                result = cursor.fetchall()   
                return (count,result) 
        except pymysql.Error as ex:
            logger.error("数据库查询失败: {ex}".format(ex=str(ex))) 
            return ex.__str__()  
                    
        finally:
            cnx.close()  
   
    def queryOne(self,sql,num=1000):  
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)   
                result = cursor.fetchone()   
                return (count,result) 
        except pymysql.Error as ex:
            logger.error("数据库查询失败: {ex}".format(ex=str(ex)))
            return ex.__str__()
                      
        finally:
            cnx.close()  
  
   
    def queryMany(self,sql, num=1000, param=None):
        
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)
                index = cursor.description
                colName = []
                for i in index:
                    colName.append(i[0])            
                result = cursor.fetchmany(size=num) 
                return (count,result,colName)
        except pymysql.Error as ex:
            logger.error("数据库查询失败: {ex}".format(ex=str(ex)))  
            return ex.__str__()
                       
        finally:
            cnx.close()        
    
    def execute_for_query(self,sql,num=1000):
        
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)
                index = cursor.description
                colName = []
                if index:
                    for i in index:
                        colName.append(i[0]) 
                result = cursor.fetchmany(size=num)           
                return (count,result,colName) 
        except pymysql.Error as ex:
            logger.error("数据库操作失败: {ex}".format(ex=str(ex))) 
            return ex.__str__()
        
        finally:
            cnx.close()
       
         
    def execute(self,sql,num=1000):
               
        cnx = self.__connect_remote()
        
        try:
            with cnx.cursor() as cursor:
                count = cursor.execute(sql)
                index = cursor.description
                colName = []
                if index:
                    for i in index:
                        colName.append(i[0]) 
                result = cursor.fetchmany(size=num)           
                cnx.commit()
                return (count,result,colName) 
        except pymysql.Error as ex:
            logger.error("数据库操作失败: {ex}".format(ex=str(ex))) 
            return ex.__str__()
                        
        finally:
            cnx.close()
    
    def get_value(self):
        pass
    
    
class SQLExecute(object):
    #这个类用来处理websocket长连接请求
    start_time = None

    def __init__(self, dbServer, websocket=None):       
        self.dbname = dbServer["db_name"]
        self.user = dbServer["db_user"]
        self.password = dbServer["db_passwd"]
        self.host = dbServer["ip"]
        self.port = dbServer["db_port"]
        self.charset = 'utf8'
        self.connect()
        self.websocket = websocket

    def connect(self, database=None, user=None, password=None, host=None, port=None, charset=None):
        db = (database or self.dbname)
        user = (user or self.user)
        password = (password or self.password)
        host = (host or self.host)
        port = (port or self.port)
        charset = (charset or self.charset)
        conv = conversions.copy()
        conv.update({
            FIELD_TYPE.TIMESTAMP: lambda obj: (convert_mysql_timestamp(obj) or obj),
            FIELD_TYPE.DATETIME: lambda obj: (convert_datetime(obj) or obj),
            FIELD_TYPE.TIME: lambda obj: (convert_timedelta(obj) or obj),
            FIELD_TYPE.DATE: lambda obj: (convert_date(obj) or obj),
        })


        conn = pymysql.connect(
            database=db, user=user, password=password, host=host, port=port,
            use_unicode=True, charset=charset,autocommit=True, conv=conv,
            client_flag=pymysql.constants.CLIENT.INTERACTIVE,
            max_allowed_packet=1024 * 1024 * 1024,
        )

        if hasattr(self, 'conn'):
            self.conn.close()
        self.conn = conn

        self.dbname = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.charset = charset


    def sql_iter(self, sql):
        sqls = sqlparse.split(sql)
        while sqls:
            for sql in sqls:
                sql = sqls.pop(0)
                if sql.endswith(';'):sql = sql.strip(';')
                yield sql

    def execute(self, statement):
        
        statement = statement.strip()
        
        if not statement:
            yield (None, None, None, None)

        components = self.sql_iter(statement)
           
        for sql in components:

            if sql.endswith('\G'):
                sql = sql[:-2].strip()
            
            with self.conn.cursor() as cur:
                cur.execute(sql)
                self.start_time = int(time.time())
                while True:
                    yield self.get_result(cur)
    
                    if not cur.nextset() or (not cur.rowcount and cur.description is None):
                        break


    def get_result(self, cursor):
        title = headers = None
        costs = ' ({cost} sec)'.format(cost=round((time.time()-self.start_time),3))
        if cursor.description is not None:
            headers = [ x[0] for x in cursor.description]
            status = '{0} row{1} in set'
        else:
            
            status = 'Query OK, {0} row{1} affected'
        status = status.format(cursor.rowcount,
                               '' if cursor.rowcount == 1 else 's')
        return (title, cursor if cursor.description else None, headers, status + costs)

    def pretty_result(self, result):
        try:
            for title, cur, headers, status in result:
                table = PrettyTable(headers, encoding="utf8")
                table.padding_width = 10
                table.align[headers[0]] = 'l'
                for row in cur.fetchall():
                    table.add_row(list(row)) 
                table.set_style(DEFAULT)
                self.websocket.send(table.get_string().replace('\n','\n\r')+'\r\n'+status)              
        except Exception as ex:
            logger.error(ex.__str__())
            self.websocket.send("\033[31m " + ex.__str__() + "\033[0m")
                    
    def close(self):
        try:
            self.conn.close()
        except pymysql.MySQLError as ex:
            logger.error(ex.__str__())
        
if __name__ == "__main__":
    sql = SQLExecute( 
                      database='opsmanage', user="root",
                      host="192.168.10.133", password="xxxx", port=3306, socket=None, charset="utf8",                 
                      )
    sqls = '''select * from opsmanage_user;
                select * from opsmanage_wiki_tag;''' 
    count = 0
    while True:
        rs = sql.execute(sqls)
        sql.pretty_result(rs)       
        time.sleep(1)
        count = count  + 1
        if count > 10:
            sql.close()
            break      