#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
from asset.models import Project_Assets,Service_Assets      

class IPVS_CONFIG(models.Model):   
    scheduler_mode = (
                ('sh',u'地址哈希'),
                ('rr',u'轮训'),
                ('wrr',u'加权轮询'),        
                ('lc',u'最少连接'),        
                ('wlc',u'加权最少链接'),        
                )  
    protocol_type = (
                ('-t',u'TCP'),
                ('-u',u'UDP'),
                )  
        
    ipvs_assets = models.ForeignKey('asset.Assets',related_name='ipvs_total', on_delete=models.CASCADE,verbose_name='assets_id')
    vip = models.CharField(max_length=100,verbose_name='VIP')
    port = models.IntegerField(verbose_name='端口')
    scheduler = models.CharField(choices=scheduler_mode,max_length=10,verbose_name='调度算法')
    protocol = models.CharField(choices=protocol_type,max_length=10,verbose_name='tcp/udp',default='-t')   
    persistence = models.IntegerField(verbose_name='转发模式',blank=True,null=True)
    line =  models.CharField(max_length=100,verbose_name='线路描述',blank=True,null=True)
    desc = models.CharField(max_length=200,verbose_name='备注',blank=True,null=True)
    is_active = models.SmallIntegerField(verbose_name='激活',default=0)
    class Meta:
        db_table = 'opsmanage_ipvs_config'
        default_permissions = ()
        permissions = (
            ("ipvs_read_ipvs_config", "读取IPVS信息表权限"),
            ("ipvs_change_ipvs_config", "更改IPVS信息表权限"),
            ("ipvs_add_ipvs_config", "添加IPVS信息表权限"),
            ("ipvs_delete_ipvs_config", "删除IPVS信息表权限"),     
        )
        unique_together = (("vip", "port", "ipvs_assets"))
        verbose_name = '应用管理'  
        verbose_name_plural = 'IPVS信息表'
    
    def project(self):
        try:
            return Project_Assets.objects.get(id=self.ipvs_assets.project).project_name
        except:
            return "未知"    
    
    def business(self):
        try:
            return Service_Assets.objects.get(id=self.ipvs_assets.business).service_name
        except:
            return "未知"              
    
    def to_json(self):
        try:
            sip = self.ipvs_assets.server_assets.ip
        except:
            sip = '未知'
        json_format = {
            "id":self.id,
            "sip":sip,
            "vip":self.vip,
            "port":self.port,
            "project":self.project(),
            "protocol":self.protocol,           
            "scheduler":self.scheduler,
            "persistence":self.persistence,
            "ipvs_assets":self.ipvs_assets.id,
            "line":self.line,
            "desc":self.desc,
            "is_active":self.is_active
        }
        return  json_format 
    
    def add_vip(self):
        if self.persistence:
            return "ipvsadm -A {protocol} {vip}:{port} -s {scheduler} -p {persistence}".format(protocol=self.protocol,vip=self.vip,port=self.port,scheduler=self.scheduler,persistence=self.persistence)
        return "ipvsadm -A {protocol} {vip}:{port} -s {scheduler}".format(protocol=self.protocol,vip=self.vip,port=self.port,scheduler=self.scheduler)
    
    def modf_vip(self):
        if self.persistence:
            return "ipvsadm -E {protocol} {vip}:{port} -s {scheduler} -p {persistence}".format(protocol=self.protocol,vip=self.vip,port=self.port,scheduler=self.scheduler,persistence=self.persistence)        
        return "ipvsadm -E {protocol} {vip}:{port} -s {scheduler}".format(protocol=self.protocol,vip=self.vip,port=self.port,scheduler=self.scheduler)
    
    def del_vip(self):
        return "ipvsadm -D {protocol} {vip}:{port}".format(protocol=self.protocol,vip=self.vip,port=self.port)    
    
    def stats_vip(self):
        return "ipvsadm -ln {protocol} {vip}:{port} --stats".format(protocol=self.protocol,vip=self.vip,port=self.port)
    
    def rate_vip(self):
        return "ipvsadm -ln {protocol} {vip}:{port} --rate".format(protocol=self.protocol,vip=self.vip,port=self.port)    
        
