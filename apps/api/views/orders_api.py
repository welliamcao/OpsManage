#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from django.db.models import Q
from rest_framework import viewsets,permissions
from api import serializers
from orders.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from orders.models import Order_System
from dao.orders import ORDERS_COUNT_RBT
from django.http import JsonResponse


@api_view(['PUT', 'DELETE'])
@permission_required('orders.orders_change_order_system',raise_exception=True)
def order_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Order_System.objects.get(id=id)
    except Order_System.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':           
        serializer = serializers.OrderSerializer(snippet, data=request.data)
        if request.user.is_superuser or request.user.id == serializer.order_executor: 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('orders.orders_delete_order_system'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
@api_view(['GET'])
def order_count(request,format=None):
    return JsonResponse({"code":200,"msg":"success","data":{"orderCount":ORDERS_COUNT_RBT.month_orders(),
                                                            "sqlOrder":ORDERS_COUNT_RBT.sql_orders(),
                                                            "uploadOrder":ORDERS_COUNT_RBT.upload_orders(),
                                                            "downloadOrder":ORDERS_COUNT_RBT.download_orders(),
                                                           }})      
    


class OrdersPaginator(APIView):

    def get(self,request,*args,**kwargs):
        if request.user.is_superuser:
            ordersList = Order_System.objects.all().order_by("-id")
        else:
            ordersList = Order_System.objects.filter(Q(order_user=request.user.id) | Q(order_executor=request.user.id)).order_by("-id")
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=ordersList, request=request, view=self)
        ser = serializers.OrderSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data)
    


    
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