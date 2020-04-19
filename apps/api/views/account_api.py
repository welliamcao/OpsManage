#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import os
from rest_framework.views import APIView
from api import serializers
from rest_framework import status
from account.models import User, Role, Structure, User_Async_Task
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utils.logger import logger
from dao.account import StructureManage,UsersManage
from mptt.templatetags.mptt_tags import cache_tree_children
from django.http import Http404,StreamingHttpResponse
from django.contrib.auth.decorators import permission_required
from OpsManage.celery import app as celery_app
from django.utils import timezone
from utils.base import file_iterator

@api_view(['GET', 'POST' ])
def user_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':   
        
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)        
           
        snippets = User.objects.filter(**query_params)
        serializer = serializers.UserSerializer(snippets, many=True)
        return Response(serializer.data)  
       
    elif request.method == 'POST':
        if not request.user.has_perm('account.account_add_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)        
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('account.account_add_user',raise_exception=True)
def user_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.UserSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('account.account_delete_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  


class UserSuperior(APIView,UsersManage):
        
    def get(self,request,*args,**kwargs): 
        return Response(self.get_user_superior(request.user)) 

class UserTask(APIView):
        
    def get(self, request, *args, **kwargs): 
        if request.user.is_superuser:
            task_list = User_Async_Task.objects.all().order_by("-id")
        else:
            task_list = User_Async_Task.objects.filter(user=request.user.id).order_by("-id")
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=task_list, request=request, view=self)
        ser = serializers.UserTaskSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data) 

class UserTaskDetail(APIView):
     
    def get_object(self, pk, request):
        try:
            task = User_Async_Task.objects.get(id=pk)
            if not request.user.is_superuser and task.user != request.user.id:
                raise Http404       
            return task     
        except User_Async_Task.DoesNotExist:
            raise Http404      
     
    def get(self, request, pk, *args,**kwargs): 
        snippet = self.get_object(pk, request)
        serializer = serializers.UserTaskSerializer(snippet)
        return Response(serializer.data)         
         
    def post(self,request, pk, *args,**kwargs):
        snippet = self.get_object(pk, request)
        
        if request.POST.get("action") == "stop": 
            ctask = celery_app.AsyncResult(snippet.ctk)
            if ctask.status == "FAILURE":
                snippet.msg = ctask.result
            else:
                snippet.msg = request.POST.get("msg")
            #bug https://github.com/celery/celery/issues/2727    
            celery_app.control.revoke(snippet.ctk, terminate=True, signal='SIGUSR1')

        snippet.etime = timezone.now()
        snippet.status = 2
        snippet.save()
            
        serializer = serializers.UserTaskSerializer(snippet)
        return Response(serializer.data)

    def delete(self, request, pk, *args,**kwargs): 
        
        snippet = self.get_object(pk, request)
                  
        if snippet.file:
            task_file = os.getcwd() + '/' + str(snippet.file)
            if os.path.exists(task_file):
                os.remove(task_file)    
                     
        snippet.delete()       
        return Response(status=status.HTTP_204_NO_CONTENT) 


class UserTaskDownload(APIView):
     
    def get_object(self, pk, request):
        try:
            task = User_Async_Task.objects.get(id=pk)
            if not request.user.is_superuser and task.user != request.user.id:
                raise Http404       
            return task     
        except User_Async_Task.DoesNotExist:
            raise Http404      
              
    def post(self, request, pk, *args,**kwargs):
        snippet = self.get_object(pk, request)
        
        if snippet.file:
            task_file = os.getcwd() + '/' + str(snippet.file)
            response = StreamingHttpResponse(file_iterator(task_file))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(file_name=os.path.basename(task_file))
            return response 
        return Http404 

@api_view(['GET', 'POST' ])
def role_list(request,format=None):
    """
    List all order, or create a server assets order.
    """    
    if request.method == 'GET':      
        snippets = Role.objects.all()
        serializer = serializers.RoleSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        if not  request.user.has_perm('account.account_add_role'):
            return Response(status=status.HTTP_403_FORBIDDEN)         
        serializer = serializers.RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('account.account_add_role',raise_exception=True)
def role_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Role.objects.get(id=id)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.RoleSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT' and request.user.has_perm('OpsManage.change_group'):
        serializer = serializers.RoleSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.delete_group'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()    
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
class GROUP_LIST(APIView,StructureManage):
        
    def get(self,request,*args,**kwargs): 

        try:
            tree_list = Structure.objects.filter(level__gt=0)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_all_sub_node(tree_list))  
    
class STRUCTURE_TREE_LIST(APIView):
    '''(right - left - 1) // 2 = 节点下面有多少个子节点'''
    
    def recursive_node_to_dict(self,node):
        json_format = node.to_json()
        children = [self.recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            json_format['children'] = children
        else:
            json_format['icon'] = 'fa fa-minus-square-o'         
        return json_format
        
    def get(self,request,*args,**kwargs): 
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
        
        try:
            tree_list = Structure.objects.filter(**query_params)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)

        root_nodes = cache_tree_children(tree_list)
        dicts = []
        for n in root_nodes:
            dicts.append(self.recursive_node_to_dict(n))
     
        return Response(dicts)     
    
