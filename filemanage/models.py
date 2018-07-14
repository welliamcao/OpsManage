# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from orders.models import Order_System
# Create your models here.
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class FileUpload_Audit_Order(models.Model):
    order = models.OneToOneField(Order_System) 
    dest_path = models.CharField(max_length=200,verbose_name='目标服务器文件路径')
    order_content =  models.TextField(verbose_name='工单申请内容') 
    dest_server = models.TextField(verbose_name='目标服务器')
    chown_user = models.CharField(max_length=100,verbose_name='文件宿主')
    chown_rwx = models.CharField(max_length=100,verbose_name='文件权限')
    class Meta:
        db_table = 'opsmanage_fileupload_audit_order'
        permissions = (
            ("can_read_fileupload_audit_order", "读取文件上传审核工单权限"),
            ("can_change_fileupload_audit_order", "更改文件上传审核工单权限"),
            ("can_add_fileupload_audit_order", "添加文件上传审核工单权限"),
            ("can_delete_fileupload_audit_order", "删除文件上传审核工单权限"),              
        )
        verbose_name = '文件上传审核工单表'  
        verbose_name_plural = '文件上传审核工单表'  

class UploadFiles(models.Model):
    file_order = models.ForeignKey('FileUpload_Audit_Order', related_name='files', on_delete=models.CASCADE)
    file_path = models.FileField(upload_to = './file/upload/%Y%m%d%H%M%S/',verbose_name='文件上传路径',max_length=500)
    file_type = models.CharField(max_length=100,blank=True,null=True,verbose_name='文件类型')
    class Meta:
        db_table = 'opsmanage_uploadfiles'

class FileDownload_Audit_Order(models.Model):
    order = models.OneToOneField(Order_System) 
    order_content =  models.TextField(verbose_name='工单申请内容')
    dest_server = models.TextField(verbose_name='目标服务器')
    dest_path = models.CharField(max_length=200,verbose_name='文件路径')
    class Meta:
        db_table = 'opsmanage_filedownload_audit_order'
        permissions = (
            ("can_read_filedownload_audit_order", "读取文件下载审核工单权限"),
            ("can_change_filedownload_audit_order", "更改文件下载审核工单权限"),
            ("can_add_filedownload_audit_order", "添加文件下载审核工单权限"),
            ("can_delete_filedownload_audit_order", "删除文件下载审核工单权限"),              
        )
        verbose_name = '文件上传审核工单表'  
        verbose_name_plural = '文件下载审核工单表'  