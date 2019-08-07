#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group,Permission
from django.db.models import Q 
from orders.models import Order_System
from django.http import QueryDict
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from dao.users import UsersManage,GroupManageBase
from django.contrib.auth.decorators import permission_required
from utils.base import method_decorator_adaptor
   


class UserManage(LoginRequiredMixin,UsersManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "asset.assets_read_user","/403/")  
    def get(self, request, *args, **kwagrs):
        if request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'), request)
            if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
            return JsonResponse({'msg':"查询成功","code":200,'data':res})  
        return render(request,'users/user_manage.html',{"user":request.user})   
    
    @method_decorator_adaptor(permission_required, "asset.assets_change_user","/403/") 
    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('type'), request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res})              


class GroupManage(LoginRequiredMixin,GroupManageBase,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        if request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'), request)
            if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
            return JsonResponse({'msg':"查询成功","code":200,'data':res})  
        return JsonResponse({'msg':"查询成功","code":200,'data':None})    
    
    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('type'), request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res}) 
    
    
class UserCenter(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request,'users/user_center.html',{"user":request.user})     