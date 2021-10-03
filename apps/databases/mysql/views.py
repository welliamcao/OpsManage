#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from dao.mysql import DBConfig, DBManage
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.base import method_decorator_adaptor
from django.contrib.auth.decorators import permission_required

class DatabaseConfigView(LoginRequiredMixin,DBConfig,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "databases.database_read_mysql_server_config","/403/")
    def get(self, request, *args, **kwagrs):
        return render(request, 'database/mysql/db_config.html',{"user":request.user})       
        

class DatabaseManageView(LoginRequiredMixin,DBManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "databases.database_read_mysql_server_config","/403/")
    def get(self, request, *args, **kwagrs):
        if request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'),request)
            if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
            return JsonResponse({'msg':"查询成功","code":200,'data':res})         
        return render(request, 'database/mysql/db_manage.html',{"user":request.user})    
    
#     @method_decorator_adaptor(permission_required, "databases.database_add_mysql_server_config","/403/")
    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('model'),request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})     
        return JsonResponse({'msg':"操作成功","code":200,'data':res})  
    
    
class DatabaseQueryView(LoginRequiredMixin,DBManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "databases.database_query_mysql_server_config","/403/")
    def get(self, request, *args, **kwagrs):       
        return render(request, 'database/mysql/db_query.html',{"user":request.user})     
    
    
class DatabaseExecuteHistoryView(LoginRequiredMixin,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "databases.database_read_sql_execute_history","/403/")
    def get(self, request, *args, **kwagrs):       
        return render(request, 'database/mysql/db_history.html',{"user":request.user})      