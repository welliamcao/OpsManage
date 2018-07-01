#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api import serializers
from OpsManage.models import *
from rest_framework import status
from django.http import Http404
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from OpsManage.tasks.assets import recordAssets
from django.contrib.auth.decorators import permission_required
from OpsManage.utils.logger import logger
from django.http import JsonResponse



@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_project_assets',raise_exception=True)
def project_list(request,format=None):  
    if request.method == 'GET':     
        snippets = Project_Assets.objects.all()
        serializer = serializers.ProjectSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            recordAssets.delay(user=str(request.user),content="添加产品线名称：{project_name}".format(project_name=request.data.get("project_name")),type="project",id=serializer.data.get('id'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, id,format=None):  
    try:
        snippet = Project_Assets.objects.get(id=id)
    except Project_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.ProjectSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT' and request.user.has_perm('OpsManage.can_change_project_assets'):
        serializer = serializers.ProjectSerializer(snippet, data=request.data)
        old_name = snippet.project_name
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="修改产品线为：{old_name} -> {project_name}".format(old_name=old_name,project_name=request.data.get("project_name")),type="project",id=id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE' and request.user.has_perm('OpsManage.can_delete_rroject_assets'):
        if not request.user.has_perm('OpsManage.can_delete_rroject_Assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   

@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_service_assets',raise_exception=True)
def service_list(request,format=None):
    """
    List all order, or create a server assets order.
    """    
    if request.method == 'GET':     
        snippets = Service_Assets.objects.all()
        serializer = serializers.ServiceSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        del request.data['project_name']
        try:
            service = Service_Assets.objects.create(**request.data)
        except Exception, ex:
            return Response({"msg":str(ex)}, status=status.HTTP_400_BAD_REQUEST)      
        try:  
            snippet = Service_Assets.objects.get(id=service.id)
            serializer = serializers.ServiceSerializer(snippet)
            recordAssets.delay(user=str(request.user),content="添加业务类型名称：{service_name}".format(service_name=request.data.get("service_name")),type="service",id=serializer.data.get('id'))
        except Exception, ex:
            logger.error(msg="添加service失败: {ex}".format(ex=str(ex)))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        return Response(serializer.data)        
#         serializer = ServiceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
# #             recordAssets.delay(user=str(request.user),content="添加业务类型名称：{service_name}".format(service_name=request.data.get("service_name")),type="service",id=serializer.data.get('id'))  
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_change_service_assets',raise_exception=True)
def service_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Service_Assets.objects.get(id=id)
    except Service_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.ServiceSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.ServiceSerializer(snippet, data=request.data)
        old_name = snippet.service_name
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="修改业务类型为：{old_name} -> {service_name}".format(old_name=old_name,service_name=request.data.get("service_name")),type="service",id=id) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE' and request.user.has_perm('OpsManage.can_delete_assets'):
        if not request.user.has_perm('OpsManage.can_delete_service_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        recordAssets.delay(user=str(request.user),content="删除业务类型：{service_name}".format(service_name=snippet.service_name),type="service",id=id)
        return Response(status=status.HTTP_204_NO_CONTENT)   
  
@api_view(['GET', 'DELETE'])
@permission_required('OpsManage.read_log_assets',raise_exception=True)
def assetsLog_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Log_Assets.objects.get(id=id)
    except Log_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.AssetsLogsSerializer(snippet)
        return Response(serializer.data)
     
    elif request.method == 'DELETE' and request.user.has_perm('OpsManage.delete_log_assets'):
        if not request.user.has_perm('OpsManage.delete_log_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['GET', 'POST' ])
@permission_required('Opsmanage.add_group',raise_exception=True)
def group_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if not  request.user.has_perm('Opsmanage.read_group'):
        return Response(status=status.HTTP_403_FORBIDDEN)     
    if request.method == 'GET':      
        snippets = Group.objects.all()
        serializer = serializers.GroupSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        if not  request.user.has_perm('Opsmanage.change_group'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="添加用户组：{group_name}".format(group_name=request.data.get("name")),type="group",id=serializer.data.get('id'))  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('Opsmanage.change_group',raise_exception=True)
def group_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Group.objects.get(id=id)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.GroupSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.GroupSerializer(snippet, data=request.data)
        old_name = snippet.name
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="修改用户组名称：{old_name} -> {group_name}".format(old_name=old_name,group_name=request.data.get("name")),type="group",id=id) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('Opsmanage.delete_group'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        recordAssets.delay(user=str(request.user),content="删除用户组：{group_name}".format(group_name=snippet.name),type="group",id=id)        
        return Response(status=status.HTTP_204_NO_CONTENT)     

@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_zone_assets',raise_exception=True)
def zone_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
   
    if request.method == 'GET':      
        snippets = Zone_Assets.objects.all()
        serializer = serializers.ZoneSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':        
        serializer = serializers.ZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="添加机房资产：{zone_name}".format(zone_name=request.data.get("zone_name")),type="zone",id=serializer.data.get('id'))  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_change_zone_assets',raise_exception=True)
def zone_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Zone_Assets.objects.get(id=id)
    except Zone_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.ZoneSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        old_name = snippet.zone_name
        serializer = serializers.ZoneSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="修改机房资产：{old_name} -> {zone_name}".format(old_name=old_name,zone_name=request.data.get("zone_name")),type="zone",id=id) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_zone_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        recordAssets.delay(user=str(request.user),content="删除机房资产：{zone_name}".format(zone_name=snippet.zone_name),type="zone",id=id) 
        return Response(status=status.HTTP_204_NO_CONTENT)   
    
@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_line_assets',raise_exception=True)
def line_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Line_Assets.objects.all()
        serializer = serializers.LineSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.LineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="添加出口线路：{line_name}".format(line_name=request.data.get("line_name")),type="line",id=serializer.data.get('id'))  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_change_line_assets',raise_exception=True)
