#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User

# Create your models here.
class Log_Deploy_Model(models.Model): 
    ans_user = models.CharField(max_length=50,verbose_name='使用用户',default=None)
    ans_model = models.CharField(max_length=100,verbose_name='模块名称',default=None)
    ans_args = models.CharField(max_length=500,blank=True,null=True,verbose_name='模块参数',default=None)
    ans_server = models.TextField(verbose_name='服务器',default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_deploy_model'
        default_permissions = ()
        permissions = (
            ("deploy_read_log_deploy_model", "读取部署模块执行记录权限"),
            ("deploy_change_log_deploy_model", "修改部署模块执行记录权限"),
            ("deploy_add_log_deploy_model", "添加部署模块执行记录权限"),
            ("deploy_delete_log_deploy_model", "删除部署模块执行记录权限"),         
        )
        verbose_name = '应用部署管理'  
        verbose_name_plural = 'Ansible模块执行记录表' 
        
class Deploy_Playbook(models.Model):   
    playbook_name = models.CharField(max_length=50,verbose_name='剧本名称',unique=True)
    playbook_desc = models.CharField(max_length=200,verbose_name='功能描述',blank=True,null=True)
    playbook_vars = models.TextField(verbose_name='模块参数',blank=True,null=True)
    playbook_uuid = models.CharField(max_length=50,verbose_name='唯一id')
    playbook_type = models.CharField(verbose_name='服务器选择类型',max_length=10,blank=True,null=True)
    playbook_file = models.FileField(upload_to = './playbook/',verbose_name='剧本路径')
    playbook_service = models.SmallIntegerField(verbose_name='授权业务',blank=True,null=True)
    playbook_user = models.SmallIntegerField(verbose_name='授权用户',blank=True,null=True,)
    playbook_server = models.TextField(verbose_name='目标机器',blank=True,null=True)
    playbook_group = models.SmallIntegerField(verbose_name='授权组',blank=True,null=True)
    playbook_tags = models.SmallIntegerField(verbose_name='资产标签',blank=True,null=True)
    playbook_inventory_groups = models.SmallIntegerField(verbose_name='资产组',blank=True,null=True)
    create_time = models.DateTimeField(default = timezone.now,blank=True,null=True,verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True,blank=True,null=True,verbose_name='修改时间')    
    class Meta:
        db_table = 'opsmanage_deploy_playbook'
        default_permissions = ()
        permissions = (
            ("deploy_read_deploy_playbook", "读取部署剧本权限"),
            ("deploy_change_deploy_playbook", "修改部署剧本权限"),
            ("deploy_add_deploy_playbook", "添加部署剧本权限"),
            ("deploy_delete_deploy_playbook", "删除部署剧本权限"),        
            ("deploy_exec_deploy_playbook", "执行部署剧本权限"),       
        )
        verbose_name = '应用部署管理'  
        verbose_name_plural = '部署剧本配置表' 
    
    def to_json(self):
        try:
            username = User.objects.get(id=self.playbook_user).username
        except Exception as ex:
            username = '未知'
        json_format = {
            "id":self.id,           
            "playbook_name":self.playbook_name,
            "playbook_desc":self.playbook_desc,
            "playbook_vars":self.playbook_vars,
            "playbook_type":self.playbook_type,
            "playbook_file":self.playbook_file,
            "playbook_service":self.playbook_service,
            "playbook_user":username,
            "playbook_server":self.playbook_server,
            "playbook_group":self.playbook_group,
            "playbook_tags":self.playbook_tags,
            "playbook_inventory_groups":self.playbook_inventory_groups,
            "create_time":self.create_time,
            "update_date":self.update_date,
        }
        return  json_format             
        
class Deploy_Script(models.Model): 
    script_name = models.CharField(max_length=50,verbose_name='脚本名称',unique=True)
    script_uuid = models.CharField(max_length=50,verbose_name='唯一id',blank=True,null=True)
    script_server = models.TextField(verbose_name='目标机器',blank=True,null=True)
    script_file = models.FileField(upload_to = './scripts/',verbose_name='脚本路径')
    script_args = models.TextField(blank=True,null=True,verbose_name='脚本参数')
    script_service = models.SmallIntegerField(verbose_name='授权业务',blank=True,null=True)
    script_user = models.SmallIntegerField(verbose_name='添加人',blank=True,null=True)
    script_group = models.SmallIntegerField(verbose_name='授权组',blank=True,null=True)
    script_tags = models.SmallIntegerField(verbose_name='资产标签',blank=True,null=True)
    script_inventory_groups = models.SmallIntegerField(verbose_name='资产组',blank=True,null=True)
    script_type = models.CharField(max_length=50,verbose_name='脚本类型',blank=True,null=True)
    create_time = models.DateTimeField(default = timezone.now,blank=True,null=True,verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True,blank=True,null=True,verbose_name='修改时间')
   
    
    class Meta:
        db_table = 'opsmanage_deploy_script'
        default_permissions = ()
        permissions = (
            ("deploy_read_deploy_script", "读取部署脚本权限"),
            ("deploy_change_deploy_script", "修改部署脚本权限"),
            ("deploy_add_deploy_script", "添加部署脚本权限"),
            ("deploy_delete_deploy_script", "删除部署脚本权限"),              
            ("deploy_exec_deploy_script", "执行部署脚本权限"),    
            ("deploy_exec_deploy_model", "执行部署模块权限"),      
            ("deploy_read_deploy_model", "读取部署模块权限"),   
        )
        verbose_name = '应用部署管理'  
        verbose_name_plural = '部署脚本配置表'         

    def to_json(self):
        try:
            username = User.objects.get(id=self.script_user).username
        except Exception as ex:
            username = '未知'
        json_format = {
            "id":self.id,           
            "script_name":self.script_name,
            "script_args":self.script_args,
            "script_service":self.script_service,
            "script_user":username,
            "script_server":self.script_server,
            "script_group":self.script_group,
            "script_tags":self.script_tags,
            "script_inventory_groups":self.script_inventory_groups,
            "create_time":self.create_time,
            "update_date":self.update_date,
        }
        return  json_format 
        

class Log_Deploy_Playbook(models.Model): 
    ans_id = models.IntegerField(verbose_name='id',blank=True,null=True,default=None)
    ans_user = models.CharField(max_length=50,verbose_name='使用用户',default=None)
    ans_name = models.CharField(max_length=100,verbose_name='模块名称',default=None)
    ans_content = models.CharField(max_length=200,default=None)
    ans_server = models.TextField(verbose_name='服务器',default=None)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        db_table = 'opsmanage_log_deploy_playbook'
        default_permissions = ()
        permissions = (
            ("deploy_read_log_deploy_playbook", "读取部署剧本执行记录权限"),
            ("deploy_change_log_deploy_playbook", "修改部署剧本执行记录权限"),
            ("deploy_add_log_deploy_playbook", "添加部署剧本执行记录权限"),
            ("deploy_delete_log_deploy_playbook", "删除部署剧本执行记录权限"),
        )
        verbose_name = '应用部署管理'  
        verbose_name_plural = '部署剧本操作记录表' 
    
class Deploy_Inventory(models.Model):    
    name = models.CharField(max_length=200,unique=True,verbose_name='资产名称')
    desc = models.CharField(max_length=200,verbose_name='功能描述')
    user =  models.SmallIntegerField(verbose_name='创建人')
    create_time = models.DateTimeField(default = timezone.now,blank=True,null=True,verbose_name='创建时间') 
    class Meta:
        db_table = 'opsmanage_deploy_inventory'
        default_permissions = ()
        permissions = (
            ("deploy_read_deploy_inventory", "读取部署资产权限"),
            ("deploy_change_deploy_inventory", "修改部署资产权限"),
            ("deploy_add_deploy_inventory", "添加部署资产权限"),
            ("deploy_delete_deploy_inventory", "删除部署资产权限"),             
        )
        verbose_name = '应用部署管理'  
        verbose_name_plural = '部署资产表'


class Deploy_Inventory_Groups(models.Model):    
    inventory = models.ForeignKey('Deploy_Inventory',related_name='inventory_group', on_delete=models.CASCADE)
    group_name =  models.CharField(max_length=100,verbose_name='group name')
    ext_vars = models.TextField(verbose_name='组外部变量',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_deploy_inventory_groups'
        default_permissions = ()
        verbose_name = '应用部署管理'  
        verbose_name_plural = '部署资产成员表'
        unique_together = (("inventory", "group_name"))

class Deploy_Inventory_Groups_Server(models.Model):
    groups = models.ForeignKey('Deploy_Inventory_Groups',related_name='inventory_group_server', on_delete=models.CASCADE)
    server = models.SmallIntegerField(verbose_name='服务器')
    class Meta:
        db_table = 'opsmanage_deploy_inventory_groups_servers'
        default_permissions = ()
        unique_together = (("groups", "server"))
        
        
class Deploy_CallBack_Model_Result(models.Model):
    logId = models.ForeignKey('Log_Deploy_Model', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='输出内容',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_deploy_callback_model_result'
        default_permissions = ()
        verbose_name = '应用部署管理'  
        verbose_name_plural = '部署剧本操作记录表'
    
    
class Deploy_CallBack_PlayBook_Result(models.Model):
    logId = models.ForeignKey('Log_Deploy_Playbook', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='输出内容',blank=True,null=True)   
    class Meta:
        db_table = 'opsmanage_deploy_callback_playbook_result'
        default_permissions = ()
        verbose_name = '应用部署管理'  
        verbose_name_plural = '部署剧本操作记录详情表'         