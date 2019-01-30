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
        permissions = (
            ("cron_can_read_cron_config", "读取任务配置权限"),
            ("cron_can_change_cron_config", "更改任务配置权限"),
            ("cron_can_add_cron_config", "添加任务配置权限"),
            ("cron_can_delete_cron_config", "删除任务配置权限"),            
        )
        verbose_name = '任务配置表'  
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
        verbose_name = '任务配置操作记录表'  
        verbose_name_plural = '任务配置操作记录表'
         
    
# class Aps_Jobs_Status(models.Model):
#     id = models.CharField(primary_key=True ,max_length=191,verbose_name='任务Id')
#     next_run_time = models.FloatField(db_index=True)
#     job_state = models.BinaryField()
#     class Meta:
#         db_table = 'opsmanage_jobs_status'
#         verbose_name = 'aps任务状态表'  
#         verbose_name_plural = 'aps任务状态表'    
#     
# class Aps_Jobs_Config(models.Model): 
#     job_id =  models.CharField(primary_key=True,max_length=191,verbose_name='任务Id')  
#     job_func = models.CharField(max_length=50,verbose_name='job函数')
#     job_name = models.CharField(max_length=100,verbose_name='名称')
#     job_args = models.TextField(verbose_name='任务参数')
#     trigger_type = models.CharField(max_length=50,verbose_name='触发器类型')
#     trigger = models.CharField(max_length=200,verbose_name='触发器')
#     job_status = models.SmallIntegerField(verbose_name='任务状态')
#     job_user = models.SmallIntegerField(verbose_name='任务添加人')
#     job_mgt = models.IntegerField(verbose_name='misfire_grace_time',default=60)
#     job_crt_dt = models.SmallIntegerField(blank=True,null=True,verbose_name='创建时间')
#     job_mod_dt = models.SmallIntegerField(blank=True,null=True,verbose_name='修改时间')
#     class Meta:
#         db_table = 'opsmanage_jobs_config'
#         verbose_name = 'aps任务配置表'  
#         verbose_name_plural = 'aps任务配置表'        