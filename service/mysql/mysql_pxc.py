#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from service.mysql.mysql_status import MySQLStatus


class PXCWsrepUUID(MySQLStatus):
    """某个节点出现不同的值，说明此节点没有连接到集群中"""
    level = 'high'
    metric = None
    key_name = "wsrep_cluster_state_uuid"
    
class PXCWsrepClusterStatus(MySQLStatus):
    """集群节点的状态。如果不为"Primary，需要注意"""
    level = 'high'
    metric = None
    key_name = "wsrep_cluster_status" 
    
class PXCWsrepClusterSize(MySQLStatus):
    """集群节点的总数"""
    level = 'low'
    metric = None
    key_name = "wsrep_cluster_size"    
    
class PXCWsrepReady(MySQLStatus):
    """如果为ON可以正常使用SQL语句, 若为OFF, 需进一步检查wsrep_connected的值"""
    level = 'high'
    metric = None
    key_name = "wsrep_ready"     
    
class PXCWsrepConnected(MySQLStatus):
    """如果此变量的值为OFF，说明该节点还没有加入到任何一个集群"""
    level = 'high'
    metric = None
    key_name = "wsrep_connected"    
    
class PXCWsrepLocalStateComment(MySQLStatus):
    """正常的返回值是Joining, Waiting on SST, Joined, Synced or Donor，返回Initialized说明已不在正常工作状态"""
    level = 'mid'
    metric = None
    key_name = "wsrep_local_state_comment"  
        
class PXCWsrepLocalSendQueueAvg(MySQLStatus):
    """如果值偏高，说明网络连接可能是瓶颈"""
    level = 'mid'
    metric = None
    key_name = "wsrep_local_send_queue_avg"        

class PXCWsrepLocalRecvQueueAvg(MySQLStatus):
    """表示slave事务队列的平均长度，slave瓶颈的预兆"""
    level = 'mid'
    metric = None
    key_name = "wsrep_local_recv_queue_avg"  

class PXCWsrepFlowControlPausedns(MySQLStatus):
    """表示复制停止了多长时间，以纳秒为单位"""
    level = 'high'
    metric = None
    key_name = "wsrep_flow_control_paused_ns"   

class PXCWsrepFlowControlPaused(MySQLStatus):
    """表示复制停止了多长时间。即表明集群因为Slave延迟而慢的程度，值为0~1，越靠近0越好，值为1表示复制完全停止。可优化wsrep_slave_threads的值来改善"""
    level = 'high'
    metric = None
    key_name = "wsrep_flow_control_paused"  

class PXCWsrepFlowControlSent(MySQLStatus):
    """表示该节点已经停止复制了多少次"""
    level = 'high'
    metric = None
    key_name = "wsrep_flow_control_sent"   

class PXCWsrepFlowControlRecv(MySQLStatus):
    """表示该节点已经停止复制了多少次"""
    level = 'high'
    metric = None
    key_name = "wsrep_flow_control_recv" 

class PXCWsrepGcachePoolSize(MySQLStatus):
    """gcache动态分配的字节数"""
    level = 'low'
    metric = None
    key_name = "wsrep_gcache_pool_size" 

class PXCWsrepIncomingAddresses(MySQLStatus):
    """集群中的节点地址"""
    level = 'low'
    metric = None
    key_name = "wsrep_incoming_addresses"  
    