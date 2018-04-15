# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='分类名称',unique=True)
    class Meta:
        db_table = 'opsmanage_wiki_category'
        permissions = (
            ("can_read_wiki_category", "读取分类权限"),
            ("can_change_wiki_category", "更改分类权限"),
            ("can_add_wiki_category", "添加分类权限"),
            ("can_delete_wiki_category", "删除分类权限"),              
        )
        verbose_name = 'wiki分类'  
        verbose_name_plural = 'wiki分类'     
    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=100,verbose_name='标签类型',unique=True)
    class Meta:
        db_table = 'opsmanage_wiki_tag'
        permissions = (
            ("can_read_wiki_tag", "读取标签权限"),
            ("can_change_wiki_tag", "更改标签权限"),
            ("can_add_wiki_tag", "添加标签权限"),
            ("can_delete_wiki_tag", "删除标签权限"),              
        )
        verbose_name = 'wiki标签'  
        verbose_name_plural = 'wiki标签'    
    def __str__(self):
        return self.name



class Post(models.Model):
    title = models.CharField(max_length=70,verbose_name='标题',unique=True)
    content =  models.TextField(verbose_name='类容')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now_add=True,verbose_name='修改时间')
    category = models.ForeignKey(Category,verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True,verbose_name='标签')
    author = models.ForeignKey(User,verbose_name='创建者')

    class Meta:
        db_table = 'opsmanage_wiki_post'
        permissions = (
            ("can_read_wiki_post", "读取文章权限"),
            ("can_change_wiki_post", "更改文章权限"),
            ("can_add_wiki_post", "添加文章权限"),
            ("can_delete_wiki_post", "删除文章权限"),              
        )
        verbose_name = 'wiki文章'  
        verbose_name_plural = 'wiki文章'

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=100,verbose_name='评论用户')
    email = models.EmailField(max_length=255,verbose_name='邮箱')
    url = models.URLField(blank=True,verbose_name='文章地址')
    text = models.TextField(verbose_name='文章类容')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    post = models.ForeignKey('Post',verbose_name='文章id')
    class Meta:
        db_table = 'opsmanage_wiki_comment'
        permissions = (
            ("can_read_wiki_comment", "读取评论权限"),
            ("can_change_wiki_comment", "更改评论权限"),
            ("can_add_wiki_comment", "添加评论权限"),
            ("can_delete_wiki_comment", "删除评论权限"),              
        )
        verbose_name = 'wiki文章评论'  
        verbose_name_plural = 'wiki文章评论'    

    def __str__(self):
        return self.text[:20]

