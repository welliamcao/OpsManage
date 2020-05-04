#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import time
from django.db import models
from account.models import User
from utils import base

ORDER_EXECUTE_STATUS = (
      (0,'已提交'),
      (1,'处理中'),
      (2,'已完成'),
      (3,'已回滚'),
      (4,'已关闭'),      
      (5,'已失败'),         
    ) 

ORDER_AUDIT_STATUS = (
      (1,'已拒绝'),
      (2,'审核中'),
      (3,'已授权'),             
    ) 

ORDER_AUDIT_STATUS_DICT = {
    "1":'已拒绝',
    "2":'审核中',
    "3":'已授权'
    }

ORDER_EXECUTE_STATUS_DICT = {
    "0":'已提交',
    "1":'处理中',
    "2":'已完成',
    "3":'已回滚',
    "4":'已关闭',
    "5":'执行失败',
    }

class Order_System(models.Model):

    LEVEL = (
             (0,'普通'),
             (1,'紧急'),
             )
    TYPE = (
             (0,'SQL审核'),
             (1,'运维服务'),         
             (2,'文件上传'),    
             (3,'文件下载'),                 
            )
    order_user = models.SmallIntegerField(verbose_name='工单申请人id')
    order_subject = models.CharField(max_length=200,blank=True,null=True,verbose_name='工单申请主题')   
    order_executor = models.SmallIntegerField(verbose_name='工单审核人')
    order_audit_status = models.SmallIntegerField(choices=ORDER_AUDIT_STATUS,default=2,verbose_name='工单审核状态') 
    order_execute_status = models.SmallIntegerField(choices=ORDER_EXECUTE_STATUS,default=0,verbose_name='工单提交状态') 
    order_level = models.IntegerField(choices=LEVEL,blank=True,null=True,verbose_name='工单紧急程度')
    order_type = models.SmallIntegerField(choices=TYPE,verbose_name='工单类型')
    order_mark = models.TextField(blank=True,null=True,verbose_name='备注') 
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='工单发布时间')
    modify_time = models.DateTimeField(auto_now=True,blank=True,verbose_name='工单最后修改时间')
    start_time = models.DateTimeField(verbose_name='工单开始时间',blank=True, null=True) 
    end_time = models.DateTimeField(verbose_name='工单结束时间',blank=True, null=True)    
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
    
    def is_expired(self):
        current_time = int(time.time())
        
        if base.changeTotimestamp(self.end_time.strftime('%Y-%m-%d %H:%M:%S')) - current_time < 0:#如果已过工单执行时间就返回False
            return 0 
        
        return 1        
        
     
    
    def is_unexpired(self):
        current_time = int(time.time())
        
        if base.changeTotimestamp(self.start_time.strftime('%Y-%m-%d %H:%M:%S')) - current_time > 0:#如果未到工单执行时间就返回False 
            return 0 
        
        return 1          

    
    def to_json(self):        
        json_format = {
            "id":self.id,
            "order_user":self.order_user,
            "order_subject":self.order_subject,          
            "order_executor":self.order_executor,
            "order_audit_status":self.order_audit_status,
            "order_execute_status":self.order_execute_status,
            "order_level":self.order_level,
            "order_type":self.order_type,
            "order_mark":self.order_mark,
            "modify_time":self.modify_time.strftime('%Y-%m-%d %H:%M:%S'),
            "create_time":self.create_time.strftime('%Y-%m-%d %H:%M:%S'),     
            "start_time":self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end_time":self.end_time.strftime('%Y-%m-%d %H:%M:%S'),                              
        }
        return  json_format 


class OrderLog(models.Model):
    order = models.IntegerField(verbose_name='工单id', db_index=True)
    audit_status = models.SmallIntegerField(choices=ORDER_AUDIT_STATUS,verbose_name='工单审核状态')
    execute_status = models.SmallIntegerField(choices=ORDER_EXECUTE_STATUS,verbose_name='工单审核状态')
    operator = models.SmallIntegerField(verbose_name='操作人')
    operation_info = models.TextField(verbose_name='操作信息',blank=True,null=True)
    operation_time = models.DateTimeField(auto_now=True,verbose_name='工单操作时间')

    class Meta:
        db_table = 'opsmanage_order_system_log'
        default_permissions = ()        
        verbose_name = u'工单管理'
        verbose_name_plural = u'工单流日志'
        
    def to_json(self):
        try:
            username = User.objects.get(id=self.operator).name
        except Exception as ex:
            username = "未知"
        
        json_format = {
            "order":self.order,
            "audit_status":self.audit_status,          
            "execute_status":self.execute_status, 
            "operator":username,
            "operation_info":self.operation_info,
            "operation_time":self.operation_time.strftime('%Y-%m-%d %H:%M:%S'),           
        }
        return  json_format  
        
