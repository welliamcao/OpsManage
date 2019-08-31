#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from api import serializers
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from django_celery_beat.models  import CrontabSchedule,IntervalSchedule,PeriodicTask
from django_celery_results.models import TaskResult
from utils.base import method_decorator_adaptor

@api_view(['GET', 'POST' ])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_crontab_list(request,format=None):  
    if request.method == 'GET':     
        snippets = CrontabSchedule.objects.all()
        serializer = serializers.TaskCrontabSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.TaskCrontabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_crontab_detail(request, id,format=None):  
    try:
        snippet = CrontabSchedule.objects.get(id=id)
    except CrontabSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.TaskCrontabSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.TaskCrontabSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
@api_view(['GET', 'POST' ])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_intervals_list(request,format=None):  
    if request.method == 'GET':     
        snippets = IntervalSchedule.objects.all()
        serializer = serializers.TaskIntervalsSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.TaskIntervalsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_intervals_detail(request, id,format=None):  
    try:
        snippet = IntervalSchedule.objects.get(id=id)
    except IntervalSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.TaskIntervalsSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.TaskIntervalsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['GET', 'POST' ])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_task_list(request,format=None):  
    if request.method == 'GET':     
        snippets = PeriodicTask.objects.all()
        serializer = serializers.PeriodicTaskSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.PeriodicTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_task_detail(request, id,format=None):  
    try:
        snippet = PeriodicTask.objects.get(id=id)
    except PeriodicTask.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.PeriodicTaskSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.PeriodicTaskSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['GET', 'POST' ])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_task_result_list(request,format=None):  
    if request.method == 'GET':     
        result_list = TaskResult.objects.all()
        page = serializers.PageConfig()
        page_user_list = page.paginate_queryset(queryset=result_list, request=request, view=self)
        ser = serializers.TaskResultSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)       
    
    
class CeleryTaskResultList(APIView):
    
    @method_decorator_adaptor(permission_required, "djcelery.change_periodictask","/403/")        
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for ds in request.query_params.keys():
            if ds in ['offset']:continue
            query_params[ds] = request.query_params.get(ds)
        try:
            task_logs_list = TaskResult.objects.filter(**query_params)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=task_logs_list, request=request, view=self)
        ser = serializers.TaskResultSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data) 
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_task_result_detail(request, id,format=None):  
    try:
        snippet = TaskResult.objects.get(id=id)
    except PeriodicTask.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.TaskResultSerializer(snippet)
        return Response(serializer.data)
     
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)                   