def line_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Line_Assets.objects.get(id=id)
    except Line_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.LineSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.LineSerializer(snippet, data=request.data)
        old_name = snippet.line_name
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="修改出口线路类型：{old_name} -> {line_name}".format(old_name=old_name,line_name=request.data.get("line_name")),type="line",id=id) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_line_assets'):            
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        recordAssets.delay(user=str(request.user),content="删除出口线路：{line_name}".format(line_name=snippet.line_name),type="line",id=id) 
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_raid_assets',raise_exception=True)
def raid_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Raid_Assets.objects.all()
        serializer = serializers.RaidSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.RaidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="添加Raid类型：{raid_name}".format(raid_name=request.data.get("raid_name")),type="raid",id=serializer.data.get('id'))  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_change_raid_assets',raise_exception=True)
def raid_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Raid_Assets.objects.get(id=id)
    except Raid_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.RaidSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        old_name = snippet.raid_name
        serializer = serializers.RaidSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="修改Raid类型：{old_name} -> {raid_name}".format(old_name=old_name,raid_name=request.data.get("raid_name")),type="raid",id=id) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_raid_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        recordAssets.delay(user=str(request.user),content="删除Raid类型：{raid_name}".format(raid_name=snippet.raid_name),type="raid",id=id) 
        return Response(status=status.HTTP_204_NO_CONTENT)  
                

@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_assets',raise_exception=True)
def asset_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Assets.objects.all()
        serializer = serializers.AssetsSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.AssetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="添加资产：{name}".format(name=request.data.get("name")),type="assets",id=serializer.data.get('id'))  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_change_assets',raise_exception=True)
def asset_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Assets.objects.get(id=id)
    except Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.AssetsSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.AssetsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="更新资产：{name}".format(name=snippet.name),type="assets",id=id) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.delete_asset_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        recordAssets.delay(user=str(request.user),content="删除资产：{name}".format(name=snippet.name),type="assets",id=id) 
        return Response(status=status.HTTP_204_NO_CONTENT) 


@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_server_assets',raise_exception=True)
def asset_server_list(request,format=None):
    """
    List all order, or create a server assets order.
    """

    if request.method == 'GET':      
        snippets = Server_Assets.objects.all()
        serializer = serializers.ServerSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        if(request.data.get('data')):
            data =  request.data.get('data')
        else:
            data = request.data
        serializer = serializers.ServerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="添加服务器资产：{ip}".format(ip=data.get("ip")),type="server",id=serializer.data.get('id'))  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_change_server_assets',raise_exception=True)
