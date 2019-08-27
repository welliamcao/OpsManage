#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import os, json
from utils import base
from django.views.generic import View
from django.http import HttpResponseRedirect,JsonResponse,StreamingHttpResponse
from django.shortcuts import render
from dao.orders import (ApplyManage,OrderSQLManage,
                        OrderFileDownloadManage,OrderStatus,
                        OrderFileUploadManage)
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.logger import logger

class OrderApply(LoginRequiredMixin,ApplyManage,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request,'orders/order_apply.html',{"user":request.user})
    
    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('type'), request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res})            
    
    
# class OrderConfig(LoginRequiredMixin,View):
#     login_url = '/login/'
#     def get(self, request, *args, **kwagrs):
#         return render(request,'orders/order_config.html',{"user":request.user})  
    
    
class OrderLists(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        return render(request,'orders/order_list.html',{"user":request.user})    
    

class OrderInfo(LoginRequiredMixin,OrderStatus,View):
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        res = self.allowcator(request.GET.get('type'), request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})        
        return JsonResponse({'msg':"操作成功","code":200,'data':res})    
    
class OrderSQLHandle(LoginRequiredMixin,OrderSQLManage,View): 
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        if request.GET.get('id') and request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'), request)
            if isinstance(res, str):return HttpResponseRedirect("/404/")
            return render(request,'orders/order_sql.html',{"user":request.user})  
        else:       
            return HttpResponseRedirect("/404/")
        
    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('type'), request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res})      


class OrderFileUploadHandle(LoginRequiredMixin,OrderFileUploadManage,View): 
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        if request.GET.get('id') and request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'), request)
            if isinstance(res, str):return HttpResponseRedirect("/404/")
            return render(request,'orders/order_fileupload.html',{"user":request.user})  
        else:       
            return HttpResponseRedirect("/404/")
        
    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('type'), request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res}) 
    
class OrderFileDwonloadHandle(LoginRequiredMixin,OrderFileDownloadManage,View): 
    login_url = '/login/'
    def get(self, request, *args, **kwagrs):
        if request.GET.get('id') and request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'), request)
            if isinstance(res, str):return HttpResponseRedirect("/404/")
            return render(request,'orders/order_filedownload.html',{"user":request.user})  
        else:       
            return HttpResponseRedirect("/404/")
        
    def post(self, request, *args, **kwagrs):
        if request.POST.get('type') == "downloads":return self.downloads(request)
        res = self.allowcator(request.POST.get('type'), request)
        if isinstance(res, str):return JsonResponse({'msg':res,"code":500,'data':[]})
        return JsonResponse({'msg':"操作成功","code":200,'data':res})     
    
    def downloads(self,request): 
        try:
            sList,ANS = self.file_downloads(request)
        except Exception as ex:
            logger.error("下载文件失败:{ex}".format(ex))
            return JsonResponse({'msg':"工单不存在","code":500,'data':[]})
        dest = os.getcwd() + '/upload/file/download/' 
        module_args = "src={src} dest={dest}".format(src=request.POST.get('path'),dest=dest)
        ANS.run_model(host_list=sList,module_name='fetch',module_args=module_args)
        filesData = json.loads(ANS.get_model_result())
        filePath = filesData.get('success').get(request.POST.get('dest_host')).get('dest')
        if filePath:
            response = StreamingHttpResponse(base.file_iterator(filePath))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(file_name=os.path.basename(filePath))
            return response   
        return JsonResponse({'msg':"文件不存在","code":500,'data':[]})                  
        
        
        
        