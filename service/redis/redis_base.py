#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from libs.redispool import RedisPool
from utils.logger import logger

class RedisBase(RedisPool):
    def __init__(self,dbServer):
        self.redis = self.start_up(dbServer)
    
    def get_db_size(self):
        cnx = self.redis._connect_remote()
        return cnx.info('keyspace')

    def get_info(self, section=None):
        cnx = self.redis._connect_remote()
        return cnx.info(section)
    
    def get_repl(self):
        return self.get_info(section='Replication')       
    
    def get_cluster_nodes(self):
        return self.redis.cluster_node()
    
class RedisInfo(RedisPool):
        
    def get_value(self, data):
        try:
            return data.get(self.key_name)
        except Exception as ex:
            logger.error(self.key_name + ': ' + ex.__str__())
            return -1    
        

        
class RedisArch(object):
    def __init__(self, redis, db_server):
        super(RedisArch,self).__init__()  
        self.redis = redis
        self.db_server = db_server
        self.arch_info = {
                    'title': self.db_server.get("db_mark"),
                    'className': 'product-dept',
                    'children': []                   
                }
    
    def slave(self):
        self.arch_info["name"] = '从库模式'
        redis_repl = self.redis.get_repl()
        self.arch_info['children'] = [{"name":"Master","title":redis_repl.get('master_host') + ':' + str(redis_repl.get('master_port')),"children":[]}]
        self.arch_info['children'][0]["children"].append({"title":'Slave',"name":self.db_server.get("ip") + ':' + str(self.db_server.get("db_port"))})
        return  self.arch_info          
            
    def master_slave(self):
        self.arch_info["name"] = '主从模式'
        redis_repl = self.redis.get_repl()
        if redis_repl.get('role') == 'master':
            self.arch_info['children'] = [{"name":"Master","title":self.db_server.get("ip") + ':' + str(self.db_server.get("db_port")),"children":[]}]
            if redis_repl.get('connected_slaves') > 0:
                for ds in range(0, redis_repl.get('connected_slaves')):
                    slave = redis_repl.get('slave' + str(ds))
                    self.arch_info['children'][0]["children"].append({"title":'State: {state}  Lag: {lag}'.format(state=str(slave.get('state')),lag=str(slave.get('lag'))),"name":slave.get('ip') + ':' + str(slave.get('port'))})
        if redis_repl.get('role') == 'slave':
            self.arch_info['children'] = [{"name":"Master","title":redis_repl.get('master_host') + ':' + str(redis_repl.get('master_port')),"children":[]}]
            self.arch_info['children'][0]["children"].append({"title":'Slave-0',"name":self.db_server.get("ip") + ':' + str(self.db_server.get("db_port"))})
        return  self.arch_info  
    
    def cluster(self):
        self.arch_info["name"] = '集群模式'
        for ds in self.redis.get_cluster_nodes():
            data = {"name":'Master / {slot}'.format(slot=ds.get('slot')),"title":ds.get("host") + ':' + str(ds.get("port")),'children':[]}
            if len(ds.get('slave')) > 0:
                for ds in ds.get('slave'):
                    data['children'].append({"name":'Slave',"title":ds.get("host") + ':' + str(ds.get("port"))})
            self.arch_info['children'].append(data)
        return  self.arch_info  
    
    def single(self):
        self.arch_info["name"] = '单例模式'
        self.arch_info['children'] = [{"title":"Master","name":self.db_server.get("ip") + ':' + str(self.db_server.get("db_port")),"children":[]}]
        return  self.arch_info  