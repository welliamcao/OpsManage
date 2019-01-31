#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import ast
from rest_framework import viewsets,permissions
from api import serializers
from OpsManage.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from OpsManage.utils.logger import logger

@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_read_ansible_playbook',raise_exception=True)
def playbook_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Ansible_Playbook.objects.all()
        serializer = serializers.AnbiblePlaybookSerializer(snippets, many=True)
        return Response(serializer.data)   
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_delete_ansible_playbook',raise_exception=True)
def playbook_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Ansible_Playbook.objects.get(id=id)
    except Ansible_Playbook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.AnbiblePlaybookSerializer(snippet)
        return Response(serializer.data)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_ansible_playbook'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_delete_log_ansible_model',raise_exception=True)
def modelLogsdetail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Log_Ansible_Model.objects.get(id=id)
    except Log_Ansible_Model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.AnsibleModelLogsSerializer(snippet)
        return Response(serializer.data)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_log_ansible_model'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_delete_log_ansible_playbook',raise_exception=True)
def playbookLogsdetail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Log_Ansible_Playbook.objects.get(id=id)
    except Log_Ansible_Playbook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.AnsiblePlaybookLogsSerializer(snippet)
        return Response(serializer.data)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_log_ansible_playbook'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_read_ansible_inventory',raise_exception=True)
def inventory_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        inventory = Ansible_Inventory.objects.get(id=id)
    except Ansible_Inventory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        source = {}
        for ds in inventory.inventory_group.all():
            source[ds.group_name] = {}
            hosts = []
            for ser in ds.inventory_group_server.all():
                assets =  Assets.objects.get(id=ser.server)
                if hasattr(assets,'server_assets'):hosts.append( assets.server_assets.ip)
                elif hasattr(assets,'network_assets'):hosts.append(assets.network_assets.ip)
            source[ds.group_name]['hosts'] = hosts
            if ds.ext_vars:
                try:
                    source[ds.group_name]['vars'] = ast.literal_eval(ds.ext_vars)
                except Exception ,ex:
                    source[ds.group_name]['vars'] = {}
                    logger.warn(msg="获取资产组变量失败: {ex}".format(ex=ex))
        return JsonResponse({"code":200,"msg":"success","data":source}) 
    elif request.method == 'DELETE':
        inventory.delete()
        return JsonResponse({"code":200,"msg":"删除成功","data":None}) 
    
@api_view(['GET', 'POST'])
@permission_required('OpsManage.can_read_ansible_inventory',raise_exception=True)
def ansible_host_vars(request, id,format=None):
    try:
        assets = Assets.objects.get(id=id)
    except Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET': 
        host_vars = {}   
        if assets.host_vars:
            try:
                host_vars = ast.literal_eval(assets.host_vars)
            except Exception,ex:
                return JsonResponse({'msg':"获取主机变量失败: {ex}".format(ex=ex),"code":500,'data':{}}) 
        return JsonResponse({'msg':"查询成功","code":200,'data':host_vars})  
    elif  request.method == 'POST': 
        host_vars = request.data.get('host_vars',None)
        if host_vars:
            try:
                host_vars = ast.literal_eval(request.data.get('host_vars'))
            except Exception,ex:
                return JsonResponse({'msg':"更新主机变量失败: {ex}".format(ex=ex),"code":500,'data':{}}) 
        assets.host_vars = host_vars
        assets.save()
        return JsonResponse({'msg':"更新成功","code":200,'data':host_vars})          