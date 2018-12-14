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

@api_view(['GET', 'POST' ])
@permission_required('OpsManage.can_read_gameserver_config',raise_exception=True)
def details(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':
        snippets = GameServer_Config.objects.all()
        serializer = serializers.GameServerSerializer(snippets,many=True)
        return Response(serializer.data)

@permission_required('OpsManage.can_read_gameserver_config',raise_exception=True)
def showid(request,format=None):
    if request.method == 'GET':
        idlist={}
        ids = GameServer_Update_List.objects.all().values("listid","orderid")
        if ids:
            for id in ids:
                idlist[id["listid"]].append(id["orderid"])
        return Response(data=idlist)


