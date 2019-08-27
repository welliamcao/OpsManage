# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time,os
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from wiki.models import  Tag,Post,Category
from django.contrib.auth.models import User
from utils.logger import logger
from utils import base 
# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt





@login_required()
@permission_required('wiki.wiki_can_add_wiki_post',login_url='/noperm/')
def article_add(request):
    if request.method == "GET":
        tagList = Tag.objects.all()
        categoryList = Category.objects.all()
        return render(request,'wiki/wiki_post.html',{"user":request.user,"tagList":tagList,"categoryList":categoryList})
    elif request.method == "POST":  
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tags = request.POST.getlist('tag[]')
        try:
            category = Category.objects.get(id=category)
        except Exception as ex:
            logger.warn(msg="获取分类失败: {ex}".format(ex=str(ex)))  
            return  JsonResponse({'msg':"获取分类失败: {ex}".format(ex=str(ex)),"code":500,'data':[]})              
        try:
            article = Post.objects.create(title=title,content=content,category=category,
                                      author=User.objects.get(username=request.user))
        except Exception as ex:
            logger.warn(msg="创建文章失败: {ex}".format(ex=str(ex)))  
            return  JsonResponse({'msg':"创建文章失败: {ex}".format(ex=str(ex)),"code":500,'data':[]})  
        try:        
            for tg in tags:
                tag = Tag.objects.get(id=tg)
                article.tags.add(tag)
        except Exception as ex:
            logger.warn(msg="创建文章标签失败: {ex}".format(ex=str(ex))) 
        return  JsonResponse({'msg':"文章添加成功","code":200,'data':[]})
    
