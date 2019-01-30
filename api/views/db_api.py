#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api import serializers
from databases.models import *
from asset.models import Assets
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from orders.models import Order_System
from dao.base import MySQLPool
from dao.database import MySQLARCH
from django.http import JsonResponse
from utils.logger import logger
from utils import mysql as MySQL

@api_view(['POST'])
@permission_required('databases.database_can_add_database_server_config',raise_exception=True)
def db_list(request,format=None):               
    if request.method == 'POST':  
        try:
            database = DataBase_Server_Config.objects.create(**request.data)
        except Exception as ex:
            return Response({"msg":str(ex)}, status=status.HTTP_400_BAD_REQUEST)      
        try:  
            snippet = DataBase_Server_Config.objects.get(id=database.id)
            serializer = serializers.DataBaseServerSerializer(snippet)
        except DataBase_Server_Config.DoesNotExist:
            logger.error(msg="添加数据库失败: {ex}".format(ex=str(ex)))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        return Response(serializer.data)   
    
@api_view(['GET','PUT', 'DELETE'])
def db_detail(request, id,format=None):
    try:
        snippet = DataBase_Server_Config.objects.get(id=id)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        try:  
            snippet = DataBase_Server_Config.objects.get(id=id)
            serializer = serializers.DataBaseServerSerializer(snippet)
        except  DataBase_Server_Config.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data) 
            
    if request.method == 'PUT':
        if not request.user.has_perm('databases.database_can_change_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN) 
        serializer = serializers.DataBaseServerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('databases.database_can_delete_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
@api_view(['POST' ])
@permission_required('databases.database_can_add_inception_server_config',raise_exception=True)
def inc_list(request,format=None):
    """
    List all order, or create a server assets order.
    """     
    if request.method == 'POST':
        serializer = serializers.InceptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_required('databases.database_can_change_inception_server_config',raise_exception=True)
def inc_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Inception_Server_Config.objects.get(id=id)
    except Inception_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = serializers.InceptionSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('databases.database_can_delete_inception_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

    
# @api_view(['PUT', 'DELETE'])
# @permission_required('Datdatabasestabase_can_change_order_systemr',raise_exception=True)
# def sql_order_detail(request, id,format=None):
#     """
#     Retrieve, update or delete a server assets instance.
#     """
#     try:
#         snippet = Order_System.objects.get(id=id)
#     except Order_System.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'PUT':
#         if int(request.data.get('order_status')) == 4:
#             sendOrderNotice.delay(id,mask='【已取消】')  
#         elif int(request.data.get('order_status')) == 6:
#             sendOrderNotice.delay(id,mask='【已授权】')  
#         serializer = serializers.AuditSqlOrderSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#      
#     elif request.method == 'DELETE':
#         if not request.user.has_perm('Databasdatabasesse_can_delete_order_system'):
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)       
    
    
@api_view(['POST' ])
@permission_required('databases.database_can_add_sql_custom_high_risk_sql',raise_exception=True)
def sql_custom_list(request,format=None):
    """
    List all order, or create a server assets order.
    """     
    if request.method == 'POST':
        serializer = serializers.CustomSQLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT', 'DELETE'])
@permission_required('databases.database_can_change_custom_high_risk_sql',raise_exception=True)
def sql_custom_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Custom_High_Risk_SQL.objects.get(id=id)
    except Custom_High_Risk_SQL.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = serializers.CustomSQLSerializer(snippet)
        return Response(serializer.data)         
    
    elif request.method == 'PUT':
        serializer = serializers.CustomSQLSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('databases.database_can_delete_custom_high_risk_sql'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
@api_view(['PUT', 'DELETE'])
@permission_required('databases.database_can_change_sql_execute_histroy',raise_exception=True)
def sql_exec_logs(request, id,format=None):
    try:
        snippet = SQL_Execute_Histroy.objects.get(id=id)
    except SQL_Execute_Histroy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
     
    if request.method == 'DELETE':
        if not request.user.has_perm('databases.database_can_delete_sql_execute_histroy'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST','GET'])
@permission_required('databases.database_can_read_database_server_config',raise_exception=True)  
def db_status(request, id,format=None):
    try:
        dbServer = DataBase_Server_Config.objects.get(id=id)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'POST':
        MySQL_STATUS = {}
        MYSQL = MySQLPool(host=dbServer.db_assets.server_assets.ip,port=dbServer.db_port,user=dbServer.db_user,passwd=dbServer.db_passwd,dbName=dbServer.db_name)
        STATUS = MYSQL.get_status()
        GLOBAL = MYSQL.get_global_status()
        MySQL_STATUS['base'] = STATUS[0] + GLOBAL
        MySQL_STATUS['pxc'] = STATUS[1] 
        MySQL_STATUS['master'] = MYSQL.get_master_status()
        MySQL_STATUS['slave'] = MYSQL.get_slave_status()
        return JsonResponse({"code":200,"msg":"success","data":MySQL_STATUS})
    
@api_view(['POST','GET'])
@permission_required('databases.database_can_read_database_server_config',raise_exception=True)  
def db_org(request, id,format=None):
    try:
        dbServer = DataBase_Server_Config.objects.get(id=id)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'POST':
        MYSQL = MySQLPool(host=dbServer.db_assets.server_assets.ip,port=dbServer.db_port,user=dbServer.db_user,passwd=dbServer.db_passwd,dbName=dbServer.db_name)
        ARCH_INFO = MySQLARCH(MYSQL,dbServer)
        if dbServer.db_mode == 3:data = ARCH_INFO.pxc()
        elif dbServer.db_mode == 2:data = ARCH_INFO.master_slave()
        else:
            data = ARCH_INFO.single()
        return JsonResponse({"code":200,"msg":"success","data":data})    
        