#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.base import method_decorator_adaptor
from django.contrib.auth.decorators import permission_required      
from django.http import JsonResponse
from dao.ipvs import IVPSManage

class Lists(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'apply/ipvs/list.html',{"user":request.user})

class VipStatus(LoginRequiredMixin,IVPSManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_change_ipvs_config","/403/") 
    def put(self, request, *args, **kwagrs):
        res = self.vip_status(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res}) 


class RsStatus(LoginRequiredMixin,IVPSManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_change_ipvs_config","/403/") 
    def put(self, request, *args, **kwagrs):
        res = self.rs_status(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res})
    
class VipBatch(LoginRequiredMixin,IVPSManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_change_ipvs_config","/403/") 
    def put(self, request, *args, **kwagrs):
        res = self.vip_batch_modf(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res})    
    
class RsBatch(LoginRequiredMixin,IVPSManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_change_ipvs_config","/403/") 
    def put(self, request, *args, **kwagrs):
        res = self.rs_batch_modf(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res}) 
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_delete_ipvs_config","/403/")     
    def delete(self, request, *args, **kwagrs):
        res = self.rs_batch_delete(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res})  
    
class NsBatch(LoginRequiredMixin,IVPSManage,View):
    login_url = '/login/'

    @method_decorator_adaptor(permission_required, "apply.ipvs_delete_ipvs_config","/403/")     
    def delete(self, request, *args, **kwagrs):
        res = self.ns_batch_delete(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res})        