# -*- coding=utf-8 -*-
import time, operator
import redis, rediscluster
from utils.logger import logger
from rediscluster import RedisCluster
from rediscluster.exceptions import (
    RedisClusterException, AskError, MovedError, ClusterDownError,
    ClusterError, TryAgainError
)

from redis.exceptions import RedisError, ResponseError, TimeoutError, DataError, ConnectionError, BusyLoadingError

class RedisPoolBase:
    def __init__(self, dbServer): 
        self.dbServer = dbServer
        self.host = dbServer["ip"]
        self.db = dbServer.get("db_name").replace("db","")
        self.password = dbServer["db_passwd"]
        self.port = dbServer["db_port"] 

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

    def prompt(self, host=None, port=None, db=None):
        host = (host or self.host)
        port = (port or self.port)
        if self.db:
            return '{}:{}[{}]> '.format(host, port, self.db)
        else:
            return '{}:{}> '.format(host, port)
    
    def format_result(self, result):
               
        def format_list(results, ss):
            rresults, rcount = '', 1
            for rr in results: 
                if isinstance(rr, bytes):
                    rr = rr.decode('utf-8')
                elif isinstance(rr, int):
                    rr = '(integer) {}'.format(rr) 
                elif isinstance(rr, list):      
                    rr = format_list(rr, ss + ' '*3)
                else:
                    rr = '"{}"'.format(rr)
                if rcount > 1: 
                    rresults =  rresults + ss + str(rcount) + ') ' +  rr  + '\n\r'
                else:
                    rresults =  str(rcount) + ') ' +  rr  + '\n\r'
                rcount = rcount + 1
            return rresults                
                
        if isinstance(result, bytes):
            return result.decode('utf-8').replace('\n','\n\r')
                       
        elif isinstance(result, list):
            results, count = '', 1
            for rs in result:
                if isinstance(rs, list):
                    rresults = format_list(rs,' '*3)[:-2].replace('\n\r\n\r','\n\r')    
                    results = results  + str(count) +") " + rresults
                else:
                    results = results + str(count) +") \"" + rs  + '"\n\r'
                count = count + 1
                
            return results 
                
        else:            
            return str(result)        

class RedisStandalonePool(RedisPoolBase): 
    def __init__(self, dbServer): 
        self.dbServer = dbServer
        self.host = dbServer["ip"]
        self.db = dbServer["db_name"].replace("db","")
        self.password = dbServer["db_passwd"]
        self.port = dbServer["db_port"]  
             

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

    def close(self):
        pass

    
 
        
                
class RedisClusterPool(rediscluster.RedisCluster,RedisPoolBase):
    def __init__(self, dbServer):
        
        self.dbServer = dbServer
        self.host = dbServer["ip"]
        self.password = dbServer["db_passwd"]
        self.db = None
        self.port = dbServer["db_port"]          
        self.node = {'host': self.host, 'port': self.port, 'name': self.host + ':' + str(self.port)}
        
        try:
            super().__init__(host=self.host, port=self.port, decode_responses=True, password=self.password)
        except rediscluster.exceptions.RedisClusterException:
            return '(error) ERR could not connect to redis at {}:{}'.format(self.host, self.port)
    
    def get_command_keys(self):
        return list(self.RESULT_CALLBACKS.keys()) + list(self.NODES_FLAGS.keys()) + list(self.CLUSTER_COMMANDS_RESPONSE_CALLBACKS.keys())
    
    def cluster_node(self):
        dataList = []
        nodes = self.cluster_nodes()
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

    def execute_commands(self, node=None, slot=False ,*args, **kwargs):
        """
        Send a command to a node in the cluster
        """
        if not args:
            raise RedisClusterException("Unable to determine command to use")

        command = args[0]
        # If set externally we must update it before calling any commands
        if self.refresh_table_asap:
            self.connection_pool.nodes.initialize()
            self.refresh_table_asap = False

        redirect_addr = None
        asking = False
        is_read_replica = False

        try_random_node = False
        ttl = int(self.RedisClusterRequestTTL)

        while ttl > 0:
            ttl -= 1
            if asking:
                node = self.connection_pool.nodes.nodes[redirect_addr]
                r = self.connection_pool.get_connection_by_node(node)
            elif try_random_node:
                r = self.connection_pool.get_random_connection()
                try_random_node = False
            else:
                if self.refresh_table_asap:
                    # MOVED
                    node = self.connection_pool.get_master_node_by_slot(slot)
                r = self.connection_pool.get_connection_by_node(node)

            try:
                if asking:
                    r.send_command('ASKING')
                    self.parse_response(r, "ASKING", **kwargs)
                    asking = False
                if is_read_replica:
                    r.send_command('READONLY')
                    self.parse_response(r, 'READONLY', **kwargs)
                    is_read_replica = False
                try:
                    r.send_command(*args)
                    return self.parse_response(r, command, **kwargs)
                except Exception as ex:
                    return "(error) ERR wrong number of arguments for '{}' "'command'.format(command)
            except (RedisClusterException, BusyLoadingError) as ex:
                return ex.__str__()
            except (ConnectionError, TimeoutError):
                try_random_node = True

                if ttl < self.RedisClusterRequestTTL / 2:
                    time.sleep(0.1)
            except ClusterDownError as e:
                self.connection_pool.disconnect()
                self.connection_pool.reset()
                self.refresh_table_asap = True

                raise e
            except MovedError as e:
                self.refresh_table_asap = True
                self.connection_pool.nodes.increment_reinitialize_counter()

                node = self.connection_pool.nodes.set_node(e.host, e.port, server_type='master')
                self.connection_pool.nodes.slots[e.slot_id][0] = node
            except TryAgainError as e:
                if ttl < self.RedisClusterRequestTTL / 2:
                    time.sleep(0.05)
            except AskError as e:
                redirect_addr, asking = "{0}:{1}".format(e.host, e.port), True
            finally:
                self.connection_pool.release(r)

        return ClusterError('TTL exhausted.')

    def execute(self, payload):
        
        past_node = self.node
        
        payload = payload.split()
        
        cmd, *args =  payload
        
        move_str = ''
        
        if cmd.upper() in self.get_command_keys():
            slot = False  
        
        elif len(payload) > 1:
            
            cmds = payload[0].strip().upper() + ' ' + payload[1].strip().upper()
            
            if cmds in self.get_command_keys():
                slot = False 
                
            else:
                slot = self._determine_slot(*payload)
                self.node = self.connection_pool.get_node_by_slot(slot, self.read_from_replicas and (command in self.READ_COMMANDS))
                self.host, self.port = self.node.get('host'), self.node.get('port')   
                move_str = '-> Redirected to slot [{slot}] located at {host}:{port}'.format(slot=slot,host=self.host,port=self.port)               
        
        else:
            slot = False    
                
        try:
            ret = self.execute_commands(self.node, slot, cmd, *args)

            if not ret:
                return '(empty list or set)'
            else:
                if move_str and operator.ne(past_node, self.node): 
                    return  move_str + '\r\n' + self.format_result(ret)
                else:
                    return self.format_result(ret)
        except AttributeError:
            return "(error) ERR unknown command '{}'".format(cmd)
            
    def close(self):
        pass
#         self.connection_pool.close()   

class RedisPool:
    def __init__(self,dbServer):
        self.dbServer = dbServer
        super(RedisPool, self).__init__() 
    
    def start_up(self, dbServer=None):
        dbServer = (dbServer or self.dbServer)        
        if dbServer.get('db_mode','ms') == 'cluster':
            return RedisClusterPool(dbServer)
        else:
            return RedisStandalonePool(dbServer)
             
        