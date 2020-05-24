# -*- coding=utf-8 -*-
import redis
from utils.logger import logger

class RedisPool: 
    def __init__(self, dbServer): 
        self.dbServer = dbServer
          
    def _connect_remote(self):
        try:
            return redis.StrictRedis(host=self.dbServer["ip"], port=self.dbServer["db_port"],db=self.dbServer["db_name"].replace("db",""), password=self.dbServer["db_passwd"])   
        except redis.ConnectionError as ex:
            logger.error("连接数据库失败: {ex}".format(ex=ex.__str__()))
            raise redis.ConnectionError(ex)        
        

    def execute(self, cmd):
        cnx = self._connect_remote()       
        try:
            return cnx.execute_command(cmd)
        except redis.RedisError as ex:
            logger.error("数据库操作失败: {ex}".format(ex=ex.__str__())) 
            return ex.__str__()
        #会自动释放，不需要再显示关闭连接                
#         finally:
#             cnx.close()

    def find_big_keys(self, key_length):
        cnx = self._connect_remote()
        dataList = []
        i = 0
        scan_val = cnx.scan(cursor=i,count=1000)
        while scan_val[0] > 0 :
            i = scan_val[0]
            try:
                pipe = cnx.pipeline(transaction=False)
                for k in scan_val[1]:
                    pipe.debug_object(k)
                exec_val = pipe.execute()
                x = 0
                for keys in exec_val:    
                    key = scan_val[1][x]        
                    length = keys.get("serializedlength")
                    if length > key_length:
                        dataList.append({"name":key,"length":length})
                    x = x + 1
            except Exception as ex:
                logger.error(ex.__str__()) 
            scan_val = cnx.scan(cursor=i,count=1000)
#             time.sleep(0.05)
    
    def format_result(self, result):
                
        if isinstance(result, bytes):
            return result.decode('utf-8').replace('\n','\n\r')
            
        elif isinstance(result, list):
            results, count = '', 1
            for rs in result:
                rresults, rcount = '', 1
                if isinstance(rs, list):
                    s = ' '
                    for rr in rs:  
                        if isinstance(rr, bytes):
                            rr = rr.decode('utf-8')
                        else:
                            rr = str(rr)
                        if rcount > 1: s = '    '
                        rresults =  rresults + s + str(rcount) +") \""  + rr  + '"\n\r'
                        rcount = rcount + 1
                    if len(rresults) > 0:
                        results = results  + str(count) +") " + rresults
                else:
                    results = results + str(count) +") \"" + rs.decode('utf-8')  + '"\n\r'
                count = count + 1
                
            return results 
                
        else:            
            return str(result) 