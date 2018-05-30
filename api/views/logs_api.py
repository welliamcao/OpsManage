#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from api import serializers
from OpsManage.models import *
from rest_framework import status
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST' ])
@permission_required('OpsManage.can_read_log_ansible_model',raise_exception=True)
def AnsibleModelLogsList(request,format=None):  
    if request.method == 'POST': 
        try:   
            snippets = Log_Ansible_Model.objects.filter(create_time__gte=request.data.get('startTime'),
                                                        create_time__lte=request.data.get('endTime'),
                                                        ).order_by("id")[:1000]
            serializer = serializers.AnsibleModelLogsSerializer(snippets, many=True)
        except Exception, ex:
            return ex
        if request.user.has_perm('delete_log_ansible_model'):
            return Response({"data":serializer.data,"perm":1})
        else:
            return Response({"data":serializer.data,"perm":0})
        
@api_view(['POST' ])
@permission_required('OpsManage.can_read_log_ansible_playbook',raise_exception=True)
def AnsiblePlayBookLogsList(request,format=None):  
    if request.method == 'POST': 
        try:   
            snippets = Log_Ansible_Playbook.objects.filter(create_time__gte=request.data.get('startTime'),
                                                        create_time__lte=request.data.get('endTime'),
                                                        ).order_by("id")[:1000]
            serializer = serializers.AnsiblePlaybookLogsSerializer(snippets, many=True)
        except Exception, ex:
            return ex
        if request.user.has_perm('can_delete_log_ansible_playbook'):
            return Response({"data":serializer.data,"perm":1})
        else:
            return Response({"data":serializer.data,"perm":0})