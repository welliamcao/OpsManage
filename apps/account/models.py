#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from mptt.models import MPTTModel, TreeForeignKey


class Role(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField(Permission, blank=True, verbose_name="角色权限")
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")
        
    class Meta:
        db_table = 'opsmanage_role'
        default_permissions = ()
        permissions = (
            ("account_read_role", "读取角色权限"),
            ("account_change_role", "更改角色权限"),
            ("account_add_role", "添加角色权限"),
            ("account_delete_role", "删除角色权限"),               
        )
        verbose_name = '账户管理'
        verbose_name_plural = '角色信息'

    def to_json(self):
        json_format = {
            "id":self.id,
            "name":self.name,
            "desc":self.desc,
            "permissions":[ x.id for x in  self.permissions.all()],
        }
        return  json_format

class Structure(MPTTModel):
    type_choices = (("unit", "单位"), ("department", "部门"))
    text = models.CharField(max_length=60, verbose_name="名称")
    desc = models.CharField(max_length=150, blank=True, null=True, verbose_name="描述")
    type = models.CharField(max_length=20, choices=type_choices, default="department", verbose_name="类型")
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, verbose_name='上级业务', null=True, blank=True,db_index=True ,related_name='children')
    manage = models.SmallIntegerField(blank=True,null=True,verbose_name='负责人')
    mail_group = models.CharField(max_length=200, verbose_name="邮件群组地址", blank=True, null=True)
    wechat_webhook_url = models.TextField(verbose_name="企业微信群聊机器人WebHook", blank=True, null=True)
    dingding_webhook_url = models.TextField(verbose_name="钉钉群聊机器人WebHook", blank=True, null=True)
    
    class Meta:
        db_table = 'opsmanage_structure'
        default_permissions = ()
        permissions = (
            ("account_read_structure", "读取组织架构权限"),
            ("account_change_structure", "更改组织架构权限"),
            ("account_add_structure", "添加组织架构权限"),
            ("account_delete_structure", "删除组织架构权限"),         
        )
        verbose_name = '账户管理'
        verbose_name_plural = '组织架构信息'
        
    def __str__(self):
        return self.text

    def node_path(self):
        self.paths = ''
        if not self.parent:
            self.paths = self.text
        else:
            dataList = Structure.objects.raw("""SELECT id,text as path FROM opsmanage_structure WHERE tree_id = {tree_id} AND  lft < {lft} AND  rght > {rght} ORDER BY lft DESC;""".format(tree_id=self.tree_id,lft=self.lft,rght=self.rght))
            for ds in dataList:
                self.paths = ds.path + '/' + self.paths
            self.paths = self.paths  + self.text
        return  self.paths
    
    def last_node(self):
        if self.is_leaf_node():
            return 1
        else:
            return 0
    
    def icon(self):
        icon =  "fa fa-tree"  
        if self.parent: 
            icon = "fa fa-plus-square" 
        if self.is_leaf_node():
            return 'fa fa-minus-square-o' 
        return icon           
    
    def manage_name(self):
        
        if self.manage:

            try:
                user =  User.objects.get(id=self.manage)
            except:
                return "无"
            
            if user.name:
                return user.name
            else:
                return user.username

                
    def to_json(self):
        if self.parent: 
            parentId = self.parent.id
        else:
            parentId = 0      
        json_format = {
            "id":self.id,
            "text":self.text,
            "icon":self.icon(),
            "level":self.level,
            "desc":self.desc,
            "tree_id":self.tree_id,
            "lft":self.lft,
            "rght":self.rght,
            "paths":self.node_path(),
            "manage":self.manage,
            "manage_name":self.manage_name(),
            "last_node":self.last_node(),
            "parentId": parentId,    
            "mail_group":self.mail_group,
            "wechat_webhook_url":self.wechat_webhook_url,
            "dingding_webhook_url":self.dingding_webhook_url,                          
        }
        return json_format    

class User(AbstractUser):
    name = models.CharField(max_length=20, default="", verbose_name="中文名字")
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码",null=True, blank=True)
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    department = models.ManyToManyField("Structure", blank=True, verbose_name="部门")
    post = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    roles = models.ManyToManyField("Role", verbose_name="角色", blank=True)

     
    class Meta:
        db_table = 'opsmanage_user'
        default_permissions = ()
        permissions = (
            ("account_read_user", "读取用户信息权限"),
            ("account_change_user", "更改用户信息权限"),
            ("account_add_user", "添加用户信息权限"),
            ("account_delete_user", "删除用户信息权限"),               
        )
        verbose_name = '账户管理'
        verbose_name_plural = '用户表'
        ordering = ['id']
        
    def __str__(self):
        return self.username
    
    def superior_name(self):
        if self.superior:
            return self.superior.name
        else:
            return "无"
    
    def get_superior(self):
        if self.superior:
            return self.superior.id

    def to_json(self):
        json_format = {
            "id":self.id,
            "username":self.username,
            "is_staff":self.is_staff,
            "is_active":self.is_active,
            "date_joined":self.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
            "name":self.name,
            "mobile":self.mobile,
            "email":self.email,
            "department":[ x.id for x in self.department.all()],
            "post":self.post,
            "superior":self.get_superior(),
            "superior_name":self.superior_name(),
            "roles":[ x.id for x in self.roles.all() ]
        }
        return  json_format

TASK_STATUS = (
        (0, "进行中"),
        (1, "已完成"),
        (2, "执行失败"),
        (3, "执行超时")
    ) 
   
TASK_TYPE = (
        (0, "部署任务"),
        (1, "数据导出"),
        (2, "binlog解析"),
    )
    
class User_Async_Task(models.Model):
    task_id = models.BigIntegerField(verbose_name='任务id', db_index=True)
    task_name = models.CharField(max_length=100, verbose_name='任务名称') 
    extra_id = models.SmallIntegerField(verbose_name='平台其他model的id') 
    user = models.SmallIntegerField(verbose_name='用户id') 
    type = models.SmallIntegerField(verbose_name='任务类型',  choices=TASK_TYPE)
    status = models.SmallIntegerField(verbose_name='任务状态', choices=TASK_STATUS, default=0)
    file = models.FileField(upload_to = './task/', verbose_name='任务结果文件路径', blank=True, null=True)
    args = models.CharField(max_length=500, verbose_name='任务参数') 
    msg = models.TextField(blank=True, null=True, verbose_name='失败原因') 
    token = models.CharField(max_length=50, verbose_name='token', db_index=True)
    ctk = models.CharField(max_length=40, verbose_name='celery task id', db_index=True)
    ctime = models.DateTimeField(auto_now_add=True, blank=True,null=True, verbose_name='开始时间')
    etime = models.DateTimeField(blank=True,null=True, verbose_name='结束时间')
    class Meta:
        db_table = 'opsmanage_user_task'
        default_permissions = ()
        verbose_name = '用户任务管理'  
        verbose_name_plural = '用户异步任务记录表'             
        index_together = ["user", "type"]
        
    def to_json(self):
        if self.etime:
            self.etime = self.ctime.strftime('%Y-%m-%d %H:%M:%S')
        json_format = {
            "id":self.id,
            "task_id":self.task_id,
            "extra_id":self.extra_id,
            "task_name":self.task_name,
            "user":self.user,
            "type":self.type,
            "status":self.status,
            "file":str(self.file),           
            "token":self.token,
            "args":self.args,
            "msg":self.msg,
            "ctk":self.ctk,
            "ctime":self.ctime.strftime('%Y-%m-%d %H:%M:%S'),
            "etime":self.etime,
        }
        return  json_format      