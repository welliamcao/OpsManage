#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from __future__ import unicode_literals

from django.db import models



class Order_System(models.Model):
    STATUS = (
#               (0,'已通过'),
              (1,'已拒绝'),
              (2,'审核中'),
              (3,'已部署'),
              (4,'待授权'),
              (5,'已执行'),
              (6,'已回滚'),
              (7,'已撤回'),
              (8,'已授权'),
              (9,'已失败'),              
              ) 
    LEVEL = (
             (0,'非紧急'),
             (1,'紧急'),
             )
    TYPE = (
             (0,'SQL审核'),
             (1,'代码部署'),         
             (2,'文件上传'),    
             (3,'文件下载'),                 
            )
    order_user = models.SmallIntegerField(verbose_name='工单申请人id')
    order_subject = models.CharField(max_length=200,blank=True,null=True,verbose_name='工单申请主题')   
    order_executor = models.SmallIntegerField(verbose_name='工单处理人id')
    order_status = models.IntegerField(choices=STATUS,default='审核中',verbose_name='工单状态') 
    order_level = models.IntegerField(choices=LEVEL,blank=True,null=True,verbose_name='工单紧急程度')
    order_type = models.SmallIntegerField(choices=TYPE,verbose_name='工单类型')
    order_cancel = models.TextField(blank=True,null=True,verbose_name='取消原因') 
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='工单发布时间')
    modify_time = models.DateTimeField(auto_now=True,blank=True,verbose_name='工单最后修改时间')
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_order_system'
        default_permissions = ()
        permissions = (
            ("orders_read_order_system", "读取工单系统权限"),
            ("orders_change_order_systemr", "更改工单系统权限"),
            ("orders_add_order_system", "添加工单系统权限"),
            ("orders_delete_order_system", "删除工单系统权限"),            
        )
        unique_together = (("order_subject","order_user","order_type"))
        verbose_name = '工单管理'  
        verbose_name_plural = '工单系统表'        


        
        
class SQL_Audit_Order(models.Model):
    order = models.OneToOneField('Order_System', on_delete=models.CASCADE) 
    order_type = models.CharField(max_length=10,verbose_name='sql类型')
    order_db = models.ForeignKey('databases.DataBase_Server_Config',related_name ='order_db',verbose_name='数据库id', on_delete=models.CASCADE)
    order_sql =  models.TextField(verbose_name='待审核SQL内容',blank=True,null=True) 
    order_file = models.FileField(upload_to = './sql/',verbose_name='sql脚本路径')
    order_err = models.TextField(blank=True,null=True,verbose_name='失败原因') 
    sql_backup = models.SmallIntegerField(verbose_name='是否备份')
    class Meta:
        db_table = 'opsmanage_sql_audit_order'
        default_permissions = ()
        permissions = (
            ("orders_read_sql_audit_order", "读取SQL审核工单权限"),
            ("orders_change_sql_audit_order", "更改SQL审核工单权限"),
            ("orders_add_sql_audit_order", "添加SQL审核工单权限"),
            ("orders_delete_sql_audit_order", "删除SQL审核工单权限"),              
        )
        verbose_name = '工单管理'  
        verbose_name_plural = 'SQL审核工单表'              

class SQL_Order_Execute_Result(models.Model):
    '''
        errlevel: 返回值为非0的情况下，说明是有错的。1表示警告，不影响执行，2表示严重错误，必须修改。
        stagestatus: 用来表示检查及执行的过程是成功还是失败，如果审核成功，则返回 Audit completed。如果执行成功则返回Execute Successfully，否则返回Execute failed.
                                                                        如果备份成功，则在后面追加Backup successfully，否则追加Backup failed，这个列的返回信息是为了将结果集直接输出而设置的.
                            参考文档：http://mysql-inception.github.io/inception-document/results/                                                                
    '''
    order = models.ForeignKey('SQL_Audit_Order',verbose_name='orderid', on_delete=models.CASCADE)
    stage = models.CharField(max_length= 20)
    errlevel = models.IntegerField(verbose_name='错误信息')
    stagestatus = models.CharField(max_length=40)
    errormessage = models.TextField(blank=True,null=True,verbose_name='错误信息')
    sqltext = models.TextField(blank=True,null=True,verbose_name='SQL内容')
    affectrow = models.IntegerField(blank=True,null=True,verbose_name='影响行数')
    sequence = models.CharField(max_length=30,db_index=True,verbose_name='序号')
    backup_db = models.CharField(max_length=100,blank=True,null=True,verbose_name='Inception备份服务器')
    execute_time = models.CharField(max_length=20,verbose_name='语句执行时间')
    sqlsha = models.CharField(max_length=50,blank=True,null=True,verbose_name='是否启动OSC')
    create_time = models.DateTimeField(auto_now_add=True,db_index=True)
    class Meta:
        db_table = 'opsmanage_sql_execute_result'
        default_permissions = ()
        verbose_name = '工单管理'  
        verbose_name_plural = 'SQL工单执行记录表' 
        
class Order_Notice_Config(models.Model):   
    TYPE = (
             (0,'邮箱'),
             (1,'微信'),         
             (2,'钉钉'),                    
            )
    ORDER_TYPE = (
         (0,'SQL审核'),
         (1,'代码部署'),         
         (2,'文件上传'),    
         (3,'文件下载'),                 
        )     
    order_type = models.SmallIntegerField(choices=ORDER_TYPE,verbose_name='工单类型')
    grant_group = models.SmallIntegerField(verbose_name='工单授权组')
    mode =  models.SmallIntegerField(choices=TYPE,verbose_name='工单类型')
    number = models.TextField(verbose_name='通知人') 
    '''自定义权限'''
    class Meta:
        db_table = 'opsmanage_order_notice_config'
        default_permissions = ()
        permissions = (
            ("orders_read_notice_config", "读取工单通知配置表权限"),
            ("orders_change_notice_config", "更改工单通知配置表权限"),
            ("orders_add_notice_config", "添加工单通知配置表权限"),
            ("orders_delete_notice_config", "删除工单通知配置表权限"),              
        )        
        unique_together = (("order_type","mode"))
        verbose_name = '工单管理'  
        verbose_name_plural = '工单通知配置表'          