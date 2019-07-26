# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Cron_Config(models.Model): 
    cron_server = models.ForeignKey('asset.Assets',related_name='crontab_total',on_delete=models.CASCADE) 
    cron_minute = models.CharField(max_length=10,verbose_name='分',default=None)
    cron_hour = models.CharField(max_length=10,verbose_name='时',default=None)
    cron_day = models.CharField(max_length=10,verbose_name='天',default=None)
    cron_week = models.CharField(max_length=10,verbose_name='周',default=None)
    cron_month = models.CharField(max_length=10,verbose_name='月',default=None)
    cron_user = models.CharField(max_length=50,verbose_name='任务用户',default=None)
    cron_name = models.CharField(max_length=100,verbose_name='任务名称',default=None)
    cron_log_path = models.CharField(max_length=500,blank=True,null=True,verbose_name='任务日志路径',default=None)
    cron_type = models.CharField(max_length=10,verbose_name='任务类型',default=None)
    cron_command = models.CharField(max_length=200,verbose_name='任务参数',default=None)
    cron_script = models.FileField(upload_to = './cron/',blank=True,null=True,verbose_name='脚本路径',default=None)
    cron_script_path =  models.CharField(max_length=100,blank=True,null=True,verbose_name='脚本路径',default=None)
    cron_status = models.SmallIntegerField(verbose_name='任务状态',default=None)
    class Meta:
        db_table = 'opsmanage_cron_config'
        default_permissions = ()
        permissions = (
            ("sched_can_read_cron_config", "读取任务配置权限"),
            ("sched_can_change_cron_config", "更改任务配置权限"),
            ("sched_can_add_cron_config", "添加任务配置权限"),
            ("sched_can_delete_cron_config", "删除任务配置权限"),            
        )
        verbose_name = '计划任务管理'  
        verbose_name_plural = '任务配置表' 
        unique_together = (("cron_name", "cron_server","cron_user"))
        
