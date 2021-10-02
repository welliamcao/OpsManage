#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
from asset.models import Business_Tree_Assets  
from datetime import datetime    
from account.models import User

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
    business = models.IntegerField(verbose_name='业务关联')
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
     
                
    def business_paths(self):
        try:
            business = Business_Tree_Assets.objects.get(id=self.business)
            return business.business_env() + '/' +business.node_path()
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
            "protocol":self.protocol,           
            "scheduler":self.scheduler,
            "persistence":self.persistence,
            "ipvs_assets":self.ipvs_assets.id,
            "business":self.business,
            "rs_count":self.ipvs_rs.all().count(),
            "business_paths":self.business_paths(),
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


    def to_assets(self):
        try:
            sip = self.rs_assets.server_assets.ip
        except:
            sip = '未知'        
        json_format = {
            "id":self.rs_assets.id,
            "ip":sip,
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
        
        
class APPLY_CENTER_CONFIG(models.Model): 
    id = models.AutoField(verbose_name='id',primary_key=True)
    apply_name = models.CharField(max_length=100,verbose_name='图标',unique=True) 
    apply_desc = models.CharField(max_length=200,verbose_name='描述')
    apply_icon = models.FileField(upload_to = 'apply/icon/',verbose_name='应用图标',null=True, blank=True)
    apply_type = models.CharField(max_length=50,verbose_name='类型')
    apply_playbook = models.CharField(max_length=200,verbose_name='应用剧本')
    apply_payload = models.TextField(verbose_name='参数变量',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_apply_config'
        default_permissions = ()
        permissions = (
            ("apply_read_config", "读取应用配置表权限"),
            ("apply_change_config", "更改应用配置表权限"),
            ("apply_add_config", "添加应用配置表权限"),
            ("apply_delete_config", "删除应用配置表权限"),              
            )   
        verbose_name = '应用管理' 
        verbose_name_plural = '应用配置表'  
        
    def to_json(self):
        json_format = {
            "id":self.id,           
            "apply_name":self.apply_name,
            "apply_desc":self.apply_desc,
            "apply_type":self.apply_type,
            "apply_payload":self.apply_payload,
            "apply_icon":str(self.apply_icon)
        }
        return  json_format 
    
    
class ApplyTasksModel(models.Model):
    
    task_status = (
            ("ready", u"准备中"),
            ("stop", u"停止"),
            ("running", u"运行中"),
            ("failed", u"失败"),
            ("finished", u"完成"),
            ("expired", u"过期")
        ) 
    id = models.AutoField(verbose_name='id',primary_key=True)   
    user = models.IntegerField(verbose_name='用户')
    apply_id = models.IntegerField(verbose_name='应用id',db_index=True)
    task_id =  models.CharField(max_length=100,verbose_name='任务id')
    task_per = models.CharField(max_length=10,verbose_name='任务进度')
    status = models.CharField(choices=task_status,max_length=10,default='ready',verbose_name='状态',db_index=True)
    deploy_type = models.CharField(max_length=20,default='playbook',verbose_name='任务类型')
    payload =  models.TextField(verbose_name='ansible参数变量')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='开始时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='修改时间')
    error_msg = models.TextField(verbose_name='错误信息',null=True, blank=True)

    def to_json(self):
        try:
            username = User.objects.get(id=self.user).to_avatar()
        except Exception as ex:
            username = '未知'        
        return {
            'user_info':username,
            'task_id': self.task_id,
            'apply_id':self.apply_id,
            'task_per':self.task_per,
            'deploy_type': self.deploy_type,
            'payload': self.payload,
            "create_time":datetime.strftime(self.create_time, '%Y-%m-%d %H:%M:%S'),
            "update_time":datetime.strftime(self.update_time, '%Y-%m-%d %H:%M:%S'),
            'error_msg': self.error_msg,
            'status': self.status
        }
        
    class Meta:
        db_table = 'opsmanage_apply_tasks'
        default_permissions = ()
        verbose_name = '应用部署任务表'  
        verbose_name_plural = '应用部署任务表'  
        
        
class Apply_Tasks_Result(models.Model):
    task_type = {
        ("banner", u"任务标题"),
        ("msg", u"任务消息"),
        ("stats", u"任务总结"),
    }     
    logId = models.ForeignKey('ApplyTasksModel', on_delete=models.CASCADE)
    task_msg = models.TextField(verbose_name='输出内容',blank=True,null=True) 
    task_name = models.CharField(max_length=200,verbose_name='输出内容',blank=True,null=True)
    task_type = models.CharField(choices=task_type,max_length=10,verbose_name='输出内容',blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='开始时间')  
    class Meta:
        db_table = 'opsmanage_apply_tasks_result'
        default_permissions = ()
        verbose_name = '应用部署任务结果表'  
        verbose_name_plural = '应用部署结果表'  
        
    def to_json(self):       
        return {
            'id':self.id,
            'task_id': self.logId.id,
            'task_msg':self.task_msg,
            'task_name':self.task_name,
            'task_type': self.task_type,
            "create_time":datetime.strftime(self.create_time, '%Y-%m-%d %H:%M:%S'),
        }                                    