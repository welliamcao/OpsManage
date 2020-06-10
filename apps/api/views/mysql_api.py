#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import os
from rest_framework import viewsets,permissions
from api import serializers
from databases.models import *
from asset.models import Assets
from django.http import QueryDict
from rest_framework import status
from django.http import Http404,StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from dao.base import DataHandle
from service.mysql.mysql_base import MySQLBase,MySQLARCH
from dao.mysql import DBManage,DBConfig, DBUser
from django.http import JsonResponse
from utils.logger import logger
from utils.base import method_decorator_adaptor,file_iterator
from account.models import User
from service import  mysql_service
  
    
@api_view(['GET','PUT', 'DELETE'])
def db_detail(request, id,format=None):
    try:
        snippet = DataBase_MySQL_Server_Config.objects.get(id=id)
    except DataBase_MySQL_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        try:  
            snippet = DataBase_MySQL_Server_Config.objects.get(id=id)
            serializer = serializers.DataBaseServerSerializer(snippet)
        except  DataBase_MySQL_Server_Config.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data) 
            
    elif request.method == 'PUT':
        if not request.user.has_perm('databases.database_can_change_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN) 
        
        serializer = serializers.DataBaseServerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if request.data.get("db_passwd"):
                snippet.db_passwd = request.data.get("db_passwd")
                snippet.save()            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('databases.database_can_delete_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
         
    
class DB_CUSTOM_SQL(APIView,DBConfig):
    @method_decorator_adaptor(permission_required, "databases.database_can_read_sql_custom_high_risk_sql","/403/")     
    def get(self, request, format=None):
        snippets = Custom_High_Risk_SQL.objects.all()
        serializer = serializers.CustomSQLSerializer(snippets, many=True)
        return Response(serializer.data) 
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_sql_custom_high_risk_sql","/403/")
    def post(self, request, format=None):
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
    
    
class DatabaseExecuteHistory(APIView):
    
    @method_decorator_adaptor(permission_required, "databases.database_read_sql_execute_history","/403/")        
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for k in request.query_params.keys():
            if k not in ["offset"]:
                query_params[k] = request.query_params.get(k)
            
        if request.user.is_superuser and query_params:
            logs_list = SQL_Execute_History.objects.filter(**query_params)
            
        elif not request.user.is_superuser and query_params:
            query_params["exe_user"] = request.user.username
            logs_list = SQL_Execute_History.objects.filter(**query_params)
            
        elif request.user.is_superuser:   
            logs_list = SQL_Execute_History.objects.all()
            
        else:    
            query_params["exe_user"] = request.user.username
            logs_list = SQL_Execute_History.objects.filter(**query_params)
        
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=logs_list, request=request, view=self)
        ser = serializers.HistorySQLSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)    

class DatabaseExecuteHistoryDetail(APIView):  
    
    @method_decorator_adaptor(permission_required, "databases.database_change_sql_execute_history","/403/")  
    def put(self,request, id, *args, **kwargs):
        try:
            snippet = SQL_Execute_History.objects.get(id=id)
        except SQL_Execute_History.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        
        try:
            snippet.favorite = request.POST.get("favorite")
            snippet.mark = request.POST.get("mark")
            snippet.save()
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_400_BAD_REQUEST)  
                  
        serializer = serializers.HistorySQLSerializer(snippet)
        return Response(serializer.data)   

    
@api_view(['POST','GET'])
@permission_required('databases.database_query_database_server_config',raise_exception=True)  
def db_status(request, id,format=None):
    try:
        dbServer = DataBase_MySQL_Server_Config.objects.get(id=id)
    except DataBase_MySQL_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'GET':
        MySQL_STATUS = {}
        if not request.query_params:
            MySQL_STATUS =  mysql_service.varibles(dbServer.to_connect())
        
        if request.query_params.get("type"):
            MySQL_STATUS = mysql_service.allowcator(request.query_params.get("type"),dbServer.to_connect())
        
        return JsonResponse({"code":200,"msg":"success","data":MySQL_STATUS})
    
