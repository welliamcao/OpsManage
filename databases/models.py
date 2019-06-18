#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models
      

class DataBase_Server_Config(models.Model):
    env_type = (
                ('alpha',u'开发环境'),
                ('beta',u'测试环境'),
                ('ga',u'生产环境'),
                )
    mode = (
            (1,u'单例'),
            (2,u'主从'),
            (3,u'pxc'),
            (4,u'Tidb'),
            (5,u'Bhproxy'),
            (6,u'ProxySQL'),
            ) 
    rw_type = (
                ('read',u'只读'),
                ('r/w',u'读写'),
                ('write',u'可写'),
                )    
    db_env = models.CharField(choices=env_type,max_length=10,verbose_name='环境类型',default=None)
    db_type = models.CharField(max_length=10,verbose_name='数据库类型',blank=True,null=True)
    db_name = models.CharField(max_length=100,verbose_name='数据库名',blank=True,null=True)
    db_assets = models.ForeignKey('asset.Assets',related_name='database_total', on_delete=models.CASCADE,verbose_name='assets_id')
    db_mode = models.SmallIntegerField(choices=mode,verbose_name='架构类型',default=1)
    db_user = models.CharField(max_length=100,verbose_name='用户',blank=True,null=True)
    db_passwd = models.CharField(max_length=100,verbose_name='密码',blank=True,null=True)
    db_port = models.IntegerField(verbose_name='端口')
    db_mark =  models.CharField(max_length=100,verbose_name='标识',blank=True,null=True)
    db_rw =  models.CharField(choices=rw_type,max_length=20,verbose_name='读写类型',blank=True,null=True)
    class Meta:
        db_table = 'opsmanage_database_server_config'
        default_permissions = ()
        permissions = (
            ("database_read_database_server_config", "读取数据库信息表权限"),
            ("database_change_database_server_config", "更改数据库信息表权限"),
            ("database_add_database_server_config", "添加数据库信息表权限"),
            ("database_delete_database_server_config", "删除数据库信息表权限"),     
            ("database_query_database_server_config", "数据库查询查询权限"), 
			("databases_dml_database_server_config", "数据库执行DML语句权限"), 
            ("database_binlog_database_server_config", "数据库Binglog解析权限"),        
            ("database_schema_database_server_config", "数据库表结构查询权限"),
            ("database_optimize_database_server_config", "数据库SQL优化建议权限"),
        )
        unique_together = (("db_port", "db_assets","db_env","db_name"))
        verbose_name = '数据库信息表'  
        verbose_name_plural = '数据库信息表'
    
    def get_modes(self):
        data = dict()
        for i in self.mode:    
            data[i[0]] = i[1]
        return data
    
    def get_types(self):
        data = dict()
        for i in self.env_type:    
            data[i[0]] = i[1]
        return data        
    
    def get_rw(self):
        data = dict()
        for i in self.rw_type:    
            data[i[0]] = i[1]
        return data         
    
class Database_User(models.Model):
    db = models.SmallIntegerField(verbose_name='db_id')
    user = models.SmallIntegerField(verbose_name='用户id') 
    tables =  models.TextField(verbose_name='可以操作的表',blank=True,null=True) 
    privs = models.CharField(max_length=250,verbose_name='SQL类型',blank=True,null=True)    
    class Meta:
        db_table = 'opsmanage_database_user'
        default_permissions = ()
        unique_together = (("db", "user"))
        verbose_name = '用户数据库分配表'  
        verbose_name_plural = '用户数据库分配表'
    
class Database_Group(models.Model):
    db = models.SmallIntegerField(verbose_name='db_id')
    group = models.SmallIntegerField(verbose_name='用户id')    
    class Meta:
        db_table = 'opsmanage_database_group'
        unique_together = (("db", "group"))
        verbose_name = '用户组数据库分配表'  
        verbose_name_plural = '用户组数据库分配表'


class SQL_Execute_Histroy(models.Model):
    exe_user = models.CharField(max_length= 100,verbose_name='执行人')
    exe_db = models.ForeignKey('DataBase_Server_Config',verbose_name='数据库id', on_delete=models.CASCADE)
    exe_sql =  models.TextField(verbose_name='执行的SQL内容') 
    exec_status = models.SmallIntegerField(blank=True,null=True,verbose_name='执行状态')
    exe_result = models.TextField(blank=True,null=True,verbose_name='执行结果') 
    exe_time = models.IntegerField(default=0,verbose_name='执行时间')
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='执行时间')  
    class Meta:
        db_table = 'opsmanage_sql_execute_histroy'
        default_permissions = ()
        permissions = (
            ("database_read_sql_execute_histroy", "读取SQL执行历史表权限"),
            ("database_change_sql_execute_histroy", "更改SQL执行历史表权限"),
            ("database_add_sql_execute_histroy", "添加SQL执行历史表权限"),
            ("database_delete_sql_execute_histroy", "删除SQL执行历史表权限"),              
        )
        verbose_name = 'SQL执行历史记录表'  
        verbose_name_plural = 'SQL执行历史记录表'     
        
class Custom_High_Risk_SQL(models.Model):
    sql = models.CharField(max_length=200,unique=True,verbose_name='SQL内容') 
    class Meta:
        db_table = 'opsmanage_custom_high_risk_sql'
        default_permissions = ()
        permissions = (
            ("database_read_custom_high_risk_sql", "读取高危SQL表权限"),
            ("database_change_custom_high_risk_sql", "更改高危SQL表权限"),
            ("database_add_custom_high_risk_sql", "添加高危SQL表权限"),
            ("database_delete_custom_high_risk_sql", "删除高危SQL表权限"),              
        )
        verbose_name = '自定义高危SQL表'  
        verbose_name_plural = '自定义高危SQL表' 
        
        