# -*- coding: utf-8 -*-

from django.db import models
from orders.models import Order_System
from enum import unique
# Create your models here.
class Project_Config(models.Model):  
    project_repertory_choices = (
                          ('git',u'git'),
                          ('svn',u'svn'),
                          )   
    deploy_model_choices =  (
                          ('branch',u'branch'),
                          ('tag',u'tag'),
                          )  
    project = models.ForeignKey('asset.Project_Assets',related_name='project_config', on_delete=models.CASCADE) 
    project_env = models.CharField(max_length=50,verbose_name='项目环境',default=None)
    project_name =  models.CharField(max_length=100,verbose_name='项目名称',default=None)
    project_service = models.SmallIntegerField(verbose_name='业务类型')
    project_type = models.CharField(max_length=10,verbose_name='编译类型')
    project_local_command = models.TextField(blank=True,null=True,verbose_name='部署服务器要执行的命令',default=None)
    project_repo_dir = models.CharField(max_length=100,verbose_name='本地仓库目录',default=None)
    project_dir = models.CharField(max_length=100,verbose_name='代码目录',default=None)
    project_exclude = models.TextField(blank=True,null=True,verbose_name='排除文件',default=None)
    project_is_include = models.SmallIntegerField(default=0, verbose_name="包含或者排除")    
    project_address = models.CharField(max_length=100,verbose_name='版本仓库地址',default=None)
    project_uuid = models.CharField(max_length=50,verbose_name='唯一id')
    project_repo_user = models.CharField(max_length=50,verbose_name='仓库用户名',blank=True,null=True)
    project_repo_passwd = models.CharField(max_length=50,verbose_name='仓库密码',blank=True,null=True)
    project_repertory = models.CharField(choices=project_repertory_choices,max_length=10,verbose_name='仓库类型',default=None)
    project_status = models.SmallIntegerField(verbose_name='是否激活',blank=True,null=True,default=None)
    project_pre_remote_command = models.TextField(blank=True,null=True,verbose_name='部署之后执行的命令',default=None)
    project_remote_command = models.TextField(blank=True,null=True,verbose_name='部署之后执行的命令',default=None)
    project_user = models.CharField(max_length=50,verbose_name='项目文件宿主',default=None) 
    project_model = models.CharField(choices=deploy_model_choices,max_length=10,verbose_name='上线类型',default=None)
    project_servers = models.TextField(verbose_name='目标主机')
    project_logpath = models.CharField(max_length=500, verbose_name='日志路径')
    project_target_root  = models.CharField(max_length=200, verbose_name='部署路径')
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_project_config'
        default_permissions = ()
        permissions = (
            ("project_read_project_config", "读取项目部署权限"),
            ("project_change_project_config", "更改项目部署权限"),
            ("project_add_project_config", "添加项目部署权限"),
            ("project_delete_project_config", "删除项目部署权限"),               
        )
        unique_together = (("project_env", "project","project_name"))
        verbose_name = '项目发布管理'  
        verbose_name_plural = '项目管理表'  
 
class Log_Project_Config(models.Model):
    project = models.ForeignKey('Project_Config',related_name='project_config', on_delete=models.CASCADE)
    username = models.CharField(max_length=50,verbose_name='操作用户')
    commit_id = models.CharField(max_length=200,default=None,blank=True,null=True)
    servers = models.TextField(verbose_name='目标主机',default=None)
    branch = models.CharField(max_length=100,default=None,blank=True,null=True)
    tag = models.CharField(max_length=100,default=None,blank=True,null=True)
    status = models.CharField(max_length=10)
    type = models.CharField(max_length=10,default='deploy',blank=True,null=True)
    task_id = models.CharField(max_length=50,verbose_name='唯一id',unique=True,db_index=True)
    package = models.CharField(max_length=500,default=None,blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
#     take_time = models.IntegerField(verbose_name='花费时间')
    class Meta:
        default_permissions = ()
        db_table = 'opsmanage_log_project_config'
        verbose_name = '项目发布管理'  
        verbose_name_plural = '项目配置操作日志配置表'                

    def get_version(self):
        try:
            if self.project.project_model == "branch":
                return "分支: " + self.branch + ' 版本: ' + self.commit_id[0:10]
            else:
                return "标签: " + self.tag
        except:
            return "未知"
        
class Log_Project_Record(models.Model):
    key = models.CharField(max_length=50,verbose_name='操作类型',default=None)
    msg = models.TextField(verbose_name='名称',default=None)
    title = models.CharField(max_length=100,verbose_name='标题') 
    status = models.CharField(max_length=10,default=None,blank=True,null=True)
    task_id = models.CharField(max_length=50,db_index=True,verbose_name='唯一id') 
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')
    class Meta:
        default_permissions = ()
        db_table = 'opsmanage_log_project_record'
        verbose_name = '项目发布管理'  
        verbose_name_plural = '项目配置操作记录表'      
           
    
class Project_Roles(models.Model):
    role_choices = (
                    ("deploy",u"deploy"),
                    ("manage",u"manage")
                    )
    project = models.ForeignKey('Project_Config',related_name='project_roles', on_delete=models.CASCADE)
    user = models.SmallIntegerField(verbose_name='用户id',default=None)
    role =  models.CharField(choices=role_choices,max_length=10,verbose_name='项目角色')
    class Meta:
        default_permissions = ()
        db_table = 'opsmanage_project_role'
        unique_together = (("project", "user"))
        verbose_name = '项目发布管理' 
        verbose_name_plural = '项目角色管理表' 
        