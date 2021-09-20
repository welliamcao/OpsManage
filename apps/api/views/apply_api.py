#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import os
from api import serializers
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.mixins import LoginRequiredMixin
from dao.apply import ApplyTaskManage
from django.views.generic import View
from apply.models import APPLY_CENTER_CONFIG,ApplyTasksModel
from django.contrib.auth.decorators import permission_required
from utils.base import method_decorator_adaptor
from api import serializers

class ApplyCenterConfig(LoginRequiredMixin, APIView):
    login_url = '/login/'
    
    def get(self, request, *args, **kwagrs):
        query_params = dict()
        for ds in request.query_params.keys():
            if ds in ['offset']:continue
            query_params[ds] = request.query_params.get(ds)
        if  query_params:       
            apply_list = APPLY_CENTER_CONFIG.objects.filter(**query_params)
        else:
            apply_list = APPLY_CENTER_CONFIG.objects.all()        
    
        page = serializers.PageConfig()  # 注册分页
        apply_config_list = page.paginate_queryset(queryset=apply_list, request=request, view=self)
        ser = serializers.ApplyCenterConfigSerializer(instance=apply_config_list, many=True)
        return page.get_paginated_response(ser.data) 
    
    @method_decorator_adaptor(permission_required, "apply.apply_add_config","/403/")
    def post(self, request, *args, **kwagrs): 
        if not os.path.exists(request.data.get('apply_playbook')):
            return Response("{apply_playbook} is not exists".format(apply_playbook=request.data.get('apply_playbook')) , status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializers.ApplyCenterConfigSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    
class ApplyConfigDetail(LoginRequiredMixin, ApplyTaskManage, APIView):
    
    def get_object(self, pk):
        try:
            return APPLY_CENTER_CONFIG.objects.get(id=pk)
        except APPLY_CENTER_CONFIG.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "apply.apply_read_config","/403/")     
    def get(self,request,pk,format=None):
        snippet = self.get_object(pk)
        serializer = serializers.ApplyCenterConfigSerializer(snippet)
        return Response(serializer.data)
    
    @method_decorator_adaptor(permission_required, "apply.apply_change_config","/403/")
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.ApplyCenterConfigSerializer(snippet, data=request.data)     
        if serializer.is_valid():
            serializer.save()                    
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    @method_decorator_adaptor(permission_required, "apply.apply_delete_config","/403/")
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)   
        for task in ApplyTasksModel.objects.filter(apply_id=snippet.id):
            self.stop_task(task)
            task.delete()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
class ApplyTasks(LoginRequiredMixin, ApplyTaskManage, APIView):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "apply.apply_read_config","/403/")
    def get(self, request, *args, **kwagrs):
        query_params = dict()
        for ds in request.query_params.keys():
            if ds in ['offset']:continue
            query_params[ds] = request.query_params.get(ds)
        if  query_params:       
            tasks_list = ApplyTasksModel.objects.filter(**query_params)
        else:
            tasks_list = ApplyTasksModel.objects.all()        
        page = serializers.PageConfig()  # 注册分页
        apply_tasks_list = page.paginate_queryset(queryset=tasks_list, request=request, view=self)
        ser = serializers.ApplyTasksSerializer(instance=apply_tasks_list, many=True)
        return page.get_paginated_response(ser.data) 
    
    @method_decorator_adaptor(permission_required, "apply.apply_add_config","/403/")
    def post(self, request, *args, **kwagrs): 
        snippet = self.create_task(request)
        if isinstance(snippet, str):
            return Response({"detail":snippet}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ApplyTasksSerializer(snippet)
        return Response(serializer.data)      
    

class ApplyTasksCount(LoginRequiredMixin, ApplyTaskManage, APIView):
    login_url = '/login/'
    
    @method_decorator_adaptor(permission_required, "apply.apply_read_config","/403/")
    def get(self, request, *args, **kwagrs):
        return Response(self.get_task_count())      
    
class ApplyTasksDetail(LoginRequiredMixin, ApplyTaskManage, APIView):
    
    def get_object(self, pk):
        try:
            return ApplyTasksModel.objects.get(id=pk)
        except ApplyTasksModel.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "apply.apply_read_config","/403/")     
    def get(self,request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.ApplyTasksSerializer(snippet)
        return Response(serializer.data)  
    
    @method_decorator_adaptor(permission_required, "apply.apply_change_config","/403/")
    def put(self, request, pk, *args, **kwagrs): 
        snippet = self.get_object(pk)
        result = self.stop_task(snippet)
        if isinstance(result, str):
            return Response({"detail":result}, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ApplyTasksSerializer(snippet)
        return Response(serializer.data)       

    @method_decorator_adaptor(permission_required, "apply.apply_delete_config","/403/")
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)   
        if snippet.status in ["runnig","ready"]:
            return Response({"detail":"please stop the task first"}, status=status.HTTP_400_BAD_REQUEST)
        else:     
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 

class ApplyTasksLogDetail(LoginRequiredMixin, ApplyTaskManage, APIView):
    
    def get_object(self, pk):
        try:
            return ApplyTasksModel.objects.get(id=pk)
        except ApplyTasksModel.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "apply.apply_read_config","/403/")     
    def get(self,request,pk,format=None):
        snippet = self.get_task_detail(pk)
        return Response(snippet)   
    
    
class ApplyTasksSyncTagsDetail(ApplyTaskManage, APIView):
    
    def get_object(self, pk):
        try:
            return ApplyTasksModel.objects.get(id=pk)
        except ApplyTasksModel.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "apply.apply_change_config","/403/")     
    def post(self,request,pk,format=None):
        task = self.get_object(pk)
        snippet = self.sync_task_to_tags_assets(task)
        if isinstance(snippet, str):
            return Response({"detail":snippet}, status=status.HTTP_400_BAD_REQUEST)
        return Response(task.to_json(), status=status.HTTP_201_CREATED)            