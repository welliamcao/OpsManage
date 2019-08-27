#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from api import serializers
from sched.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required

@api_view(['GET', 'POST' ])
@permission_required('sched.cron_can_add_cron_config',raise_exception=True)
def cron_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Cron_Config.objects.all()
        serializer = serializers.CronSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.CronSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('sched.cron_can_change_cron_config',raise_exception=True)
def cron_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Cron_Config.objects.get(id=id)
    except Cron_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.CronSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.CronSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_cron_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_required('sched.cron_can_delete_cron_config',raise_exception=True)
# def cronLogsdetail(request, id,format=None):
#     """
#     Retrieve, update or delete a server assets instance.
#     """
#     try:
#         snippet = Log_Cron_Config.objects.get(id=id)
#     except Log_Cron_Config.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#  
#     if request.method == 'GET':
#         serializer = serializers.CronLogsSerializer(snippet)
#         return Response(serializer.data)
#      
#     elif request.method == 'DELETE':
#         if not request.user.has_perm('OpsManage.can_delete_cron_config'):
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)  