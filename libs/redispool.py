# -*- coding=utf-8 -*-
import redis
from utils.logger import logger
from rediscluster import RedisCluster

class RedisPool: 
    def __init__(self, dbServer): 
        self.dbServer = dbServer
        self.host = dbServer["ip"]
        self.db = dbServer["db_name"].replace("db","")
        self.password = dbServer["db_passwd"]
        self.port = dbServer["db_port"]  
        
    def cluster_connect(self, host=None, port=None, password=None):
        password = (password or self.password)
        host = (host or self.host)
        port = (port or self.port)
        startup_nodes = [{"host": host, "port": port}]
        try:
            conn = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, password=password)
            return conn
        except Exception as ex:
            logger.error("连接数据库失败: {ex}".format(ex=ex.__str__()))
            raise ex.__str__()
    
    def cluster_nodes(self):
        dataList = []
        cnx = self.cluster_connect()
        nodes = cnx.cluster_nodes()
        ms = {}
        for r in nodes: 
            nid = r.get('id')
            node = ms.get(nid, {}) 
            node['info'] = r
            ms[nid] = node
            if 'slave' in r.get('flags'):
                mid = r.get('master')
                ms[mid] = ms.get(mid, {})
                mslave = ms[mid].get('slave', []) 
                mslave.append(r)
                ms[mid]['slave'] = mslave
        
        
        for nid, r in ms.items():
            node = r['info']
            slave = r.get('slave', [])
            data = {}
            if 'master' in node.get('flags'):
                data["host"] = node.get('host')
                data["port"] = node.get('port')
                data["slot"] = len(node.get('slots'))
                data["slave"] = [{"host":s['host'],"port":s['port']}  for s in slave]
                dataList.append(data)      
        return  dataList

    def _connect_remote(self, host=None, port=None, password=None, db=None):
        host = (host or self.host)
        port = (port or self.port)          
        db = (db or self.db)
        password = (password or self.password)
        try:
            return redis.StrictRedis(host=host, port=port,db=db, password=password)   
        except redis.ConnectionError as ex:
            logger.error("连接数据库失败: {ex}".format(ex=ex.__str__()))
            raise redis.ConnectionError(ex)        
        

    def execute(self, cmd):
#         if self.dbServer.get('db_type') == 'cluster':
#             cnx = self.cluster_connect()
#         else:
#             cnx = self._connect_remote()     
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
        
class RedisClusterPool:   
    def __init__(self, dbServer): 
        self.dbServer = dbServer
        self.dbname = dbServer["db_name"]
        self.password = dbServer["db_passwd"]
        self.port = dbServer["db_port"]        
        self.connect()
        
    def connect(self, password=None, host=None, port=None):
        password = (password or self.password)
        host = (host or self.host)
        port = (port or self.port)
        startup_nodes = [{"host": host, "port": port}]
        try:
            conn = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, password=password)
            if hasattr(self, 'conn'):
                del self.conn
            self.conn = conn
        except Exception as ex:
            logger.error("连接数据库失败: {ex}".format(ex=ex.__str__()))
            raise ex.__str__()
    
    def cluster_nodes(self):
        nodes = self.conn.cluster_nodes()
        ms = {}
        for r in nodes: 
            nid = r.get('id')
            node = ms.get(nid, {}) 
            node['info'] = r
            ms[nid] = node
            if 'slave' in r.get('flags'):
                mid = r.get('master')
                ms[mid] = ms.get(mid, {})
                mslave = ms[mid].get('slave', []) 
                mslave.append(r)
                ms[mid]['slave'] = mslave
        
        
        
        for nid, r in ms.iteritems():
            node = r['info']
            slave = r.get('slave', [])
            if 'master' in node.get('flags'):
                slave = ', '.join( ['%s:%s:%s' %(s['host'], s['port'], s['id']) for s in slave])
                print('%s %s:%s \t%s \tslave: %s' %(node['id'], node.get('host'), node.get('port'), len(node.get('slots')), slave))
        