#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from wiki.models import Category,Tag,Post
from utils.logger import logger
from django.contrib.auth.models import User
from dao.base import DjangoCustomCursors,DataHandle

class WikeManage(DataHandle):
    def __init__(self):
        super(WikeManage, self).__init__() 
        
    
#     def create_post(self,request): 
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         category = request.POST.get('category')
#         tags = request.POST.getlist('tag[]')
#         try:
#             category = Category.objects.get(id=category)
#         except Exception as ex:
#             logger.warn(msg="获取分类失败: {ex}".format(ex=str(ex)))  
#             return "获取分类失败: {ex}".format(ex=str(ex))             
#         try:
#             article = Post.objects.create(title=title,content=content,category=category,
#                                       author=User.objects.get(username=request.user))
#         except Exception as ex:
#             logger.warn(msg="创建文章失败: {ex}".format(ex=str(ex)))
#             return "创建文章失败: {ex}".format(ex=str(ex))    
#         try:        
#             for tg in tags:
#                 tag = Tag.objects.get(id=tg)
#                 article.tags.add(tag)
#         except Exception as ex:
#             logger.warn(msg="创建文章标签失败: {ex}".format(ex=str(ex)))  
#         return article       