def asset_server_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Server_Assets.objects.get(id=id)
    except Server_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.ServerSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        '''如果更新字段包含assets则先更新总资产表'''
        if(request.data.get('data')):
            data =  request.data.get('data')
        else:
            data = request.data     
        if(data.get('assets')):
            assets_data = data.pop('assets')
            try:
                assets_snippet = Assets.objects.get(id=snippet.assets.id)
                assets = serializers.AssetsSerializer(assets_snippet,data=assets_data)
            except Assets.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if assets.is_valid():
                assets.save()
                recordAssets.delay(user=str(request.user),content="修改服务器资产：{ip}".format(ip=snippet.ip),type="server",id=id)
        serializer = serializers.ServerSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_server_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        try:
            assets_snippet = Assets.objects.get(id=snippet.assets.id)
            assets_snippet.delete()
            recordAssets.delay(user=str(request.user),content="删除服务器资产：{ip}".format(ip=snippet.ip),type="server",id=id)
        except Assets.DoesNotExist:
            pass       
        return Response(status=status.HTTP_204_NO_CONTENT)         
   
    
@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_add_net_assets',raise_exception=True)
def asset_net_list(request,format=None):
    """
    List all order, or create a new net assets.
    """
    if request.method == 'GET':      
        snippets = Network_Assets.objects.all()
        serializer = serializers.NetworkSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        if(request.data.get('data')):
            data =  request.data.get('data')
        else:
            data = request.data     
        serializer = serializers.NetworkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="添加网络设备资产：{ip}".format(ip=data.get("ip")),type="net",id=serializer.data.get('id')) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.can_change_net_assets',raise_exception=True)
def asset_net_detail(request, id,format=None):
    """
    Retrieve, update or delete a net assets instance.
    """
    try:
        snippet = Network_Assets.objects.get(id=id)
    except Network_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = serializers.NetworkSerializer(snippet)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        '''如果更新字段包含assets则先更新总资产表'''
        if(request.data.get('data')):
            data =  request.data.get('data')
        else:
            data = request.data         
        if(data.get('assets')):
            assets_data = data.pop('assets')
            try:
                assets_snippet = Assets.objects.get(id=snippet.assets.id)
                assets = serializers.AssetsSerializer(assets_snippet,data=assets_data)
            except Assets.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if assets.is_valid():
                assets.save()            
        serializer = serializers.NetworkSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            recordAssets.delay(user=str(request.user),content="更新网络设备资产：{ip}".format(ip=snippet.ip),type="net",id=id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.delete_net_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        try:
            assets_snippet = Assets.objects.get(id=snippet.assets.id)
            assets_snippet.delete()
            recordAssets.delay(user=str(request.user),content="删除网络设备资产：{ip}".format(ip=snippet.ip),type="net",id=id)
        except Assets.DoesNotExist:
            pass       
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

@api_view(['GET', 'POST'])
@permission_required('OpsManage.can_change_assets',raise_exception=True)
def asset_info(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        assets = Assets.objects.get(id=id)
    except Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'POST':
        dataList = []
        try:
            if assets.assets_type in ['server','vmser']:
                dataList.append({"name":'CPU型号',"value":assets.server_assets.cpu})
                dataList.append({"name":'CPU个数',"value":assets.server_assets.vcpu_number})
                dataList.append({"name":'硬盘容量',"value":str(int(assets.server_assets.disk_total)/1024)+'GB'})
                dataList.append({"name":'内存容量',"value":str(int(assets.server_assets.ram_total)/1024)+'GB'})
                dataList.append({"name":'操作系统',"value":assets.server_assets.system})
                dataList.append({"name":'内核版本',"value":assets.server_assets.kernel})
                dataList.append({"name":'主机名',"value":assets.server_assets.hostname})
            else:
                dataList.append({"name":'CPU型号',"value":assets.network_assets.cpu})
                dataList.append({"name":'内存容量',"value":assets.network_assets.stone})
                dataList.append({"name":'背板带宽',"value":assets.network_assets.bandwidth})
                dataList.append({"name":'端口总数',"value":assets.network_assets.port_number})
        except Exception ,ex:
            logger.warn(msg="获取资产信息失败: {ex}".format(ex=ex))
        return JsonResponse({"code":200,"msg":"success","data":dataList})   
            