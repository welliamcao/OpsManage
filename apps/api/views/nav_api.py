#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from api import serializers
from navbar.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from utils.logger import logger
from rest_framework.views import  APIView,Response
from dao.navbar import NAVBAR


@api_view(['GET', 'POST' ])
def navtype_list(request,format=None):  
    if request.method == 'GET':     
        snippets = Nav_Type.objects.all()
        serializer = serializers.NavTypeSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST' and request.user.has_perm('navbar.nav_add_nav_type'):
        serializer = serializers.NavTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('navbar.nav_read_nav_type',raise_exception=True)
def navtype_detail(request, id,format=None):  
    try:
        snippet = Nav_Type.objects.get(id=id)
    except Nav_Type.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.NavTypeSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT' and request.user.has_perm('navbar.nav_change_nav_type'):
        serializer = serializers.NavTypeSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('navbar.nav_delete_nav_type'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
@api_view(['GET', 'POST' ])
def navnumber_list(request,format=None):
    """
    List all order, or create a server assets order.
    """    
    if request.method == 'GET':     
        snippets = Nav_Type_Number.objects.all()
        serializer = serializers.NavTypeNumberSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST' and request.user.has_perm('navbar.nav_add_nav_number'):
        snippet = NAVBAR.createNavBar(request)
        if isinstance(snippet, str):return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,data=snippet) 
        serializer = serializers.NavTypeNumberSerializer(snippet)
        return Response(serializer.data)
       

@api_view(['GET', 'PUT', 'DELETE'])
def navnumber_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Nav_Type_Number.objects.get(id=id)
    except Nav_Type_Number.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.NavTypeNumberSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT' and request.user.has_perm('navbar.nav_change_nav_number'):
        serializer = serializers.NavTypeNumberSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            NAVBAR.updateImg(snippet) 
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('navbar.nav_delete_nav_number'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
    
    
@api_view(['GET', 'POST' ])
def navthird_list(request,format=None):  
    if request.method == 'GET':     
        snippets = Nav_Third.objects.all()
        serializer = serializers.NavThirdSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST' and request.user.has_perm('navbar.nav_add_nav_type'):
        serializer = serializers.NavThirdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def navthird_detail(request, id,format=None):  
    try:
        snippet = Nav_Third.objects.get(id=id)
    except Nav_Third.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.NavThirdSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT' and request.user.has_perm('navbar.nav_change_nav_type'):
        serializer = serializers.NavThirdSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('navbar.nav_delete_nav_type'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['GET', 'POST' ])
def navthird_number_list(request,format=None):
    """
    List all order, or create a server assets order.
    """    
    if request.method == 'GET':     
        snippets = Nav_Third_Number.objects.all()
        serializer = serializers.NavThirdNumberSerializer(snippets, many=True)
        return Response(serializer.data)     
    
    elif request.method == 'POST' and request.user.has_perm('navbar.nav_add_nav_number'):
        try:
            number = Nav_Third_Number.objects.create(**request.data)
        except Exception as ex:
            return Response({"msg":str(ex)}, status=status.HTTP_400_BAD_REQUEST)      
        try:  
            snippet = Nav_Third_Number.objects.get(id=number.id)
            serializer = serializers.NavThirdNumberSerializer(snippet)
        except Exception as ex:
            logger.error(msg="添加成员失败: {ex}".format(ex=str(ex)))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        return Response(serializer.data)
       

@api_view(['GET', 'PUT', 'DELETE'])
def navthird_number_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """    
    try:
        snippet = Nav_Third_Number.objects.get(id=id)
    except Nav_Third_Number.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.NavThirdNumberSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT' and request.user.has_perm('navbar.nav_change_nav_number'):
        serializer = serializers.NavThirdNumberSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('navbar.nav_delete_nav_number'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        