#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from api import serializers
from databases.models import *
from asset.models import Assets
from django.http import QueryDict
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from service.redis.redis_base import RedisBase, RedisArch
from dao.redis import RedisManage, RedisConfig, RedisUser
from django.http import JsonResponse
from utils.logger import logger
from utils.base import method_decorator_adaptor
from account.models import User
from service import  redis_service
  
    
@api_view(['GET','PUT', 'DELETE'])
def db_detail(request, id, format=None):
    try:
        snippet = DataBase_Redis_Server_Config.objects.get(id=id)
    except DataBase_Redis_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        try:  
            snippet = DataBase_Redis_Server_Config.objects.get(id=id)
            serializer = serializers.RedisServerSerializer(snippet)
        except  DataBase_Redis_Server_Config.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data) 
            
    elif request.method == 'PUT':
        if not request.user.has_perm('databases.database_can_change_redis_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN) 
        
        serializer = serializers.RedisServerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if request.data.get("db_passwd"):
                snippet.db_passwd = request.data.get("db_passwd")
                snippet.save()            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('databases.database_can_delete_redis_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
         

@api_view(['POST','GET'])
@permission_required('databases.database_query_redis_server_config',raise_exception=True)  
def db_status(request, id,format=None):
    try:
        dbServer = DataBase_Redis_Server_Config.objects.get(id=id)
    except DataBase_Redis_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'GET':
        
        REDIS_STATUS = {}
                    
        if request.query_params.get("type"):
            REDIS_STATUS = redis_service.allowcator(request.query_params.get("type"),dbServer.to_connect())        
        else:
            REDIS_STATUS = RedisBase(dbServer.to_connect()).get_info("server")
        
        return JsonResponse({"code":200,"msg":"success","data":REDIS_STATUS})
    

@api_view(['POST','GET'])
@permission_required('databases.database_read_redis_server_config',raise_exception=True)  
def db_org(request, id,format=None):
    try:
        dbServer = DataBase_Redis_Server_Config.objects.get(id=id)
    except DataBase_Redis_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'POST':
        Redis = RedisBase(dbServer.to_connect())
        ARCH_INFO = RedisArch(Redis, dbServer.to_connect())
        if dbServer.db_mode == 'cluster':data = ARCH_INFO.cluster()
        elif dbServer.db_mode == 'ms':data = ARCH_INFO.master_slave()
        elif dbServer.db_mode == 'slave':data = ARCH_INFO.slave()
        else:
            data = ARCH_INFO.single()
        return JsonResponse({"code":200,"msg":"success","data":data})    
        
        
@api_view(['POST','GET'])
@permission_required('databases.database_query_redis_server_config',raise_exception=True)  
def db_tree(request,format=None):   
    if request.method == 'GET':
        return Response(RedisManage().tree(request))   
    

class REDIS_SERVER_LIST(APIView,RedisConfig):
    @method_decorator_adaptor(permission_required, "databases.database_read_redis_server_config","/403/")     
    def get(self,request,format=None):
        snippets = [ x.to_json() for x in  DataBase_Redis_Server_Config.objects.all() ]
        return Response(snippets)
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_redis_server_config","/403/")
    def post(self, request, format=None):
        try:
            database = DataBase_Redis_Server_Config.objects.create(**request.data)
        except Exception as ex:
            return Response({"msg":str(ex)}, status=status.HTTP_400_BAD_REQUEST)      
        try:  
            snippet = DataBase_Redis_Server_Config.objects.get(id=database.id)
            serializer = serializers.RedisServerSerializer(snippet)
        except DataBase_Redis_Server_Config.DoesNotExist:
            logger.error(msg="添加数据库失败: {ex}".format(ex=str(ex)))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        return Response(serializer.data)     
    

class REDIS_SERVER_DETAIL(APIView,RedisConfig):
    
    def get_object(self, pk):
        try:
            return DataBase_Redis_Server_Config.objects.get(id=pk)
        except DataBase_Redis_Server_Config.DoesNotExist:
            raise Http404    
    
    @method_decorator_adaptor(permission_required, "databases.database_read_redis_server_config","/403/")     
    def get(self,request,pk,format=None):
        snippet = self.get_object(pk)
        try:  
            snippets = Database_Redis_Detail.objects.filter(db_server=snippet)
            serializer = serializers.RedisSerializer(snippets, many=True)
        except  Database_Redis_Detail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data) 
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_redis_server_config","/403/")
    def post(self, request, pk, format=None):
        dbServer = self.get_object(pk)
        snippets = self.sync_db(dbServer)
        serializer = serializers.RedisSerializer(snippets, many=True)
        return Response(serializer.data)    

@api_view(['GET','PUT', 'DELETE'])
def db_server_db_detail(request, sid, id,format=None):
    try:
        db_server = DataBase_Redis_Server_Config.objects.get(id=sid)
    except DataBase_Redis_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        snippet = Database_Redis_Detail.objects.get(id=id,db_server=db_server)
    except Database_Redis_Detail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    
    if request.method == 'GET':
        serializer = serializers.RedisSerializer(snippet)
        return Response(serializer.data) 

    elif  request.method == 'PUT':
        if not request.user.has_perm('databases.database_change_add_redis_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)          
        serializer = serializers.RedisSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.has_perm('databases.database_change_add_redis_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        Database_Table_Detail_Record.objects.filter(db=id).delete() #删除数据库关联表记录
        Database_Redis_User.objects.filter(db=snippet.id).delete() #删除用户关联数据库记录
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 


class REDIS_USER_REDIS_LIST(APIView,RedisUser):
    
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

class REDIS_USER_DB(APIView,RedisUser):
    
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


class REDIS_USER_SERVER_DBLIST(APIView,RedisUser):
    
    def get_db_server(self, sid):
        try:
            return DataBase_Redis_Server_Config.objects.get(id=sid)
        except DataBase_Redis_Server_Config.DoesNotExist:
            raise Http404  
    
    def get_user(self,uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            raise Http404      
    
    @method_decorator_adaptor(permission_required, "databases.database_can_read_redis_server_config","/403/")    
    def get(self, request, uid, sid, format=None):   
        return Response(self.get_server_all_db(self.get_db_server(sid), self.get_user(uid)))
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_redis_server_config","/403/") 
    def post(self, request, uid, sid, format=None):
        
        db_server, user = self.get_db_server(sid), self.get_user(uid) 
        
        self.update_user_server_db(request, db_server, user)
        
        return Response(self.get_user_server_db(db_server, user), status=status.HTTP_201_CREATED)        
    
    @method_decorator_adaptor(permission_required, "databases.database_can_delete_redis_server_config","/403/")     
    def delete(self, request, uid, sid, format=None):
        Database_Redis_User.objects.filter(id=QueryDict(request.body).get("user_db_id")).delete()
        return Response(self.get_user_server_db(self.get_db_server(sid), self.get_user(uid)))        
                
   
    
class REDIS_USER_SERVER_DBCMDS(APIView,RedisUser):
    
    def get_db(self,uid ,did):
        try:
            return  Database_Redis_User.objects.get(db=did,user=uid)
        except Database_Redis_User.DoesNotExist:
            raise Http404  
    
    def get_user(self,uid):
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            raise Http404          
        
    @method_decorator_adaptor(permission_required, "databases.database_can_read_redis_server_config","/403/")    
    def get(self, request, uid, did, format=None):   
        return Response(self.get_user_db_sql(self.get_db(uid, did)))    
    
    @method_decorator_adaptor(permission_required, "databases.database_can_add_redis_server_config","/403/") 
    def post(self, request, uid, did, format=None):  
        
        user_db = self.get_db(uid, did)
        print(request.data.getlist('cmds'))
        try:
            user_db.cmds = ",".join(request.data.getlist('cmds'))
            user_db.save()
        except Exception as ex:
            return  Response(str(ex), status=status.HTTP_400_BAD_REQUEST)        
          
        return Response(self.get_user_db_sql(self.get_db(uid, did)))       