class SQL_Audit_Order(models.Model):
    order = models.OneToOneField('Order_System', on_delete=models.CASCADE) 
    order_type = models.CharField(max_length=10,verbose_name='sql类型')
    order_db = models.ForeignKey('databases.Database_MySQL_Detail',related_name ='order_db',verbose_name='数据库id', on_delete=models.CASCADE)
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

    def to_json(self):
        json_format = {
            "id":self.id,
            "order_type":self.order_type,
            "order_sql":self.order_sql,
            "order_file":str(self.order_file).split('/')[-1],
            "order_err":self.order_err if self.order_err else '无',
            "sql_backup":self.sql_backup,           
            "db":{}
        }
        json_format["db"] = self.order_db.to_json()
        return  json_format  

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

    def to_json(self):
        json_format = {
            "id":self.id,
            "stage":self.stage,
            "errlevel":self.errlevel,
            "stagestatus":self.stagestatus,
            "errormessage":self.errormessage,
            "sqltext":self.sqltext,           
            "affectrow":self.affectrow,
            "sequence":self.sequence,
            "backup_db":self.backup_db,
            "execute_time":self.execute_time,
            "sqlsha":self.sqlsha,
            "create_time":self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return  json_format  

class FileUpload_Audit_Order(models.Model):
    order = models.OneToOneField(Order_System, on_delete=models.CASCADE) 
    dest_path = models.CharField(max_length=200,verbose_name='目标服务器文件路径')
    order_content =  models.TextField(verbose_name='工单申请内容') 
    dest_server = models.TextField(verbose_name='目标服务器')
    chown_user = models.CharField(max_length=100,verbose_name='文件宿主')
    chown_rwx = models.CharField(max_length=100,verbose_name='文件权限')
    class Meta:
        db_table = 'opsmanage_fileupload_audit_order'
        default_permissions = ()
        verbose_name = '工单管理'  
        verbose_name_plural = '文件上传审核工单表'  

    def to_json(self):
        json_format = {
            "id":self.id,
            "dest_path":self.dest_path,
            "order_content":self.order_content,
            "dest_server":self.dest_server,
            "chown_user":self.chown_user,
            "chown_rwx":self.chown_rwx,           
        }
        return  json_format  

class UploadFiles(models.Model):
    file_order = models.ForeignKey('FileUpload_Audit_Order', related_name='uploadfiles', on_delete=models.CASCADE)
    file_path = models.FileField(upload_to = './file/upload/%Y%m%d%H%M%S/',verbose_name='文件上传路径',max_length=500)
    file_type = models.CharField(max_length=100,blank=True,null=True,verbose_name='文件类型')
    class Meta:
        db_table = 'opsmanage_uploadfiles'
        default_permissions = ()

    def to_json(self):
        
        if self.file_path:
            file_path = str(self.file_path).split("/")[-1]           
        
        json_format = {
            "id":self.id,
            "file_path":file_path,
            "file_type":self.file_type,        
        }
        return  json_format 

class FileDownload_Audit_Order(models.Model):
    order = models.OneToOneField(Order_System, on_delete=models.CASCADE) 
    order_content =  models.TextField(verbose_name='工单申请内容')
    dest_server = models.TextField(verbose_name='目标服务器')
    dest_path = models.CharField(max_length=200,verbose_name='文件路径')
    class Meta:
        db_table = 'opsmanage_filedownload_audit_order'
        default_permissions = ()
        verbose_name = '工单管理'  
        verbose_name_plural = '文件下载审核工单表'  

    def to_json(self):        
        json_format = {
            "id":self.id,
            "dest_path":self.dest_path,
            "order_content":self.order_content,
            "dest_server":self.dest_server,     
        }
        return  json_format

class Service_Audit_Order(models.Model):
    order = models.OneToOneField(Order_System, on_delete=models.CASCADE) 
    order_content =  models.TextField(verbose_name='工单申请内容') 
    file_path = models.FileField(upload_to = './order/upload/%Y%m%d%H%M%S/',verbose_name='文件上传路径',max_length=500,blank=True,null=True)
    file_type = models.CharField(max_length=100,blank=True,null=True,verbose_name='文件类型')   
    file_md5 =  models.CharField(max_length=50,blank=True,null=True,verbose_name='文件md5值')  
    modify_time = models.DateTimeField(auto_now=True,blank=True,verbose_name='工单最后修改时间')    
    class Meta:
        db_table = 'opsmanage_service_audit_order'
        default_permissions = ()
        verbose_name = '工单管理'  
        verbose_name_plural = '运维服务审核工单表'     

    def to_json(self):
        
        file_path = str(self.file_path).split('/')[-1]
        
        json_format = {
            "id":self.id,
            "file_path":file_path,
            "order_content":self.order_content,
            "file_type":self.file_type,
            "file_md5":self.file_md5,       
            "modify_time":self.modify_time.strftime('%Y-%m-%d %H:%M:%S'),  
        }
        return  json_format
        
class Order_Notice_Config(models.Model):   
    TYPE = (
             (0,'邮箱'),
             (1,'微信'),         
             (2,'钉钉'),                    
            )
    ORDER_TYPE = (
         (0,'SQL审核'),
         (1,'运维服务'),         
         (2,'文件上传'),    
         (3,'文件下载'),                 
        )     
    order_type = models.SmallIntegerField(choices=ORDER_TYPE,verbose_name='工单类型')
#     grant_group = models.SmallIntegerField(verbose_name='工单授权组')
    mode =  models.SmallIntegerField(choices=TYPE,verbose_name='工单类型')
#     number = models.TextField(verbose_name='通知人') 
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
                