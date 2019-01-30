#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import uuid,os,json
from django.http import QueryDict
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from deploy.models import *
from utils.ansible_api_v2 import ANSRunner
from django.contrib.auth.decorators import permission_required
from utils.logger import logger
from dao.assets import AssetsBase,AssetsSource
from dao.database import DBConfig,DBManage,DBUser
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.base import method_decorator_adaptor


class DatabaseConfigs(LoginRequiredMixin,DBConfig,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        if request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'),request)
            if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
            return JsonResponse({'msg':"查询成功","code":200,'data':res})     
        return render(request, 'database/db_config.html',{"user":request.user}) 
        
        
class DatabaseUsers(LoginRequiredMixin,DBUser,View):
    login_url = '/login/'
    
    def get(self, request, *args, **kwagrs):
        res = self.allowcator(request.GET.get('type','get_all_user_db'),request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"查询成功","code":200,'data':res})     
    
    def post(self, request, *args, **kwagrs):
        res = self.create_user_database(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"添加成功","code":200,'data':[]})     

    def put(self, request, *args, **kwagrs):
        res = self.update_user_database(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':[]})       

    def delete(self, request, *args, **kwagrs):
        res = self.delete_user_database(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':[]}) 
 

class DatabaseManage(LoginRequiredMixin,DBManage,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        if request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'),request)
            if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
            return JsonResponse({'msg':"查询成功","code":200,'data':res})         
        return render(request, 'database/db_manage.html',{"user":request.user,"assets":self.base()})    
    
    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('model'),request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})     
        return JsonResponse({'msg':"操作成功","code":200,'data':res})  