class Log_Cron_Config(models.Model): 
    cron_id = models.IntegerField(verbose_name='id',blank=True,null=True,default=None)
    cron_user = models.CharField(max_length=50,verbose_name='操作用户',default=None)
    cron_name = models.CharField(max_length=100,verbose_name='名称',default=None)
    cron_content = models.CharField(max_length=100,default=None)
    cron_server = models.CharField(max_length=100,default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_cron_config'
        default_permissions = ()
        verbose_name = '计划任务管理'  
        verbose_name_plural = '任务配置操作记录表'
         


class Sched_Node(models.Model):   
    sched_node = models.AutoField(primary_key=True) 
    sched_server = models.ForeignKey('asset.Assets',related_name='sched_node',on_delete=models.CASCADE) 
    port = models.SmallIntegerField(verbose_name='端口')
    token = models.CharField(max_length=100,verbose_name='认证密码',unique=True)
    enable = models.SmallIntegerField(verbose_name='端口',default=1)
    class Meta:
        db_table = 'opsmanage_sched_node'
        default_permissions = ()
        verbose_name = '计划任务管理'  
        verbose_name_plural = '任务节点表'     
        unique_together = (("sched_server", "port"))
        
    def to_json(self):
        json_format = {
            "sched_node":self.sched_node,
            "sched_server":self.sched_server.server_assets.ip,
            "port":self.port,
            "token":self.token,
            "enable":self.enable
        }
        return  json_format     
    
class Sched_Job_Config(models.Model): 
    NOTICE_TYPE = (
             (0,'邮箱'),
             (1,'微信'),         
             (2,'钉钉'),                    
            ) 
    SCHED_TYPE = (
                 ("date",'日期'),
                 ("interval",'间隔'),         
                 ("cron",'crontab'),                                
            ) 
    TRIGGER_TYPE =  (
             (0,'失败'),
             (1,'成功'),         
             (2,'完成'),                    
            ) 
    JOBSTATUS = (
             ("running",'运行'),
             ("stopped",'停止'),                                 
            )  
    job_node = models.ForeignKey(Sched_Node,related_name='node_jobs',on_delete=models.CASCADE)   
    job_id = models.CharField(max_length=50,verbose_name='任务id',unique=True)
    job_name = models.CharField(max_length=50,verbose_name='任务名称')
    second = models.CharField(max_length=50,verbose_name='分',blank=True,null=True,default=None)
    minute = models.CharField(max_length=50,verbose_name='时',blank=True,null=True,default=None)
    hour = models.CharField(max_length=50,verbose_name='天',blank=True,null=True,default=None)
    week = models.CharField(max_length=50,verbose_name='第几周',blank=True,null=True,default=None)
    day = models.CharField(max_length=50,verbose_name='周',blank=True,null=True,default=None)
    month = models.CharField(max_length=50,verbose_name='月',blank=True,null=True,default=None)
    year = models.CharField(max_length=50,verbose_name='年',blank=True,null=True,default=None)
    day_of_week = models.CharField(max_length=50,verbose_name='星期几',blank=True,null=True,default=None)
    job_command = models.TextField(verbose_name='任务参数')
    start_date = models.CharField(max_length=20,verbose_name='开始时间',blank=True,null=True,default=None)
    end_date = models.CharField(max_length=20,verbose_name='结束时间',blank=True,null=True,default=None)
    run_date = models.CharField(max_length=20,verbose_name='指定时间',blank=True,null=True,default=None)
    sched_type = models.CharField(choices=SCHED_TYPE,max_length=10,verbose_name='调度类型')
    status = models.CharField(max_length=10,choices=JOBSTATUS,verbose_name='任务状态') 
    is_alert = models.SmallIntegerField(default=0,verbose_name='执行失败是否通知')
    notice_trigger = models.SmallIntegerField(choices=TRIGGER_TYPE,verbose_name='触发类型',blank=True,null=True,default=0)  
    notice_type =  models.SmallIntegerField(choices=NOTICE_TYPE,verbose_name='通知类型',blank=True,null=True,default=0)  
    notice_interval =  models.IntegerField(verbose_name='通知间隔',blank=True,null=True,default=3600)  
    notice_number = models.TextField(verbose_name='通知人',blank=True,null=True,default=None)  
    atime = models.IntegerField(blank=True,null=True,verbose_name='告警时间')
    class Meta:
        db_table = 'opsmanage_sched_job_config'
        default_permissions = ()
        verbose_name = '计划任务管理'  
        verbose_name_plural = '任务配置表'    
    
    def to_alert_json(self):
        json_format = {
            "notice_type":self.notice_type,
            "notice_number":self.notice_number,
            "notice_interval":self.notice_interval,
            "notice_trigger":self.notice_trigger,
            "atime":self.atime,
            "is_alert":self.is_alert,
        }
        return  json_format       
    
    def to_cron_json(self):
        json_format = {
            'id': self.job_id,
            'cmd':self.job_command,
            "status":self.status,
            "type":self.sched_type, 
            "sched":{
                    "second":self.second,
                    "minute":self.minute,
                    "hour":self.hour,
                    "week":self.week,
                    "day":self.day,
                    "month":self.month,
                    "day_of_week":self.day_of_week, 
                    "year":self.year,
                    "start_date":self.start_date,
                    "end_date":self.end_date,      
                    }        
        }
        return json_format 
    
    def to_interval_json(self):
        json_format = {
            'id': self.job_id,
            'cmd':self.job_command,
            "status":self.status,
            "type":self.sched_type,
            "sched":{
                    "seconds":self.second,
                    "minutes":self.minute,
                    "hours":self.hour,
                    "weeks":self.week,
                    "days":self.day,
                    "start_date":self.start_date,
                    "end_date":self.end_date,      
                    }   
        }
        return json_format 
    
    def to_date_json(self):
        json_format = {
            'id': self.job_id,
            'cmd':self.job_command,
            "status":self.status,
            "type":self.sched_type,
            "sched":{
                    "run_date":self.run_date,     
                    }   
        }
        return json_format                    
        

class Sched_Job_Logs(models.Model): 
    job_id = models.ForeignKey(Sched_Job_Config,related_name='node_jobs_log',on_delete=models.CASCADE)   
    status = models.SmallIntegerField(verbose_name='任务执行状态') 
    stime = models.IntegerField(verbose_name='开始时间')
    etime = models.IntegerField(verbose_name='结束时间')
    cmd = models.TextField(verbose_name='执行命令',default=None)
    result = models.TextField(verbose_name='执行结果',default=None)  
    class Meta:
        db_table = 'opsmanage_sched_job_logs'
        default_permissions = ()
        verbose_name = '计划任务管理'  
        verbose_name_plural = '任务执行日志表'  
        
    def to_json(self):
        json_format = {
            'jid': self.job_id.job_id,
            'stime':self.stime,
            'etime':self.etime,
            "status":self.status,
            "result":self.result,
        }
        return json_format                      
                