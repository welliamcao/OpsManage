#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
import os, json, uuid
from navbar.models import *
from utils.logger import logger 
from utils.avatar import AVATAR 
from django.http import QueryDict
from dao.base import DataHandle
from datetime import datetime,timedelta,date


class NavBarNumber(DataHandle):   
    def __init__(self):
        super(NavBarNumber,self).__init__()  
    
    def get_navbar_type(self,id):
        try:
            return Nav_Type.objects.get(id=id)
        except Exception as ex:
            logger.warn(msg="查询导航栏类型失败: {ex}".format(ex=ex))  
            return False              
        
    def createNavBar(self,request):
        fileName = '/upload/navbar/{ram}.png'.format(ram=uuid.uuid4().hex[0:8]) 
        try:
            navbar = Nav_Type_Number.objects.create(
                                          nav_type=self.get_navbar_type(request.data.get('nav_type')),
                                          nav_name=request.data.get('nav_name'),
                                          nav_desc=request.data.get('nav_desc'),
                                          nav_url=request.data.get('nav_url'),
                                          nav_img=fileName,
                                          )  
        except Exception as ex:
            logger.warn(msg="添加导航栏失败: {ex}".format(ex=ex))  
            return "添加导航栏失败: {ex}".format(ex=ex)
        try:
            AVATAR.generate_image(request.data.get('nav_name')[0], os.getcwd() + str(navbar.nav_img),AVATAR.randomColor())  
        except Exception as ex:
            navbar.delete()
            logger.warn(msg="创建导航栏缩略图失败: {ex}".format(ex=ex))  
            return "创建导航栏缩略图失败: {ex}".format(ex=ex)         
        return navbar      
    
    def updateImg(self,navbar):
        AVATAR.generate_image(str(navbar.nav_name)[0], os.getcwd() + str(navbar.nav_img), AVATAR.randomColor())  

class NavBarThirdNumber(object):
    
    def get_navbar(self,id):
        try:
            return Nav_Third.objects.get(id=id)
        except Exception as ex:
            logger.warn(msg="查询第三方接入类型失败: {ex}".format(ex=ex))  
            return False  
    
    def get_navbar_number(self,id):
        try:
            return Nav_Third_Number.objects.get(id=id)
        except Exception as ex:
            logger.warn(msg="查询第三方接入失败: {ex}".format(ex=ex))  
            return False  
    
NAVBAR = NavBarNumber()        