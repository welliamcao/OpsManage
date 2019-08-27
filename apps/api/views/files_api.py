#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api import serializers
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from filemanage.models import *

@api_view(['GET', 'POST' ])
@permission_required('filemanage.can_read_fileupload_audit_order',raise_exception=True)
def upload_file_list(request,format=None):  
    if request.method == 'GET':     
        snippets = FileUpload_Audit_Order.objects.all()
        serializer = serializers.UploadFilesOrderSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.UploadFilesOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('filemanage.can_change_fileupload_audit_order',raise_exception=True)
def upload_file_detail(request, id,format=None):  
    try:
        snippet = FileUpload_Audit_Order.objects.get(id=id)
    except FileUpload_Audit_Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.UploadFilesOrderSerializer(snippet)
        return Response(serializer.data)
    
    
@api_view(['GET', 'POST' ])
@permission_required('filemanage.can_add_filedownload_audit_order',raise_exception=True)
def download_file_list(request,format=None):  
    if request.method == 'GET':     
        snippets = FileDownload_Audit_Order.objects.all()
        serializer = serializers.DownloadFilesSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.DownloadFilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('filemanage.can_read_filedownload_audit_order',raise_exception=True)
def download_file_detail(request, id,format=None):  
    try:
        snippet = FileDownload_Audit_Order.objects.get(id=id)
    except FileDownload_Audit_Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.DownloadFilesSerializer(snippet)
        return Response(serializer.data)    