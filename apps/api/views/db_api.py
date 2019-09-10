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
from dao.base import MySQLPool
from dao.database import MySQLARCH,DBManage,DBUser
from django.http import JsonResponse
from utils.logger import logger
from utils import mysql as MySQL
from utils.base import method_decorator_adaptor
from django.contrib.auth.models import User

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
            
    elif request.method == 'PUT':
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
    
    
class DatabaseExecuteHistroy(APIView):
    
    @method_decorator_adaptor(permission_required, "databases.databases_read_sql_execute_histroy","/403/")        
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for k in request.query_params.keys():
            if k not in ["offset"]:
                query_params[k] = request.query_params.get(k)
            
        if request.user.is_superuser and query_params:
            logs_list = SQL_Execute_Histroy.objects.filter(**query_params)
            
        elif not request.user.is_superuser and query_params:
            query_params["exe_user"] = request.user.first_name
            logs_list = SQL_Execute_Histroy.objects.filter(**query_params)
            
        elif request.user.is_superuser:   
            logs_list = SQL_Execute_Histroy.objects.all()
            
        else:    
            query_params["exe_user"] = request.user.first_name
            logs_list = SQL_Execute_Histroy.objects.filter(**query_params)
        
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=logs_list, request=request, view=self)
        ser = serializers.HistroySQLSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)    
    
@api_view(['POST','GET'])
@permission_required('databases.database_can_read_database_server_config',raise_exception=True)  
def db_status(request, id,format=None):
    try:
        dbServer = DataBase_Server_Config.objects.get(id=id)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'POST':
        MySQL_STATUS = {}
        MYSQL = MySQLPool(dbServer=dbServer.to_connect())
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
        MYSQL = MySQLPool(dbServer.to_connect())
        ARCH_INFO = MySQLARCH(MYSQL,dbServer.to_connect())
        if dbServer.db_mode == 'pxc':data = ARCH_INFO.pxc()
        elif dbServer.db_mode == 'slave':data = ARCH_INFO.master_slave()
        else:
            data = ARCH_INFO.single()
        return JsonResponse({"code":200,"msg":"success","data":data})    
        
        
@api_view(['POST','GET'])
@permission_required('databases.databases_query_database_server_config',raise_exception=True)  
def db_tree(request,format=None):   
    if request.method == 'GET':
        return Response(DBManage().tree(request))   
    
@api_view(['GET','POST'])
def db_server_dblist(request, id,format=None):
    try:
        db_server = DataBase_Server_Config.objects.get(id=id)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        try:  
            snippets = Database_Detail.objects.filter(db_server=db_server)
            serializer = serializers.DatabaseSerializer(snippets, many=True)
        except  Database_Detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data) 

    elif  request.method == 'POST':
        if not request.user.has_perm('databases.database_can_add_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)          
        serializer = serializers.DatabaseSerializer(data=request.data,context={"db_server":db_server})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT', 'DELETE'])
def db_server_db_detail(request, sid, id,format=None):
    try:
        db_server = DataBase_Server_Config.objects.get(id=sid)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        snippet = Database_Detail.objects.get(id=id,db_server=db_server)
    except Database_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    
    if request.method == 'GET':
        serializer = serializers.DatabaseSerializer(snippet)
        return Response(serializer.data) 

    elif  request.method == 'PUT':
        if not request.user.has_perm('databases.database_change_add_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)          
        serializer = serializers.DatabaseSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('databases.database_change_add_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        Database_User.objects.filter(db=snippet.id).delete()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


@api_view(['GET'])
def db_user_db_list(request, format=None):    
    if request.method == 'GET':
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)        
        dataList = []
        if request.user.is_superuser:
            user_data_list = Database_Detail.objects.filter(**query_params)
            for ds in user_data_list:
                data = ds.to_json()
                data["username"] = request.user.username
                data["count"] = 1
                dataList.append(data)                            
        else:    
            for ds in Database_User.objects.filter(user=request.user.id):
                try:
                    data = Database_Detail.objects.get(id=ds.db,**query_params).to_json()
                    data["username"] = request.user.username
                    data["count"] = 1
                    dataList.append(data)
                except Exception as ex: 
                    continue         
        return Response(dataList)


@api_view(['GET','POST'])
@permission_required('Databases.databases_can_read_database_server_config',raise_exception=True) 
def db_user_server_dblist(request, uid, sid, format=None):
    try:
        db_server = DataBase_Server_Config.objects.get(id=sid)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    
    if request.method == 'GET':
        dataList = []
        for ds in Database_Detail.objects.filter(db_server=db_server):
            if user.is_superuser:
                count = 1
            else:
                count = Database_User.objects.filter(db=ds.id,user=uid).count()
            data = ds.to_json()
            data["username"] = user.username
            data["count"] = count
            dataList.append(data)
        return Response(dataList)

    elif  request.method == 'POST':
        if not request.user.has_perm('databases.database_can_add_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN) 
         
        all_user_db_list = [ ds.db for ds in Database_User.objects.filter(user=uid,db__in=[ ds.id for ds in db_server.databases.all()])]

        update_user_db_list = [ int(ds) for ds in request.data.getlist('dbIds') ]

        update_list = list(set(update_user_db_list).difference(set(all_user_db_list)))        
        
        del_list = list(set(all_user_db_list).difference(set(update_user_db_list)))
        
        for dbIds in update_list:
            obj, created = Database_User.objects.update_or_create(db=dbIds, user=uid)  
        
        Database_User.objects.filter(user=uid,db__in=del_list).delete()
            
        dataList = []    
        for ds in Database_Detail.objects.filter(db_server=db_server):
            count = Database_User.objects.filter(db=ds.id,user=uid).count()
            data = ds.to_json()
            data["username"] = user.username
            data["count"] = count
            dataList.append(data)

        return Response(dataList, status=status.HTTP_201_CREATED)      
    
    
@api_view(['GET','POST'])
def db_user_db_table_list(request, uid, did, format=None):
        
    try:
        user_db = Database_User.objects.get(db=did,user=uid)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET':
        user_table_list = []

        try:
            db_info = Database_Detail.objects.get(id=did)
        except Database_Detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
                   
        result= MySQLPool(dbServer=db_info.to_connect()).queryMany('show tables',10000) 
        
        if not isinstance(result, str):
            count,tableList,colName = result[0],result[1],result[2]
            try:
                if user_db.tables:grant_tables = user_db.tables.split(",")
                else:grant_tables = []
            except:
                grant_tables = []

            if count > 0:
                for ds in tableList:
                    data = dict()
                    data["name"] = ds[0]
                    if ds[0] not in grant_tables:                    
                        data["count"] = 0
                    else:
                        data["count"] = 1
                    user_table_list.append(data)

        return Response(user_table_list)

    elif  request.method == 'POST':
        if not request.user.has_perm('databases.database_can_add_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN) 

        try:
            user_db.tables = ",".join(request.data.getlist('table_name'))
            user_db.save()
        except Exception as ex:
            return  Response(str(ex), status=status.HTTP_400_BAD_REQUEST)
        
        return Response(user_db.to_json(), status=status.HTTP_201_CREATED)                         