#业务节点列表
class STRUCTURE_LIST(APIView,StructureManage):
    
    def get(self,request,*args,**kwargs): 
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
 
        if not query_params:
            snippets = Structure.objects.filter(parent__isnull=True)
        else:
            if len(list(set(["tree_id","lft","rght"]).intersection(set(query_params.keys())))) == 3: #查询节点下面的所有子节点   
                snippets = self.get_nodes_all_children(tree_id=query_params.get("tree_id"), lft=query_params.get("lft"), rght=query_params.get("rght"))
            else:
                snippets = Structure.objects.filter(**query_params)                
        serializer = serializers.StructureSerializer(snippets, many=True)
        return Response(serializer.data)    
    
    def post(self,request,*args,**kwargs):
         
        if not request.user.has_perm('account.account_add_structure'):  
            return Response(status=status.HTTP_403_FORBIDDEN)  
        try:
            business = Structure.objects.get(id=request.data["parent"])
        except:
            business = None
            
        if (business and self.get_assets(business).count() == 0) or business is None:  
                
            serializer = serializers.StructureSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
         
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
        else:
            return Response("请先清除当前节点下面绑定的资产", status=status.HTTP_400_BAD_REQUEST)

class STRUCTURE_NODE_DETAIL(APIView,StructureManage):
    
    def get_object(self, pk):
        try:
            return Structure.objects.get(id=pk)
        except Structure.DoesNotExist:
            raise Http404  
            
    def get(self, request, pk, *args,**kwargs): 
        snippet = self.get_object(pk)
        
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)

        if not query_params:
            
            serializer = serializers.StructureSerializer(snippet)
            
            return Response(serializer.data)        
        
        elif query_params.get("type") == "children":
            
            serializer = serializers.StructureSerializer(snippet.get_children(), many=True)
            
            return Response(serializer.data) 
                   
        else:    
            snippets = Structure.objects.filter(**query_params)    
        
        serializer = serializers.StructureSerializer(snippets, many=True)
            
        return Response(serializer.data) 

    
    def put(self, request, pk, *args,**kwargs):
        
        snippet = self.get_object(pk)
        
        if not request.user.has_perm('account.account_change_structure'):  
            return Response(status=status.HTTP_403_FORBIDDEN)     
           
        serializer = serializers.StructureSerializer(snippet, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, *args,**kwargs): 
        
        snippet = self.get_object(pk)
          
        if not request.user.has_perm('asset.account_delete_structure'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        bRbt = StructureManage()
        
        if snippet.is_leaf_node() and bRbt.get_assets(snippet).count() > 0:
            return Response("请先清除当前节点下面绑定的资产", status=status.HTTP_400_BAD_REQUEST)
            
        for children in snippet.get_children():
            if bRbt.get_assets(children).count() > 0:
                return Response("请先清除当前节点或者子节点下面绑定的资产", status=status.HTTP_400_BAD_REQUEST)
        
     
        snippet.delete()       
        return Response(status=status.HTTP_204_NO_CONTENT)          
                          
#业务节点
class NODES_MEMBER_DETAIL(APIView,StructureManage):
     
    def get_object(self, pk):
        try:
            return Structure.objects.get(id=pk)
        except Structure.DoesNotExist:
            raise Http404      
     
    def get(self, request, pk, *args,**kwargs): 
        snippet = self.get_object(pk)
         
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
             
        if not query_params:
            return Response(self.get_node_json_user(snippet))                    
         
        elif query_params.get("type") == "unallocated":
             
            return Response(self.get_node_unallocated_json_member(snippet))    
         
        else: 
             
            return Response([]) 
         
         
    def post(self,request, pk, *args,**kwargs):
          
        if not request.user.has_perm('account.account_change_structure'):  
            return Response(status=status.HTTP_403_FORBIDDEN)  
         
        snippet = self.get_object(pk)
                     
        user_list = User.objects.filter(id__in=request.data.getlist('user'))
         
        try:
            snippet.user_set.add(*user_list)
        except Exception as ex:
            msg="部门管理成员失败: {ex}".format(ex=str(ex))
            logger.error(msg)
            return Response(msg,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
         
        serializer = serializers.StructureSerializer(snippet)
        return Response(serializer.data)
     
    def delete(self, request, pk, *args,**kwargs): 
         
        snippet = self.get_object(pk)
           
        if not request.user.has_perm('account.account_delete_structure'):  
            return Response(status=status.HTTP_403_FORBIDDEN)
    
        user_list = User.objects.filter(id__in=request.data.getlist('user'))
         
        try:
            snippet.user_set.remove(*user_list)
        except Exception as ex:
            msg="部门管理成员失败: {ex}".format(ex=str(ex))
            logger.error(msg)
            return Response(msg,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
        return Response(status=status.HTTP_204_NO_CONTENT)      