#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework.views import APIView
from api import serializers
from asset.models import *
from rest_framework import status
from django.http import Http404
# from django.contrib.auth.models import Group
from account.models import User,Role
from dao.assets import ASSETS_COUNT_RBT,AssetsBusiness
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from utils.logger import logger
from django.http import JsonResponse
from dao.base import DataHandle
from mptt.templatetags.mptt_tags import cache_tree_children
 

@api_view(['GET', 'POST' ])
def zone_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':    
        if not request.user.has_perm('asset.assets_read_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)          
        snippets = Zone_Assets.objects.all()
        serializer = serializers.ZoneSerializer(snippets, many=True)
        return Response(serializer.data)     
    
    elif request.method == 'POST': 
        if not request.user.has_perm('asset.assets_read_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)                
        serializer = serializers.ZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def zone_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Zone_Assets.objects.get(id=id)
    except Zone_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.ZoneSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.ZoneSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
    

@api_view(['GET', 'POST' ])
def idc_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
   
    if request.method == 'GET':  
        if not request.user.has_perm('asset.assets_read_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)             
        snippets = Idc_Assets.objects.all()
        serializer = serializers.IdcSerializer(snippets, many=True)
        return Response(serializer.data) 
        
    elif request.method == 'POST':  
        if not request.user.has_perm('asset.assets_add_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)  
                
        try:
            zone = Zone_Assets.objects.get(id=request.data.get('zone'))
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST) 
        
        serializer = serializers.IdcSerializer(data=request.data,context={"zone":zone})
        
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['GET', 'PUT', 'DELETE'])
def idc_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Idc_Assets.objects.get(id=id)
    except Idc_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.IdcSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)        
        serializer = serializers.IdcSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
 
@api_view(['GET', 'POST' ])
def idle_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
   
    if request.method == 'GET':    
        if not request.user.has_perm('asset.assets_read_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)           
        snippets = Idle_Assets.objects.all()
        serializer = serializers.IdleAssetsSerializer(snippets, many=True)
        return Response(serializer.data) 
        
    elif request.method == 'POST':  
        if not request.user.has_perm('asset.assets_add_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        try:
            idc = Idc_Assets.objects.get(id=request.data.get('idc'))
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)         
        
        if not request.user.has_perm('asset.assets_add_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)  

        data = request.data.copy()
        data.update({"idle_user":request.user.id})
        
        serializer = serializers.IdleAssetsSerializer(data=data,context={"idc":idc,"idle_user":request.user.id})
        
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def idle_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Idle_Assets.objects.get(id=id)
    except Zone_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.IdleAssetsSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)   
        
        data = request.data.copy()
        data.update({"idle_user":request.user.id})        
         
        serializer = serializers.IdleAssetsSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
    
@api_view(['GET', 'POST' ])
def raid_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':     
        if not request.user.has_perm('asset.assets_add_raid'):
            return Response(status=status.HTTP_403_FORBIDDEN)          
        snippets = Raid_Assets.objects.all()
        serializer = serializers.RaidSerializer(snippets, many=True)
        return Response(serializer.data)   
      
    elif request.method == 'POST':
        if not request.user.has_perm('asset.assets_add_raid'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.RaidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #recordAssets.delay(user=str(request.user),content="添加Raid类型：{raid_name}".format(raid_name=request.data.get("raid_name")),type="raid",id=serializer.data.get('id'))  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def raid_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Raid_Assets.objects.get(id=id)
    except Raid_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_raid'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.RaidSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_raid'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.RaidSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_raid'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
                   

class AssetList(APIView,DataHandle):
    
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for ds in request.query_params.keys():  
            if ds == 'assets_type' and request.query_params.get(ds) == 'ser':         
                query_params["assets_type__in"] = ["vmser","server"]
                continue 
            query_params[ds] = request.query_params.get(ds)     
        if request.user.is_superuser:             
            snippets = Assets.objects.filter(**query_params)
        else:
            snippets = [ ds.assets for ds in User_Server.objects.filter(user=request.user,assets__in=[ ds.id  for ds in Assets.objects.filter(**query_params) ]) ]
        dataList = []
        for assets in snippets:      
            dataList.append(assets.to_json())
        return Response(dataList) 
    
    def post(self,request,*args,**kwargs):    
        if not request.user.has_perm('asset.assets_add_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)            
        serializer = serializers.AssetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['GET', 'PUT', 'DELETE'])
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
        if not request.user.has_perm('asset.assets_change_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)        
        serializer = serializers.AssetsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.delete_asset_assets'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


@api_view(['GET', 'POST' ])
def asset_server_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_server'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        snippets = Server_Assets.objects.all()
        serializer = serializers.ServerSerializer(snippets, many=True)
        return Response(serializer.data) 
        
    elif request.method == 'POST':
        if not request.user.has_perm('asset.assets_add_server'):
            return Response(status=status.HTTP_403_FORBIDDEN)        
        if(request.data.get('data')):
            data =  request.data.get('data')
        else:
            data = request.data
        serializer = serializers.ServerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET', 'PUT', 'DELETE'])
def asset_server_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Server_Assets.objects.get(id=id)
    except Server_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_server'):
            return Response(status=status.HTTP_403_FORBIDDEN)          
        serializer = serializers.ServerSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_server'):
            return Response(status=status.HTTP_403_FORBIDDEN)          
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
        serializer = serializers.ServerSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_server'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        try:
            assets_snippet = Assets.objects.get(id=snippet.assets.id)
            assets_snippet.delete()
        except Assets.DoesNotExist:
            pass       
        return Response(status=status.HTTP_204_NO_CONTENT)         
   
    
@api_view(['GET', 'POST' ])
def asset_net_list(request,format=None):
    """
    List all order, or create a new net assets.
    """
    if request.method == 'GET':    
        if not request.user.has_perm('asset.assets_read_network'):
            return Response(status=status.HTTP_403_FORBIDDEN)           
        snippets = Network_Assets.objects.all()
        serializer = serializers.NetworkSerializer(snippets, many=True)
        return Response(serializer.data)     
    
    elif request.method == 'POST':
        if not request.user.has_perm('asset.assets_add_network'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        if(request.data.get('data')):
            data =  request.data.get('data')
        else:
            data = request.data     
        serializer = serializers.NetworkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
@api_view(['GET', 'PUT', 'DELETE'])
def asset_net_detail(request, id,format=None):
    """
    Retrieve, update or delete a net assets instance.
    """
    try:
        snippet = Network_Assets.objects.get(id=id)
    except Network_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_network'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.NetworkSerializer(snippet)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_network'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_network'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        try:
            assets_snippet = Assets.objects.get(id=snippet.assets.id)
            assets_snippet.delete()
        except Assets.DoesNotExist:
            pass       
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

@api_view(['GET', 'POST'])
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
                dataList.append({"name":'CPU型号',"value":assets.server_assets.cpu if assets.server_assets.cpu else ''})
                dataList.append({"name":'CPU个数',"value":assets.server_assets.vcpu_number if assets.server_assets.vcpu_number else '' })
                dataList.append({"name":'硬盘容量',"value":str(assets.server_assets.disk_total)+'GB' if assets.server_assets.disk_total else ''})
                dataList.append({"name":'内存容量',"value":str(assets.server_assets.ram_total)+'GB' if assets.server_assets.ram_total else ''})
                dataList.append({"name":'操作系统',"value":assets.server_assets.system if assets.server_assets.system else ''})
                dataList.append({"name":'内核版本',"value":assets.server_assets.kernel if assets.server_assets.kernel else ''})
                dataList.append({"name":'主机名',"value":assets.server_assets.hostname if assets.server_assets.hostname else ''})
                dataList.append({"name":'资产备注',"value":assets.mark if assets.mark else ''})
            else:
                dataList.append({"name":'CPU型号',"value":assets.network_assets.cpu if assets.network_assets.cpu else ''})
                dataList.append({"name":'内存容量',"value":assets.network_assets.stone if assets.network_assets.stone else ''})
                dataList.append({"name":'背板带宽',"value":assets.network_assets.bandwidth if assets.network_assets.bandwidth else ''})
                dataList.append({"name":'端口总数',"value":assets.network_assets.port_number if assets.network_assets.port_number else ''})
                dataList.append({"name":'资产备注',"value":assets.mark if assets.mark else ''})
        except Exception as ex:
            logger.warn(msg="获取资产信息失败: {ex}".format(ex=ex))
        ntkList = []
        for ds in NetworkCard_Assets.objects.filter(assets=assets):
            ntkList.append({"name":ds.device,'mac':ds.macaddress,
                            "ipv4":ds.ip,"speed":ds.module,
                            "mtu":ds.mtu,"status":ds.active})
        return JsonResponse({"code":200,"msg":"success","data":{"astList":dataList,"nktList":ntkList}})   
    
@api_view(['GET', 'POST'])
def asset_count(request,format=None): 
    return JsonResponse({"code":200,"msg":"success","data":{"groupCount":ASSETS_COUNT_RBT.groupAssets(),
                                                            "statusCount":ASSETS_COUNT_RBT.statusAssets(),
                                                            "typeCount":ASSETS_COUNT_RBT.typeAssets(),
                                                            "idcCount":ASSETS_COUNT_RBT.idcAssets(),
                                                            "appsCount":ASSETS_COUNT_RBT.appsAssets(),
                                                            "dbCount":ASSETS_COUNT_RBT.databasesAssets(),
                                                            "tagsCount":ASSETS_COUNT_RBT.tagsAssets(),
                                                            "allCount":ASSETS_COUNT_RBT.allCount()}}) 
    
    
@api_view(['GET', 'POST' ])
def cabinet_list(request,format=None):
    """
    List all order, or create a server assets order.
    """    
    if request.method == 'GET':     
        snippets = Cabinet_Assets.objects.all()
        serializer = serializers.CabinetSerializer(snippets, many=True)
        return Response(serializer.data)     
    
    elif request.method == 'POST':
        if not request.user.has_perm('asset.assets_add_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)
                
        try:
            idc = Idc_Assets.objects.get(id=request.data.get('idc'))
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)  
  
        serializer = serializers.CabinetSerializer(data=request.data,context={"idc":idc})
        
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['GET', 'PUT', 'DELETE'])
def cabinet_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Cabinet_Assets.objects.get(id=id)
    except Cabinet_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.CabinetSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)               
        serializer = serializers.CabinetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_zone'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     
    
    
@api_view(['GET', 'POST' ])
def line_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':   
        if not request.user.has_perm('asset.assets_read_line'):
            return Response(status=status.HTTP_403_FORBIDDEN) 
                   
        snippets = Line_Assets.objects.all()
        serializer = serializers.LineSerializer(snippets, many=True)
        return Response(serializer.data)    
     
    elif request.method == 'POST':
        if not request.user.has_perm('asset.assets_add_line'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.LineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['GET', 'PUT', 'DELETE'])
def line_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Line_Assets.objects.get(id=id)
    except Line_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_line'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.LineSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':

        if not request.user.has_perm('asset.assets_change_line'):            
            return Response(status=status.HTTP_403_FORBIDDEN)        
        
        serializer = serializers.LineSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_line'):            
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['GET', 'POST' ])
def tags_list(request,format=None):
    """
    List all order, or create a server assets order.
    """   
    if request.method == 'GET':      
        snippets = Tags_Assets.objects.all()
        serializer = serializers.TagsSerializer(snippets, many=True)
        return Response(serializer.data)    
     
    elif request.method == 'POST':
        if not  request.user.has_perm('asset.assets_add_tags'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.TagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def tags_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Tags_Assets.objects.get(id=id)
    except Tags_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        if not request.user.has_perm('asset.assets_read_tags'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.TagsSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_tags'):  
            return Response(status=status.HTTP_403_FORBIDDEN)        
        serializer = serializers.TagsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_tags'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()      
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
@api_view(['POST' ])
@permission_required('asset.assets_add_tags',raise_exception=True)
def tags_assets(request, id,format=None):
    """
    List all order, or create a server assets order.
    """  
    try:
        snippet = Tags_Assets.objects.get(id=id)
        serializer = serializers.TagsSerializer(snippet)
    except Tags_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
         
    if request.method == 'POST':
        tagsAssets = [ s.aid.id for s in Tags_Server_Assets.objects.filter(tid=id)]
        aList = [ int(a) for a in request.data.get('ids',[]) ]
        for a in aList:
            if a not in tagsAssets:
                assets = Assets.objects.get(id=a)
                try:
                    Tags_Server_Assets.objects.create(aid=assets,tid=snippet)
                except Exception as ex:
                    logger.error(msg="添加资产标签分类失败: {ex}".format(ex=str(ex)))
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        delList = list(set(tagsAssets).difference(set(aList)))
        for ds in delList:
            assets = Assets.objects.get(id=ds)
            Tags_Server_Assets.objects.filter(aid=assets,tid=snippet).delete()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)   

@api_view(['POST' ])
@permission_required('asset.assets_change_assets',raise_exception=True)
def assets_tags(request, id,format=None):
    """
    List all order, or create a server assets order.
    """  
    try:
        snippet = Assets.objects.get(id=id)
        serializer = serializers.AssetsSerializer(snippet)
    except Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
         
    if request.method == 'POST':
        tagsAssets = [ s.tid.id for s in Tags_Server_Assets.objects.filter(aid=id)]
        tList = [ int(a) for a in request.data.get('ids',[]) ]
        for a in tList:
            if a not in tagsAssets:
                tags = Tags_Assets.objects.get(id=a)
                try:
                    Tags_Server_Assets.objects.create(aid=snippet,tid=tags)
                except Exception as ex:
                    logger.error(msg="修改资产标签分类失败: {ex}".format(ex=str(ex)))
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        delList = list(set(tagsAssets).difference(set(tList)))
        for ds in delList:
            tags = Tags_Assets.objects.get(id=ds)
            Tags_Server_Assets.objects.filter(aid=snippet,tid=tags).delete()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    


#业务线
@api_view(['GET', 'POST' ])
def business_list(request,format=None):
    """
    List all order, or create a server assets order.
    """    
    if request.method == 'GET':     
        dataList = []
        for ds in Business_Tree_Assets.objects.all():
            if ds.is_leaf_node():
                data = ds.to_json()
                data["paths"] = ds.business_env() + '/' + data["paths"]
                dataList.append(data)               
        return Response(dataList)     
       
 
#业务环境
@api_view(['GET', 'POST' ])
def env_list(request,format=None):
    """
    Env all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Business_Env_Assets.objects.all()
        serializer = serializers.BusinessEnvSerializer(snippets, many=True)
        return Response(serializer.data)  
       
    elif request.method == 'POST':
        
        if not request.user.has_perm('asset.assets_add_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)  
              
        serializer = serializers.BusinessEnvSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET', 'PUT', 'DELETE'])
def env_detail(request, id,format=None):
    try:
        snippet = Business_Env_Assets.objects.get(id=id)
    except Business_Env_Assets.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.BusinessEnvSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        if not request.user.has_perm('asset.assets_change_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)        
        serializer = serializers.BusinessEnvSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('asset.assets_delete_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()       
        return Response(status=status.HTTP_204_NO_CONTENT) 





class BUSINESS_TREE_LIST(APIView):
    '''(right - left - 1) // 2 = 节点下面有多少个子节点'''
    
    def recursive_node_to_dict(self,node):
        json_format = node.to_json()
        children = [self.recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            json_format['children'] = children
        else:
            json_format['icon'] = 'fa fa-minus-square-o' 
#         json_format["count"] = len(children)         
        return json_format
        
    def get(self,request,*args,**kwargs): 
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
        
        if 'env' in list(query_params.keys()) and len(query_params.keys()) == 1:            
            try:
                first_node = Business_Tree_Assets.objects.filter(env=query_params.get('env'),parent__isnull=True)
                tree_list = Business_Tree_Assets.objects.filter(tree_id__in=[ x.tree_id for x in first_node])
            except Exception as ex:
                return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)                        
        else:    
            try:
                tree_list = Business_Tree_Assets.objects.filter(**query_params)
#                 tree_list = Business_Tree_Assets.objects.filter(id__in=[1, 4, 24, 25,26])
            except Exception as ex:
                return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)

        root_nodes = cache_tree_children(tree_list)
        dicts = []
        for n in root_nodes:
            dicts.append(self.recursive_node_to_dict(n))       
        return Response(dicts)                

#业务节点列表
class NODE_LIST(APIView,AssetsBusiness):
    
    def get(self,request,*args,**kwargs): 
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
 
        if not query_params:
            snippets = Business_Tree_Assets.objects.filter(parent__isnull=True)
        else:
            if len(list(set(["tree_id","lft","rght"]).intersection(set(query_params.keys())))) == 3: #查询节点下面的所有子节点   
                snippets = self.get_nodes_all_children(tree_id=query_params.get("tree_id"), lft=query_params.get("lft"), rght=query_params.get("rght"))
            else:
                snippets = Business_Tree_Assets.objects.filter(**query_params)                
        serializer = serializers.BusinessTreeSerializer(snippets, many=True)
        return Response(serializer.data)    
    
    def post(self,request,*args,**kwargs):
         
        if not request.user.has_perm('asset.assets_add_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)  
        try:
            business = Business_Tree_Assets.objects.get(id=request.data["parent"])
        except:
            business = None
            
        if (business and self.get_assets(business).count() == 0) or business is None:  
                
            serializer = serializers.BusinessTreeSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
        else:
            return Response("请先清除当前节点下面绑定的资产", status=status.HTTP_400_BAD_REQUEST)

class NODE_DETAIL(APIView,AssetsBusiness):
    
    def get_object(self, pk):
        try:
            return Business_Tree_Assets.objects.get(id=pk)
        except Business_Tree_Assets.DoesNotExist:
            raise Http404  
            
    def get(self, request, pk, *args,**kwargs): 
        snippet = self.get_object(pk)
        
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)

        if not query_params:
            
            serializer = serializers.BusinessTreeSerializer(snippet)
            
            return Response(serializer.data)        
        
        elif query_params.get("type") == "children":
            
            serializer = serializers.BusinessTreeSerializer(snippet.get_children(), many=True)
            
            return Response(serializer.data) 
                   
        else:    
            snippets = Business_Tree_Assets.objects.filter(**query_params)    
        
        serializer = serializers.BusinessTreeSerializer(snippets, many=True)
            
        return Response(serializer.data) 

    
    def put(self, request, pk, *args,**kwargs):
        
        snippet = self.get_object(pk)
        
        if not request.user.has_perm('asset.assets_change_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)     
           
        serializer = serializers.BusinessTreeSerializer(snippet, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args,**kwargs): 
        
        snippet = self.get_object(pk)
          
        if not request.user.has_perm('asset.assets_delete_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        bRbt = AssetsBusiness()
        
        if snippet.is_leaf_node() and bRbt.get_assets(snippet).count() > 0:
            return Response("请先清除当前节点下面绑定的资产", status=status.HTTP_400_BAD_REQUEST)
            
        for children in snippet.get_children():
            if bRbt.get_assets(children).count() > 0:
                return Response("请先清除当前节点或者子节点下面绑定的资产", status=status.HTTP_400_BAD_REQUEST)
        
     
        snippet.delete()       
        return Response(status=status.HTTP_204_NO_CONTENT)          
                          
#业务节点
class NODES_ASSERS_DETAIL(APIView,AssetsBusiness):
    
    def get_object(self, pk):
        try:
            return Business_Tree_Assets.objects.get(id=pk)
        except Business_Tree_Assets.DoesNotExist:
            raise Http404      
    
    def get(self, request, pk, *args,**kwargs): 
        snippet = self.get_object(pk)
        
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
            
        if not query_params:
            return Response(self.get_node_json_assets(snippet))                    
        
        elif query_params.get("type") == "unallocated":
            
            return Response(self.get_node_unallocated_json_assets(snippet))    
        
        else: 
            
            return Response([]) 
        
        
    def post(self,request, pk, *args,**kwargs):
         
        if not request.user.has_perm('asset.assets_add_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)  
        
        snippet = self.get_object(pk)
                    
        asset_list = Assets.objects.filter(id__in=request.data.getlist('assets'))
        
        try:
            snippet.assets_set.add(*asset_list)
        except Exception as ex:
            msg="资产分配资产失败: {ex}".format(ex=str(ex))
            logger.error(msg)
            return Response(msg,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = serializers.BusinessTreeSerializer(snippet)
        return Response(serializer.data)
    
    def delete(self, request, pk, *args,**kwargs): 
        
        snippet = self.get_object(pk)
          
        if not request.user.has_perm('asset.assets_delete_business'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
   
        asset_list = Assets.objects.filter(id__in=request.data.getlist('assets'))
        
        try:
            snippet.assets_set.remove(*asset_list)
        except Exception as ex:
            msg="资产取消资产分配失败: {ex}".format(ex=str(ex))
            logger.error(msg)
            return Response(msg,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
        return Response(status=status.HTTP_204_NO_CONTENT)    