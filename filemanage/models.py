# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from orders.models import Order_System
# Create your models here.


class FileUpload_Audit_Order(models.Model):
    order = models.OneToOneField(Order_System, on_delete=models.CASCADE) 
    dest_path = models.CharField(max_length=200,verbose_name='目标服务器文件路径')
    order_content =  models.TextField(verbose_name='工单申请内容') 
    dest_server = models.TextField(verbose_name='目标服务器')
    chown_user = models.CharField(max_length=100,verbose_name='文件宿主')
    chown_rwx = models.CharField(max_length=100,verbose_name='文件权限')
    class Meta:
        db_table = 'opsmanage_fileupload_audit_order'
        permissions = (
            ("filemanage_read_fileupload_audit_order", "读取文件上传审核工单权限"),
            ("filemanage_change_fileupload_audit_order", "更改文件上传审核工单权限"),
            ("filemanage_add_fileupload_audit_order", "添加文件上传审核工单权限"),
            ("filemanage_delete_fileupload_audit_order", "删除文件上传审核工单权限"),              
        )
        default_permissions = ()
        verbose_name = '工单管理'  
        verbose_name_plural = '文件上传审核工单表'  

class UploadFiles(models.Model):
    file_order = models.ForeignKey('FileUpload_Audit_Order', related_name='uploadfiles', on_delete=models.CASCADE)
    file_path = models.FileField(upload_to = './file/upload/%Y%m%d%H%M%S/',verbose_name='文件上传路径',max_length=500)
    file_type = models.CharField(max_length=100,blank=True,null=True,verbose_name='文件类型')
    class Meta:
        db_table = 'opsmanage_uploadfiles'
        default_permissions = ()

class FileDownload_Audit_Order(models.Model):
    order = models.OneToOneField(Order_System, on_delete=models.CASCADE) 
    order_content =  models.TextField(verbose_name='工单申请内容')
    dest_server = models.TextField(verbose_name='目标服务器')
    dest_path = models.CharField(max_length=200,verbose_name='文件路径')
    class Meta:
        db_table = 'opsmanage_filedownload_audit_order'
        permissions = (
            ("filemanage_read_filedownload_audit_order", "读取文件下载审核工单权限"),
            ("filemanage_change_filedownload_audit_order", "更改文件下载审核工单权限"),
            ("filemanage_add_filedownload_audit_order", "添加文件下载审核工单权限"),
            ("filemanage_delete_filedownload_audit_order", "删除文件下载审核工单权限"),              
        )
        default_permissions = ()
        verbose_name = '工单管理'  
        verbose_name_plural = '文件下载审核工单表'  