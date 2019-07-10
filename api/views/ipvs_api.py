#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from api import serializers
from apply.models import *
from apply.service.ipvs import IPVSRunner 
from dao.ipvs import ASSETSIPVS,IVPSManage
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from utils.base import method_decorator_adaptor



@api_view(['GET'])
@permission_required('apply.ipvs_read_ipvs_config',raise_exception=True)
def ipvs_tree(request,format=None):
    if request.method == 'GET':
        return Response(ASSETSIPVS.tree())

@api_view(['GET'])
@permission_required('apply.ipvs_read_ipvs_config',raise_exception=True)
def ipvs_assets(request,format=None):
    if request.method == 'GET':
        return Response(ASSETSIPVS.assets())    

@api_view(['GET', 'PUT' ])
@permission_required('apply.ipvs_read_ipvs_config',raise_exception=True)
def ipvs_tree_service(request,id,format=None):
    if request.method == 'GET':
        return Response(ASSETSIPVS.service(service=id)) 

class IPVSLIST(APIView,IVPSManage):
     
    @method_decorator_adaptor(permission_required, "apply.ipvs_read_ipvs_config","/403/")     
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
        try:
            ipvs_list = IPVS_CONFIG.objects.filter(**query_params)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=ipvs_list, request=request, view=self)
        ser = serializers.IPVSSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data) 
 
    @method_decorator_adaptor(permission_required, "apply.ipvs_add_ipvs_config","/403/")     
    def post(self,request,*args,**kwargs):
        serializer = serializers.IPVSSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()              
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class IPVSLIST_DETAIL(APIView,IVPSManage):
    
    def get_object(self, pk):
        try:
            return IPVS_CONFIG.objects.get(id=pk)
        except IPVS_CONFIG.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_read_ipvs_config","/403/")     
    def get(self,request,pk,format=None):
        snippet = self.get_object(pk)
        serializer = serializers.IPVSSerializer(snippet)
        return Response(serializer.data)
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_change_ipvs_config","/403/")
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.IPVSSerializer(snippet, data=request.data)
        if serializer.is_valid():            
            serializer.save()
            IPVS = IPVSRunner(vip=self.get_ipvs_vip(id=snippet.id))
            result = IPVS.run('modf_vip',request.data)
            if result:return Response(result, status=status.HTTP_400_BAD_REQUEST)            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    @method_decorator_adaptor(permission_required, "apply.ipvs_delete_ipvs_config","/403/")
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        if snippet.is_active == 1:
            IPVS = IPVSRunner(vip=snippet)
            result = IPVS.run('del_vip')            
            if result:return Response(result, status=status.HTTP_400_BAD_REQUEST)        
        return Response(status=status.HTTP_204_NO_CONTENT)  
     
class IPVS_RS_LIST(APIView,IVPSManage):
     
    @method_decorator_adaptor(permission_required, "apply.ipvs_read_ipvs_config","/403/")     
    def get(self,request,*args,**kwargs): 
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
        try:
            ipvs_list = IPVS_RS_CONFIG.objects.filter(**query_params)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=ipvs_list, request=request, view=self)
        ser = serializers.IPVSRealServerSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)  
 
    @method_decorator_adaptor(permission_required, "apply.ipvs_add_ipvs_config","/403/")     
    def post(self,request,*args,**kwargs):
        serializer = serializers.IPVSRealServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            IPVS = IPVSRunner(vip=self.get_ipvs_vip(id=serializer.data.get('ipvs_vip')),realserver=self.get_ipvs_rs(id=serializer.data.get('id')))
            result = IPVS.run('add_rs')
            if result:return Response(result, status=status.HTTP_400_BAD_REQUEST)            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class IPVS_RS_LIST_DETAIL(APIView,IVPSManage):
    
    def get_object(self, pk):
        try:
            return IPVS_RS_CONFIG.objects.get(id=pk)
        except IPVS_RS_CONFIG.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_read_ipvs_config","/403/")     
    def get(self,request,pk,format=None):
        snippet = self.get_object(pk)
        serializer = serializers.IPVSRealServerSerializer(snippet)
        return Response(serializer.data)
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_change_ipvs_config","/403/")
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.IPVSRealServerSerializer(snippet, data=request.data)     
        if serializer.is_valid():
            serializer.save()         
            IPVS = IPVSRunner(vip=self.get_ipvs_vip(id=serializer.data.get('ipvs_vip')),realserver=self.get_ipvs_rs(id=serializer.data.get('id')))
            result = IPVS.run('modf_rs',request.data)
            if result:return Response(result, status=status.HTTP_400_BAD_REQUEST)            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    @method_decorator_adaptor(permission_required, "apply.ipvs_delete_ipvs_config","/403/")
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        IPVS = IPVSRunner(vip=self.get_ipvs_vip(id=snippet.ipvs_vip.id),realserver=snippet)
        result = IPVS.run('del_rs')
        if result:return Response(result, status=status.HTTP_400_BAD_REQUEST)          
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    

class IPVS_NS_LIST(APIView):
     
    @method_decorator_adaptor(permission_required, "apply.ipvs_read_ipvs_config","/403/")     
    def get(self,request,*args,**kwargs): 
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
        try:
            ipvs_list = IPVS_NS_CONFIG.objects.filter(**query_params)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=ipvs_list, request=request, view=self)
        ser = serializers.IPVSNanmeServerSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)  
 
    @method_decorator_adaptor(permission_required, "apply.ipvs_add_ipvs_config","/403/")     
    def post(self,request,*args,**kwargs):
        serializer = serializers.IPVSNanmeServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()          
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    
class IPVS_NS_LIST_DETAIL(APIView):
    
    def get_object(self, pk):
        try:
            return IPVS_NS_CONFIG.objects.get(id=pk)
        except IPVS_NS_CONFIG.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_read_ipvs_config","/403/")     
    def get(self,request,pk,format=None):
        snippet = self.get_object(pk)
        serializer = serializers.IPVSNanmeServerSerializer(snippet)
        return Response(serializer.data)
    
    @method_decorator_adaptor(permission_required, "apply.ipvs_change_ipvs_config","/403/")
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.IPVSNanmeServerSerializer(snippet, data=request.data)     
        if serializer.is_valid():
            serializer.save()                    
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    @method_decorator_adaptor(permission_required, "apply.ipvs_delete_ipvs_config","/403/")
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)         
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  