@api_view(['POST','GET'])
@permission_required('databases.database_can_read_database_server_config',raise_exception=True)  
def db_org(request, id,format=None):
    try:
        dbServer = DataBase_MySQL_Server_Config.objects.get(id=id)
    except DataBase_MySQL_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'POST':
        MYSQL = MySQLBase(dbServer.to_connect())
        ARCH_INFO = MySQLARCH(MYSQL, dbServer.to_connect())
        if dbServer.db_mode == 'pxc':data = ARCH_INFO.pxc()
        elif dbServer.db_mode == 'slave':data = ARCH_INFO.master_slave()
        else:
            data = ARCH_INFO.single()
        return JsonResponse({"code":200,"msg":"success","data":data})    
        
        
@api_view(['POST','GET'])
@permission_required('databases.database_query_database_server_config',raise_exception=True)  
def db_tree(request,format=None):   
    if request.method == 'GET':
        return Response(DBManage().tree(request))   
    

class DB_SERVER_LIST(APIView,DBConfig):
    @method_decorator_adaptor(permission_required, "databases.database_read_database_server_config","/403/")     
    def get(self,request,format=None):
        snippets = [ x.to_json() for x in  DataBase_MySQL_Server_Config.objects.all() ]
        return Response(snippets)
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_database_server_config","/403/")
    def post(self, request, format=None):
        try:
            database = DataBase_MySQL_Server_Config.objects.create(**request.data)
        except Exception as ex:
            return Response({"msg":str(ex)}, status=status.HTTP_400_BAD_REQUEST)      
        try:  
            snippet = DataBase_MySQL_Server_Config.objects.get(id=database.id)
            serializer = serializers.DataBaseServerSerializer(snippet)
        except DataBase_MySQL_Server_Config.DoesNotExist:
            logger.error(msg="添加数据库失败: {ex}".format(ex=str(ex)))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        return Response(serializer.data)     
    

class DB_SERVER_DETAIL(APIView,DBConfig):
    
    def get_object(self, pk):
        try:
            return DataBase_MySQL_Server_Config.objects.get(id=pk)
        except DataBase_MySQL_Server_Config.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "databases.database_read_database_server_config","/403/")     
    def get(self,request,pk,format=None):
        snippet = self.get_object(pk)
        try:  
            snippets = Database_MySQL_Detail.objects.filter(db_server=snippet)
            serializer = serializers.DatabaseSerializer(snippets, many=True)
        except  Database_MySQL_Detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data) 
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_database_server_config","/403/")
    def post(self, request, pk, format=None):
        dbServer = self.get_object(pk)
        snippets = self.sync_db(dbServer)
        serializer = serializers.DatabaseSerializer(snippets, many=True)
        return Response(serializer.data)    

