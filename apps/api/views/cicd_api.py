#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import os
from api import serializers
from cicd.models import *
from dao.cicd import AppsCount
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from utils.logger import logger
from rest_framework.views import  APIView,Response


@api_view(['GET', 'POST' ])
@permission_required('apps.project_read_project_config',raise_exception=True)
def project_list(request,format=None):  
    if request.method == 'GET':     
        snippets = Project_Config.objects.all()
        serializer = serializers.AppsSerializer(snippets, many=True)
        return Response(serializer.data)     
    
    
@api_view(['DELETE'])
@permission_required('apps.project_delete_project_config',raise_exception=True)
def project_detail(request, id,format=None):
    try:
        snippet = Project_Config.objects.get(id=id)
    except Project_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
     
    if request.method == 'DELETE':
        if not request.user.has_perm('apps.project_read_project_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

@api_view(['DELETE'])
@permission_required('apps.project_delete_project_config',raise_exception=True)
def project_log_detail(request, id,format=None):
    try:
        snippet = Log_Project_Config.objects.get(id=id)
    except Log_Project_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)   
     
    if request.method == 'DELETE':
        if not request.user.has_perm('apps.project_delete_project_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            Log_Project_Record.objects.filter(task_id=snippet.task_id).delete()
        except Exception as ex:
            logger.error(msg="删除部署日志失败: {ex}".format(ex=str(ex)))
        if snippet.package and os.path.exists(snippet.package):os.remove(snippet.package)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class AppsLogPaginator(APIView):
    
    def get(self,request,*args,**kwargs):
        logs_list = Log_Project_Config.objects.filter(project=request.query_params.get('pid'))
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=logs_list, request=request, view=self)
        ser = serializers.AppsLogsSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)
    

class AppsLogRecord(APIView):
    
    def get(self,request,*args,**kwargs):
        snippets = Log_Project_Record.objects.filter(task_id=kwargs.get('id'))
        serializer = serializers.AppsLogsRecordSerializer(snippets, many=True)
        return Response(serializer.data)    
    

class AppsCounts(APIView,AppsCount):
    
    def get(self,request,*args,**kwargs):
        pid = request.query_params.get("id")
        if pid:
            try:
                return Response(self.get_apps_count(int(pid))) 
            except Exception as ex:
                return []
        return Response(self.get_all_apps_count()) 


@api_view(['GET', 'POST' ])
@permission_required('apps.project_add_project_config',raise_exception=True)
def apps_roles_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Project_Roles.objects.all()
        serializer = serializers.AppsRolesSerializer(snippets, many=True)
        return Response(serializer.data) 
        
    elif request.method == 'POST':
        serializer = serializers.AppsRolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('apps.project_change_project_config',raise_exception=True)
def apps_roles_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Project_Roles.objects.get(id=id)
    except Project_Roles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.AppsRolesSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.AppsRolesSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('apps.project_delete_project_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)          