@login_required()
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        f = request.FILES["upload"]
        callback = request.GET.get('CKEditorFuncNum','1')
        if f:
            try:
                datePath =  time.strftime("%Y/%m/%d/",time.localtime())
                path = os.getcwd() + "/upload/wiki/" + datePath
                filePath = path  + f.name
                if os.path.isdir(os.path.dirname(filePath)) is not True:os.makedirs(os.path.dirname(filePath))
                with open(filePath, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            except Exception as ex:
                logger.error(msg="上传图片失败: {ex}".format(ex=ex))
            res = "<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'/"+ 'wiki/upload/' + datePath + f.name +"', '');</script>"
            return HttpResponse (res)
        else:
            return JsonResponse({'msg':"图片上传失败","code":500,'data':[]})


@login_required()
@permission_required('wiki.wiki_can_edit_wiki_post',login_url='/noperm/')
def article_edit(request,pid):
    try:
        article = Post.objects.select_related().get(id=pid)
    except Exception as ex:
        logger.error(msg="文章不存在: {ex}".format(ex=ex))
        return render(request,'wiki/wiki_edit.html',{"user":request.user,"errorInfo":ex})
    if request.method == "GET":
        tagList = Tag.objects.all()
        categoryList = Category.objects.all()
        article.tag = [ t.id for t in  article.tags.all() ]
        return render(request,'wiki/wiki_edit.html',{"user":request.user,"tagList":tagList,"categoryList":categoryList,"article":article})
    elif request.method == "POST": 
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tags = request.POST.getlist('tag[]')
        try:
            category = Category.objects.get(id=category)
        except Exception as ex:
            logger.warn(msg="获取分类失败: {ex}".format(ex=str(ex)))  
            return  JsonResponse({'msg':"获取分类失败: {ex}".format(ex=str(ex)),"code":500,'data':[]})              
        try:
            Post.objects.filter(id=pid).update(title=title,content=content,category=category,
                                    author=User.objects.get(username=request.user))
        except Exception as ex:
            logger.warn(msg="更新文章失败: {ex}".format(ex=str(ex)))  
            return  JsonResponse({'msg':"更新文章失败: {ex}".format(ex=str(ex)),"code":500,'data':[]}) 
        try:
            newTagsList = []
            for tg in tags:
                newTagsList.append(int(tg))
        except Exception as ex:
            logger.warn(msg="获取文章标签失败: {ex}".format(ex=ex)) 
        try:  
            oldTagsList = [ t.id for t in  article.tags.all() ]
            addTagsList = list(set(newTagsList).difference(set(oldTagsList)))
            delTagsList = list(set(oldTagsList).difference(set(newTagsList)))      
            for tg in addTagsList:
                tag = Tag.objects.get(id=tg)
                article.tags.add(tag)
            for tg in delTagsList:
                tag = Tag.objects.get(id=tg)
                article.tags.remove(tag)                
        except Exception as ex:
            logger.warn(msg="更新文章标签失败: {ex}".format(ex=ex)) 
        return  JsonResponse({'msg':"文章添加成功","code":200,'data':[]})        

@login_required()
@permission_required('wiki.wiki_can_read_wiki_post',login_url='/noperm/')
def article_index(request):
    tagList = Tag.objects.all()
    categoryList = []
    for ds in Category.objects.all():
        ds.post_count = Post.objects.filter(category=ds).count()
        categoryList.append(ds)
    postList = Post.objects.all().order_by('-id')[:10]   
    dateList = Post.objects.raw('SELECT id,DATE_FORMAT( created_time, "%%Y/%%m" ) as cdate , COUNT(*) as count FROM opsmanage_wiki_post GROUP BY DATE_FORMAT( created_time, "%%Y/%%m" );')   
    return render(request,'wiki/wiki_base.html',{"user":request.user,"tagList":tagList,"categoryList":categoryList,"postList":postList,"dateList":dateList})


@login_required()
@permission_required('wiki.wiki_can_read_wiki_post',login_url='/noperm/')
def article_show(request,pid):
    try:
        article = Post.objects.select_related().get(id=pid)
    except Exception as ex:
        logger.error(msg="文章不存在: {ex}".format(ex=ex))
        return render(request,'wiki/wiki_show.html',{"user":request.user,"errorInfo":ex})
    if request.method == "GET":
        tagList = Tag.objects.all()
        categoryList = Category.objects.all()
        article.tag = [ t.id for t in  article.tags.all() ]
        postList = Post.objects.all().order_by('-id')[:5]
        categoryList = []
        for ds in Category.objects.all():
            ds.post_count = Post.objects.filter(category=ds).count()
            categoryList.append(ds)    
        dateList = Post.objects.raw('SELECT id,DATE_FORMAT( created_time, "%%Y/%%m" ) as cdate , COUNT(*) as count FROM opsmanage_wiki_post GROUP BY DATE_FORMAT( created_time, "%%Y/%%m" );')   
        return render(request,'wiki/wiki_show.html',{"user":request.user,"tagList":tagList,
                                                     "categoryList":categoryList,"article":article,
                                                     "postList":postList,"dateList":dateList})
        
@login_required()
@permission_required('wiki.wiki_can_read_wiki_post',login_url='/noperm/')
def article_category(request,pid):
    try:
        category = Category.objects.get(id=pid)
    except Exception as ex:
        logger.warn(msg="分类不存在: {ex}".format(ex=ex))
        return render(request,'wiki/wiki_base.html',{"user":request.user,"errorInfo":"分类不存在: {ex}".format(ex=ex)}) 
    categoryList = []
    for ds in Category.objects.all():
        ds.post_count = Post.objects.filter(category=ds).count()
        categoryList.append(ds)    
    postList = Post.objects.filter(category=category).order_by('-id')
    dateList = Post.objects.raw('SELECT id,DATE_FORMAT( created_time, "%%Y/%%m" ) as cdate , COUNT(*) as count FROM opsmanage_wiki_post GROUP BY DATE_FORMAT( created_time, "%%Y/%%m" );')
    tagList = Tag.objects.all()
    return render(request,'wiki/wiki_base.html',{"user":request.user,"postList":postList,"dateList":dateList,"tagList":tagList,"categoryList":categoryList})   

@login_required()
@permission_required('wiki.wiki_can_read_wiki_post',login_url='/noperm/')
def article_tag(request,pid):
    try:
        tag = Tag.objects.get(id=pid)
    except Exception as ex:
        logger.warn(msg="标签不存在: {ex}".format(ex=ex))
        return render(request,'wiki/wiki_base.html',{"user":request.user,"errorInfo":"标签不存在: {ex}".format(ex=ex)}) 
    categoryList = []
    for ds in Category.objects.all():
        ds.post_count = Post.objects.filter(category=ds).count()
        categoryList.append(ds)    
    postList = Post.objects.filter(tags=tag.id).order_by('-id')
    dateList = Post.objects.raw('SELECT id,DATE_FORMAT( created_time, "%%Y/%%m" ) as cdate , COUNT(*) as count FROM opsmanage_wiki_post GROUP BY DATE_FORMAT( created_time, "%%Y/%%m" );')
    tagList = Tag.objects.all()
    return render(request,'wiki/wiki_base.html',{"user":request.user,"postList":postList,"dateList":dateList,"tagList":tagList,"categoryList":categoryList})  

@login_required()
@permission_required('wiki.wiki_can_read_wiki_post',login_url='/noperm/')
def article_archive(request,month):
    try:
        archiveDate =  base.getMonthFirstDayAndLastDay(month.split('/')[0],month.split('/')[1])
    except Exception as ex:
        return render(request,'wiki/wiki_base.html',{"user":request.user,"errorInfo":"归档时间不存在: {ex}".format(ex=ex)}) 
    categoryList = []
    for ds in Category.objects.all():
        ds.post_count = Post.objects.filter(category=ds).count()
        categoryList.append(ds)    
    postList = Post.objects.raw('''SELECT * FROM opsmanage_wiki_post WHERE created_time>='{startime}' AND created_time<='{endtime}' ORDER BY id DESC;'''.format(startime=str(archiveDate[0]) +' 00:00:00',endtime=str(archiveDate[1]) + ' 23:59:59'))
    dateList = Post.objects.raw('SELECT id,DATE_FORMAT( created_time, "%%Y/%%m" ) as cdate , COUNT(*) as count FROM opsmanage_wiki_post GROUP BY DATE_FORMAT( created_time, "%%Y/%%m" );')
    tagList = Tag.objects.all()
    return render(request,'wiki/wiki_base.html',{"user":request.user,"postList":postList,"dateList":dateList,"tagList":tagList,"categoryList":categoryList}) 

        
