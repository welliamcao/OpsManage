# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
class Global_Config(models.Model):
    ansible_model = models.SmallIntegerField(verbose_name='是否开启ansible模块操作记录',blank=True,null=True)
    ansible_playbook = models.SmallIntegerField(verbose_name='是否开启ansible剧本操作记录',blank=True,null=True)
    cron = models.SmallIntegerField(verbose_name='是否开启计划任务操作记录',blank=True,null=True)
    project = models.SmallIntegerField(verbose_name='是否开启项目操作记录',blank=True,null=True)
    assets = models.SmallIntegerField(verbose_name='是否开启资产操作记录',blank=True,null=True)
    server = models.SmallIntegerField(verbose_name='是否开启服务器命令记录',blank=True,null=True)
    email = models.SmallIntegerField(verbose_name='是否开启邮件通知',blank=True,null=True)
    webssh = models.SmallIntegerField(verbose_name='是否开启WebSSH',blank=True,null=True)
    sql = models.SmallIntegerField(verbose_name='是否开启SQL更新通知',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_global_config'
    
class Email_Config(models.Model):
    site = models.CharField(max_length=100,verbose_name='部署站点')
    host = models.CharField(max_length=100,verbose_name='邮件发送服务器')
    port = models.SmallIntegerField(verbose_name='邮件发送服务器端口')
    user = models.CharField(max_length=100,verbose_name='发送用户账户')
    passwd = models.CharField(max_length=100,verbose_name='发送用户密码')
    subject = models.CharField(max_length=100,verbose_name='发送邮件主题标识',default=u'[OPS]')
    cc_user = models.TextField(verbose_name='抄送用户列表',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_email_config'