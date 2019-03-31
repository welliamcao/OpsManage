#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import json
from rest_framework import viewsets,permissions
from api import serializers
from deploy.models import *
from asset.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from utils.logger import logger
from rest_framework.views import  APIView,Response
from utils.base import method_decorator_adaptor
from django.http import QueryDict

class DeployModelLogPaginator(APIView):
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_read_log_deploy_model","/403/")  
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for ds in request.query_params.keys():
            if ds in ['offset']:continue
            query_params[ds] = request.query_params.get(ds)
        if  query_params:       
            logs_list = Log_Deploy_Model.objects.filter(**query_params)
        else:
            logs_list = Log_Deploy_Model.objects.all()
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=logs_list, request=request, view=self)
        ser = serializers.DeployModelLogsSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_delete_log_deploy_model","/403/")  
    def delete(self,request,*args,**kwargs):  
        try:   
            model = Log_Deploy_Model.objects.get(id=QueryDict(request.body).get('id'))
            model.delete()
        except Exception as ex:
            logger.error(msg="删除Ansible model部署日志失败: {ex}".format(ex=str(ex)))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
        return Response(status=status.HTTP_204_NO_CONTENT)  

               

class DeployPlaybookLogPaginator(APIView):
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_read_log_deploy_playbook","/403/")  
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for ds in request.query_params.keys():
            if ds in ['offset']:continue
            query_params[ds] = request.query_params.get(ds)
        if  query_params:       
            logs_list = Log_Deploy_Playbook.objects.filter(**query_params)
        else:
            logs_list = Log_Deploy_Playbook.objects.all()
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=logs_list, request=request, view=self)
        ser = serializers.DeployPlaybookLogsSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)
    
    @method_decorator_adaptor(permission_required, "deploy.deploy_delete_log_deploy_playbook","/403/")  
    def delete(self,request,*args,**kwargs):  
        try:   
            model = Log_Deploy_Playbook.objects.get(id=QueryDict(request.body).get('id'))
            model.delete()
        except Exception as ex:
            logger.error(msg="删除Ansible model部署日志失败: {ex}".format(ex=str(ex)))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)          
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
# 
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('deploy.deploy_read_log_deploy_model',raise_exception=True)
def modelLogsdetail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """   
    if request.method == 'GET':
        snippets = Deploy_CallBack_Model_Result.objects.filter(logId=id)
        serializer = serializers.DeployModelLogsDetailSerializer(snippets, many=True)
        return Response(serializer.data) 
     
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('deploy.deploy_read_log_deploy_playbook',raise_exception=True)
def playbookLogsdetail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """  
    if request.method == 'GET':
        snippets = Deploy_CallBack_PlayBook_Result.objects.filter(logId=id)
        serializer = serializers.DeployPlaybookLogsDetailSerializer(snippets, many=True)
        return Response(serializer.data) 
        

@api_view(['GET'])
def inventory_list(request,format=None):
    if request.method == 'GET':
        snippets = Deploy_Inventory.objects.all()
        serializer = serializers.DeployInventorySerializer(snippets, many=True)
        return Response(serializer.data)        
    

@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        inventory = Deploy_Inventory.objects.get(id=id)
    except Deploy_Inventory.DoesNotExist:
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
                    source[ds.group_name]['vars'] = eval(ds.ext_vars)
                except Exception as ex:
                    source[ds.group_name]['vars'] = {}
                    logger.warn(msg="获取资产组变量失败: {ex}".format(ex=ex))
        return JsonResponse({"code":200,"msg":"success","data":source}) 
    elif request.method == 'DELETE':
        inventory.delete()
        return JsonResponse({"code":200,"msg":"删除成功","data":None}) 

@api_view(['GET', 'PUT','POST', 'DELETE'])
# @permission_required('deploy.deploy_read_deploy_inventory',raise_exception=True)
def deploy_inventory_groups(request, id,format=None):  

    try:
        inventory = Deploy_Inventory.objects.get(id=id)
    except Deploy_Inventory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET':        
        dataList = []
        for ds in inventory.inventory_group.all():
            dataList.append({"name":ds.group_name,"id":ds.id})
        return JsonResponse({"code":200,"msg":"success","data":dataList})  
       
    elif request.method == "POST":     
        if not  request.user.has_perm('deploy.deploy_add_deploy_inventory'):
            return Response(status=status.HTTP_403_FORBIDDEN)            
        try:
            ext_vars = json.dumps(eval(request.POST.get('ext_vars')))
        except Exception as ex:
            ext_vars = None
            logger.error(msg="添加资产组，转化外部变量失败: {ex}".format(ex=str(ex)))
        try:
            inventoryGroups = Deploy_Inventory_Groups.objects.create(inventory=inventory,
                                             group_name=request.POST.get('group_name'),
                                             ext_vars=ext_vars)
        except Exception as ex:
            logger.error(msg="添加资产组失败: {ex}".format(ex=str(ex)))
            return JsonResponse({'msg':"添加资产组失败: {ex}".format(ex=ex),"code":500,'data':[]})   
        try:
            for aid in request.POST.get('server_list').split(','):
                Deploy_Inventory_Groups_Server.objects.create(groups=inventoryGroups,server=aid)
        except Exception as ex:
            inventoryGroups.delete()
            logger.error(msg="添加资产组成员失败: {ex}".format(ex=str(ex)))
            return JsonResponse({'msg':"添加资产组成员失败: {ex}".format(ex=ex),"code":500,'data':[]})    
        return JsonResponse({'msg':"添加成功","code":200,'data':[]}) 


@api_view(['GET', 'PUT','POST', 'DELETE'])
def deploy_inventory_groups_query(request, id,format=None):  
    try:
        snippet = Deploy_Inventory_Groups.objects.get(id=id)
    except Deploy_Inventory_Groups.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  
    
    if request.method == 'GET':
        serializer = serializers.DeployInventoryGroupsSerializer(snippet)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
# @permission_required('deploy.deploy_add_deploy_inventory',raise_exception=True)
def deploy_host_vars(request, id,format=None):
    try:
        assets = Assets.objects.get(id=id)
    except Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET': 
        host_vars = {}   
        if assets.host_vars:
            try:
                host_vars = eval(assets.host_vars)
            except Exception as ex:
                return JsonResponse({'msg':"获取主机变量失败: {ex}".format(ex=ex),"code":500,'data':{}}) 
        return JsonResponse({'msg':"查询成功","code":200,'data':host_vars})  
    elif  request.method == 'POST': 
        host_vars = request.data.get('host_vars',None)
        if host_vars:
            try:
                host_vars = eval(request.data.get('host_vars'))
            except Exception as ex:
                return JsonResponse({'msg':"更新主机变量失败: {ex}".format(ex=ex),"code":500,'data':{}}) 
        assets.host_vars = host_vars
        assets.save()
        return JsonResponse({'msg':"更新成功","code":200,'data':host_vars})          