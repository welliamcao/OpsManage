#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from rest_framework import status
from api import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

@api_view(['GET', 'POST' ])
def user_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = User.objects.all()
        serializer = serializers.UserSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        if not request.user.has_perm('OpsManage.add_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)        
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('OpsManage.change_user',raise_exception=True)
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
        if not request.user.has_perm('OpsManage.delete_user'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  