class IPVS_RS_CONFIG(models.Model):   
    forword_type = (
                ('-m',u'NAT'),
                ('-g',u'DR'),
                ('-i',u'TUN'),
                ('-b',u'FULLNAT'),
                )      
    ipvs_vip = models.ForeignKey('IPVS_CONFIG',related_name='ipvs_rs', on_delete=models.CASCADE,verbose_name='vip_id')
    rs_assets =  models.ForeignKey('asset.Assets',related_name='ipvs_realserver_total', on_delete=models.CASCADE,verbose_name='assets_id')
    ipvs_fw_ip = models.CharField(max_length=100,verbose_name='VIP')
    forword =  models.CharField(choices=forword_type,max_length=10,verbose_name='转发模式')
    weight = models.SmallIntegerField(verbose_name='权重',default=0)
    is_active = models.IntegerField(verbose_name='激活',default=0)
    class Meta:
        db_table = 'opsmanage_ipvs_rs_config'
        default_permissions = ()  
        unique_together = (("ipvs_vip", "ipvs_fw_ip")) 
        verbose_name = '应用管理'  
        verbose_name_plural = 'IPVS_RS_信息表'  

    def project(self):
        try:
            return Project_Assets.objects.get(id=self.rs_assets.project).project_name
        except:
            return "未知"    
    
    def business(self):
        try:
            return Service_Assets.objects.get(id=self.rs_assets.business).service_name
        except:
            return "未知" 

    def to_assets(self):
        try:
            sip = self.rs_assets.server_assets.ip
        except:
            sip = '未知'        
        json_format = {
            "id":self.rs_assets.id,
            "ip":sip,
            "project":self.project(),
            "service":self.business(),
        }
        return  json_format 

    def to_json(self):
        try:
            sip = self.rs_assets.server_assets.ip
        except:
            sip = '未知'
        json_format = {
            "sip":sip,           
            "fip":self.ipvs_fw_ip,
            "forword":self.forword,
            "weight":self.weight,
            "is_active":self.is_active
        }
        return  json_format

    def add_realsever(self):
        return "ipvsadm -a {protocol} {vip}:{port} -r {ipvs_fw_ip}:{port} {forword} -w {weight}".format(vip=self.ipvs_vip.vip,port=self.ipvs_vip.port,
                                                                                                        protocol=self.ipvs_vip.protocol,ipvs_fw_ip=self.ipvs_fw_ip,
                                                                                                        forword=self.forword,weight=self.weight)
    
    def modf_realsever(self):
        return "ipvsadm -e {protocol} {vip}:{port} -r {ipvs_fw_ip}:{port} {forword} -w {weight}".format(vip=self.ipvs_vip.vip,protocol=self.ipvs_vip.protocol,
                                                                                                           port=self.ipvs_vip.port,ipvs_fw_ip=self.ipvs_fw_ip,
                                                                                                           forword=self.forword,weight=self.weight)
    
    def del_realsever(self):
        return "ipvsadm -d {protocol} {vip}:{port} -r {ipvs_fw_ip}:{port}".format(vip=self.ipvs_vip.vip,protocol=self.ipvs_vip.protocol,port=self.ipvs_vip.port,ipvs_fw_ip=self.ipvs_fw_ip)
              
class IPVS_NS_CONFIG(models.Model):
    ipvs_vip = models.ForeignKey('IPVS_CONFIG',related_name='ipvs_ns_total', on_delete=models.CASCADE,verbose_name='vip_id')  
    nameserver = models.CharField(max_length=100,verbose_name='nameserver',blank=True,null=True)
    desc = models.CharField(max_length=200,verbose_name='备注',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_ipvs_ns_config'
        default_permissions = ()   
        unique_together = (("ipvs_vip", "nameserver")) 
        verbose_name = '应用管理' 
        verbose_name_plural = 'IPVS_NS_信息表'          
        
class IPVS_OPS_LOG(models.Model):
    ipvs_vip = models.ForeignKey('IPVS_CONFIG',related_name='ipvs_ops_total', on_delete=models.CASCADE,verbose_name='vip_id')  
    user = models.IntegerField(verbose_name='操作用户',default=0)
    cmd = models.CharField(max_length=500,verbose_name='VIP')
    status = models.IntegerField(verbose_name='操作状态',default=0)
    class Meta:
        db_table = 'opsmanage_ipvs_ops_log'
        default_permissions = ()   
        verbose_name = '应用管理' 
        verbose_name_plural = 'IPVS操作记录表'         