class DB_SERVER_TABLES(APIView,DBConfig):
    
    def get_db_server(self, pk):
        try:
            return DataBase_MySQL_Server_Config.objects.get(id=pk)
        except DataBase_MySQL_Server_Config.DoesNotExist:
            raise Http404    
    
    def get_db(self, pk):
        try:
            return Database_MySQL_Detail.objects.get(id=pk)
        except Database_MySQL_Detail.DoesNotExist:
            raise Http404         
    
    @method_decorator_adaptor(permission_required, "databases.database_query_database_server_config","/403/")
    def get(self, request, pk, format=None):
        db = self.get_db(pk)
        snippets = Database_Table_Detail_Record.objects.filter(db=db.id)
        serializer = serializers.DatabaseTableSerializer(snippets, many=True)
        return Response(serializer.data)        
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_database_server_config","/403/")
    def post(self, request, pk, format=None):
        dbServer = self.get_db_server(pk)
        snippets = self.sync_table(dbServer, request.POST.get("db_id",0), request.POST.get("db_name"))
        serializer = serializers.DatabaseTableSerializer(snippets, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT', 'DELETE'])
def db_server_db_detail(request, sid, id,format=None):
    try:
        db_server = DataBase_MySQL_Server_Config.objects.get(id=sid)
    except DataBase_MySQL_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        snippet = Database_MySQL_Detail.objects.get(id=id,db_server=db_server)
    except Database_MySQL_Detail.DoesNotExist:
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
        Database_Table_Detail_Record.objects.filter(db=id).delete() #删除数据库关联表记录
        Database_MySQL_User.objects.filter(db=snippet.id).delete() #删除用户关联数据库记录
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class DB_DATA_DICT(APIView, DBConfig, DataHandle):
    def get_db_server(self, sid):
        try:
            return DataBase_MySQL_Server_Config.objects.get(id=sid)
        except DataBase_MySQL_Server_Config.DoesNotExist:
            raise Http404 
        
    def get_db(self, did):
        try:
            return Database_MySQL_Detail.objects.get(id=did)
        except Database_MySQL_Detail.DoesNotExist:
            raise Http404              
    
    @method_decorator_adaptor(permission_required, "databases.database_sqldict_database_server_config","/403/")    
    def post(self,request, sid, did, format=None):
        dbServer,db = self.get_db_server(sid), self.get_db(did) 
        user_tables = self.get_user_db_tables(db, request.user)
        data = self.get_db_dict(dbServer, db, user_tables)
        filePath = self.saveScript(content=data,filePath='./upload/sql_dict/{db_server}_{db_name}.html'.format(db_server=(dbServer.to_json().get('ip')+ '_' +str(dbServer.db_port)),db_name=db.db_name))
        response = StreamingHttpResponse(file_iterator(filePath))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="{file_name}'.format(file_name=os.path.basename(filePath))
        return response 


class DB_USER_DB_LIST(APIView,DBUser):
    
    def get_user(self,uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            raise Http404      
    
    def get(self,request,format=None):
        s_query_params,u_query_params = dict(),dict()
        for ds in request.query_params.keys():
            if ds in ["is_write"]:
                u_query_params[ds] = request.query_params.get(ds)
            else:
                s_query_params[ds] = request.query_params.get(ds)
        return Response(self.get_user_db(request.user,s_query_params,u_query_params))

class DB_USER_DB(APIView,DBUser):
    
    def get_user(self,uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            raise Http404     
    
    def get(self, request, uid, format=None):
        if request.user.is_superuser:
            user = self.get_user(uid)
            return Response(self.get_user_db(user))
        else:
            raise Http404


class DB_USER_SERVER_DBLIST(APIView,DBUser):
    
    def get_db_server(self, sid):
        try:
            return DataBase_MySQL_Server_Config.objects.get(id=sid)
        except DataBase_MySQL_Server_Config.DoesNotExist:
            raise Http404  
    
    def get_user(self,uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            raise Http404      
    
    @method_decorator_adaptor(permission_required, "databases.database_can_read_database_server_config","/403/")    
    def get(self, request, uid, sid, format=None):   
        return Response(self.get_server_all_db(self.get_db_server(sid), self.get_user(uid)))
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_database_server_config","/403/") 
    def post(self, request, uid, sid, format=None):
        
        db_server, user = self.get_db_server(sid), self.get_user(uid) 
        
        self.update_user_server_db(request, db_server, user)
        
        return Response(self.get_user_server_db(db_server, user), status=status.HTTP_201_CREATED)        
    
    @method_decorator_adaptor(permission_required, "databases.database_can_delete_database_server_config","/403/")     
    def delete(self, request, uid, sid, format=None):
        Database_MySQL_User.objects.filter(id=QueryDict(request.body).get("user_db_id")).delete()
        return Response(self.get_user_server_db(self.get_db_server(sid), self.get_user(uid)))        
                
@api_view(['GET','POST'])
def db_user_db_table_list(request, uid, did, format=None):
        
    try:
        user_db = Database_MySQL_User.objects.get(db=did,user=uid)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET':
        user_table_list = []

        try:
            db_info = Database_MySQL_Detail.objects.get(id=did)
        except Database_MySQL_Detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
                   
        result= MySQLBase(dbServer=db_info.to_connect()).get_tables()
        
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
    
    
class DB_USER_SERVER_DBSQL(APIView,DBUser):
    
    def get_db(self,uid ,did):
        try:
            return  Database_MySQL_User.objects.get(db=did,user=uid)
        except Database_MySQL_User.DoesNotExist:
            raise Http404  
    
    def get_user(self,uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            raise Http404          
        
    @method_decorator_adaptor(permission_required, "databases.database_can_read_database_server_config","/403/")    
    def get(self, request, uid, did, format=None):   
        return Response(self.get_user_db_sql(self.get_db(uid, did)))    
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_database_server_config","/403/") 
    def post(self, request, uid, did, format=None):  
        
        user_db = self.get_db(uid, did)
        
        try:
            user_db.sqls = ",".join(request.data.getlist('sqls'))
            user_db.save()
        except Exception as ex:
            return  Response(str(ex), status=status.HTTP_400_BAD_REQUEST)        
          
        return Response(self.get_user_db_sql(self.get_db(uid, did)))       