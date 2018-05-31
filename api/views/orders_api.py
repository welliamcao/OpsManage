#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api import serializers
from OpsManage.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from OpsManage.tasks.sql import sendOrderNotice
from orders.models import Order_System



@api_view(['PUT', 'DELETE'])
@permission_required('orders.can_change_order_systemr',raise_exception=True)
def order_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Order_System.objects.get(id=id)
    except Order_System.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        if int(request.data.get('order_status')) == 7:
            sendOrderNotice.delay(id,mask='【已取消】')  
        elif int(request.data.get('order_status')) == 8:
            sendOrderNotice.delay(id,mask='【已授权】')  
        elif int(request.data.get('order_status')) == 3:
            sendOrderNotice.delay(id,mask='【已部署】')         
        serializer = serializers.OrderSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_order_system'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 