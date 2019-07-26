#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models

class Nav_Type(models.Model):
    type_name = models.CharField(max_length=100,unique=True) 
    class Meta:
        db_table = 'opsmanage_nav_type'
        default_permissions = ()
        permissions = (
            ("nav_read_nav_type", "读取站内导航权限"),
            ("nav_change_nav_type", "更改站内导航权限"),
            ("nav_add_nav_type", "添加站内导航权限"),
            ("nav_delete_nav_type", "删除站内导航权限"),              
        )  
        verbose_name = '站内导航管理'  
        verbose_name_plural = '站内导航分类表' 
              
    
class Nav_Type_Number(models.Model):
    nav_type = models.ForeignKey('Nav_Type',related_name='nav_type_number', on_delete=models.CASCADE)
    nav_name = models.CharField(max_length=100) 
    nav_desc = models.CharField(max_length=200) 
    nav_url = models.TextField() 
    nav_img = models.FileField(upload_to = './avatar/',verbose_name='图片路径',blank=True,null=True) 
    
    class Meta:
        db_table = 'opsmanage_nav_number'
        default_permissions = ()
        permissions = (
            ("nav_read_nav_number", "读取站内导航详情权限"),
            ("nav_change_nav_number", "更改站内导航详情权限"),
            ("nav_add_nav_number", "添加站内导航详情权限"),
            ("nav_delete_nav_number", "删除站内导航详情权限"),              
        )  
        unique_together = (("nav_type", "nav_name"))
        verbose_name = '站内导航管理'  
        verbose_name_plural = '站内导航详情表' 
        
        
class Nav_Third(models.Model):
    type_name = models.CharField(max_length=100,unique=True) 
    icon = models.CharField(max_length=50) 
    class Meta:
        db_table = 'opsmanage_nav_third'
        default_permissions = () 
        verbose_name = '站内导航管理'  
        verbose_name_plural = '第三方站点分类表' 
              
    
class Nav_Third_Number(models.Model):
    nav_third = models.ForeignKey('Nav_Third',related_name='nav_third_number', on_delete=models.CASCADE)
    nav_name = models.CharField(max_length=100)  
    width = models.CharField(max_length=50,verbose_name='宽度') 
    height = models.CharField(max_length=50,verbose_name='高度') 
    url = models.TextField() 
    
    class Meta:
        db_table = 'opsmanage_nav_third_number'
        default_permissions = () 
        unique_together = (("nav_third", "nav_name"))
        verbose_name = '站内导航管理'  
        verbose_name_plural = '第三方站点详情表'         