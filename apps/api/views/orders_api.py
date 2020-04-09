#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import time
from django.db.models import Q
from api import serializers
from orders.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from orders.models import Order_System
from dao.orders import ORDERS_COUNT_RBT,OrderBase
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from utils import base

class OrderDetail(APIView,OrderBase):
    
    def get_object(self, pk):
        try:
            return Order_System.objects.get(id=pk)
        except Order_System.DoesNotExist:
            raise Http404          

    def check_perms(self, request, pk):
        order = self.get_object(pk)

        if request.user.is_superuser:
            return order
        
#         if order.is_expired() and order.is_unexpired():  
              
        if request.user.id == order.order_user or request.user.id == order.order_executor:
            return order  
        
        raise PermissionDenied()        
    
    def check_update_content_perms(self, request, order):
        #如果工单审核状态不是审核中，-直接返回403不可编辑
        if order.order_audit_status !=2: raise PermissionDenied()        
        
        #如果工单进度状态不是，提交或者处理中状态-直接返回403不可编辑
        if order.order_execute_status not in [0,1]: raise PermissionDenied()
        
        #如果工单未到期或者已经过期-直接返回403
        if order.is_expired() and order.is_unexpired(): raise PermissionDenied()
        
        #如果工单申请人不是自己-直接返回403
        if request.user.id == order.order_user: raise PermissionDenied() 
                    
        
        
    def get(self, request, pk, *args, **kwargs):
        
        order = self.check_perms(request, pk)
       
        return Response(self.order_detail(order))
        
    def put(self, request, pk, *args, **kwargs): 
        
        order_mark = None
        
        order = self.get_object(pk)
        
        data = request.data.copy()

        if "order_audit_status" in data.keys():
            data = self.update_order_progress(data)
        
        if "order_mark" in data.keys():
            order_mark = data.get("order_mark")
        
        if "order_content"  in data.keys():#更新工单内容
            
            self.check_update_content_perms(request, order)  
                
            if hasattr(order, 'service_audit_order'):
                
                order.service_audit_order.order_content = data.get("order_content")
                order.service_audit_order.save()
                
                self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, data.get("order_content"))
                
                return Response(order.to_json())
        else:#更新工单审核状体或者工单进度
            
            serializer = serializers.OrderSerializer(order, data=data)

            if request.user.is_superuser or request.user.id == order.order_executor: 
                if serializer.is_valid():
                    serializer.save()
                    self.record_order_operation(order.id, order.order_audit_status, order.order_execute_status, request.user, order_mark)
                    return Response(serializer.data)            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderLogsDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Order_System.objects.get(id=pk)
        except Order_System.DoesNotExist:
            raise Http404   
        
    def get(self, request, pk, *args, **kwargs):
        order = self.get_object(pk)
        
        if request.user.is_superuser or request.user.id == order.order_user or request.user.id == order.order_executor:
            return Response([ ds.to_json() for ds in OrderLog.objects.filter(order=order.id).order_by("-id") ])
                
        return Response(status=status.HTTP_403_FORBIDDEN) 
    
@api_view(['GET'])
def order_count(request,format=None):
    return JsonResponse({"code":200,"msg":"success","data":{"orderCount":ORDERS_COUNT_RBT.month_orders(),
                                                            "sqlOrder":ORDERS_COUNT_RBT.sql_orders(),
                                                            "uploadOrder":ORDERS_COUNT_RBT.upload_orders(),
                                                            "downloadOrder":ORDERS_COUNT_RBT.download_orders(),
                                                           }})      
    


class OrdersPaginator(APIView):

    def get(self, request, *args, **kwargs):
        
        if request.user.is_superuser:
            ordersList = Order_System.objects.all().order_by("-id")
        else:
            ordersList = Order_System.objects.filter(Q(order_user=request.user.id) | Q(order_executor=request.user.id)).order_by("-id")
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=ordersList, request=request, view=self)
        ser = serializers.OrderSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)
    
    def post(self,  request, *args, **kwargs):
        
        query_params = dict()
        for ds in request.POST.keys():
            query_params[ds] = request.POST.get(ds) 
            
        if not request.user.is_superuser:#普通用户只能查询自己的工单
            if "order_user"  in query_params.keys() and "order_executor" in query_params.keys():
                query_params["order_user"] = request.user.id
                query_params["order_executor"] = request.user.id
                
            elif "order_user" in query_params.keys():    
                query_params["order_user"] = request.user.id
                
            elif "order_executor" in query_params.keys():    
                query_params["order_executor"] = request.user.id
                
            else:
                query_params["order_user"] = request.user.id 
                query_params["order_executor"] = request.user.id               

        if "order_time" in query_params.keys(): 
            try:
                order_time = query_params.get('order_time').split(' - ')
                query_params.pop('order_time')
                query_params['create_time__gte'] = order_time[0] 
                query_params['create_time__lte'] = order_time[1]
            except:
                pass
       
        if "order_expire" in query_params.keys(): 
            ctime = base.changeTimestampTodatetime(int(time.time()))
            
            if str(query_params.get('order_expire')) == "1":
                query_params['end_time__gte'] = ctime
                query_params['start_time__lte'] = ctime
                
            elif str(query_params.get('order_expire')) == "2":
                query_params['start_time__gte'] = ctime
                
            else:
                query_params['end_time__lte'] = ctime
                
            query_params.pop('order_expire')
            
        order_lists = Order_System.objects.filter(**query_params).order_by("-id")[:1000]  
        serializer = serializers.OrderSerializer(order_lists, many=True)
        return Response(serializer.data)          


    
@api_view(['GET', 'POST' ])
# @permission_required('orders.orders_read_notice_config',raise_exception=True)
def notice_config(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        if request.query_params.get('order_type'):
            snippets = Order_Notice_Config.objects.filter(order_type=request.query_params.get('order_type'))
        else:snippets = Order_Notice_Config.objects.all()
        serializer = serializers.OrdersNoticeConfigSerializer(snippets, many=True)
        return Response(serializer.data) 
        
    elif request.method == 'POST':
        if not request.user.has_perm('orders.orders_add_notice_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            count = Order_Notice_Config.objects.filter(order_type=request.data.get("order_type")).count()
        except Exception as ex:
            pass
        if count == 0:
            serializer = serializers.OrdersNoticeConfigSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        else:
            return Response("每一种工单只能有一种通知类型,请修改或者删除旧数据", status=status.HTTP_400_BAD_REQUEST)  
        
        
@api_view(['GET','PUT', 'DELETE'])
@permission_required('orders.orders_read_notice_config',raise_exception=True)
def notice_config_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Order_Notice_Config.objects.get(id=id)
    except Order_Notice_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        try:  
            snippet = Order_Notice_Config.objects.get(id=id)
            serializer = serializers.OrdersNoticeConfigSerializer(snippet)
        except  Order_Notice_Config.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        return Response(serializer.data)     
    
    elif request.method == 'PUT': 
        if not request.user.has_perm('orders.orders_change_notice_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)                 
        serializer = serializers.OrdersNoticeConfigSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('orders.orders_delete_notice_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)              