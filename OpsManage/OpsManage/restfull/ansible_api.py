#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from OpsManage.serializers import *
from OpsManage.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required

@api_view(['GET', 'POST' ])
@permission_required('Opsmanage.can_read_ansible_playbook',raise_exception=True)
def playbook_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Ansible_Playbook.objects.all()
        serializer = AnbiblePlaybookSerializer(snippets, many=True)
        return Response(serializer.data)  
#     elif request.method == 'POST':
#         serializer = ProjectConfigSerializer(data=request.data)
#         
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('Opsmanage.can_delete_ansible_playbook',raise_exception=True)
def playbook_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Ansible_Playbook.objects.get(id=id)
    except Ansible_Playbook.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = AnbiblePlaybookSerializer(snippet)
        return Response(serializer.data)
 
#     elif request.method == 'PUT':
#         serializer = ProjectConfigSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_ansible_playbook'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 