#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from dao.crontab import CrontabManage
from dao.celerys import CeleryTaskManage
from dao.apsched import ApschedNodeManage,ApschedNodeJobsManage
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from utils.base import method_decorator_adaptor

class CronManage(LoginRequiredMixin,CrontabManage,View):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_read_cron_config","/403/") 
    def get(self, request, *args, **kwagrs):
        if request.GET.get('id'):
            return JsonResponse({'msg':"计划任务查询成功","code":200,'data':self.get_crontab(request)}) 
        return render(request, 'sched/cron_manage.html',{"user":request.user})
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_add_cron_config","/403/") 
    def post(self, request, *args, **kwagrs):
        if request.POST.get('type') == 'view':res = self.view_logs(request)
        elif request.POST.get('type') == 'disabled':res = self.disabled(request)
        elif request.POST.get('type') == 'enable':res = self.enable(request)
        else:res = self.create_crontab(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res})     

    @method_decorator_adaptor(permission_required, "sched.cron_can_change_cron_config","/403/") 
    def put(self, request, *args, **kwagrs):
        res = self.update_crontab(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res})       

    @method_decorator_adaptor(permission_required, "sched.cron_can_delete_cron_config","/403/")
    def delete(self, request, *args, **kwagrs):
        res = self.delete_crontab(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"删除成功","code":200,'data':[]})     
    
    
class CeleryManage(LoginRequiredMixin,CeleryTaskManage,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request, 'sched/celery_manage.html',{"user":request.user,"tasks":self.base()})
    
    def post(self, request, *args, **kwagrs):
        if request.POST.get('type') == 'view':res = self.view_logs(request)
        elif request.POST.get('type') == 'disabled':res = self.disabled(request)
        elif request.POST.get('type') == 'enable':res = self.enable(request)
        else:res = self.create_crontab(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res})     

    def put(self, request, *args, **kwagrs):
        res = self.update_crontab(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res})       

    def delete(self, request, *args, **kwagrs):
        res = self.delete_crontab(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"删除成功","code":200,'data':[]})     
    
    
    
class ApsManage(LoginRequiredMixin,View):   
    login_url = '/login/'
    
    def get(self, request, *args, **kwagrs):
        return render(request, 'sched/apsched_manage.html',{"user":request.user})
    
class ApsNodeManage(LoginRequiredMixin,ApschedNodeManage,View):   
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_read_cron_config","/403/") 
    def get(self, request, *args, **kwagrs):
        return render(request, 'sched/apsched_manage.html',{"user":request.user})   
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_add_cron_config","/403/") 
    def post(self,request, *args, **kwagrs): 
        res = self.create_node(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':[]})
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_change_cron_config","/403/") 
    def put(self, request, *args, **kwagrs):
        res = self.update_node(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"修改成功","code":200,'data':res}) 
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_delete_cron_config","/403/") 
    def delete(self, request, *args, **kwagrs):
        res = self.delete_node(request=request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"删除成功","code":200,'data':[]})  
    
    
class ApsNodeJobsManage(LoginRequiredMixin,ApschedNodeJobsManage,View):  
    login_url = '/login/' 
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_add_cron_config","/403/") 
    def post(self,request, *args, **kwagrs): 
        res = self.create_jobs(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':[]})   
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_change_cron_config","/403/")
    def put(self,request, *args, **kwagrs): 
        res = self.update_jobs(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':[]})   
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_delete_cron_config","/403/") 
    def delete(self,request, *args, **kwagrs): 
        res = self.delete_jobs(request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':[]})                   