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
from django.http import JsonResponse
from django_celery_beat.models  import CrontabSchedule,IntervalSchedule,PeriodicTask
from django_celery_results.models import TaskResult

@api_view(['GET', 'POST' ])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_crontab_list(request,format=None):  
    if request.method == 'GET':     
        snippets = CrontabSchedule.objects.all()
        serializer = serializers.TaskCrontabSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.TaskCrontabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_crontab_detail(request, id,format=None):  
    try:
        snippet = CrontabSchedule.objects.get(id=id)
    except CrontabSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.TaskCrontabSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.TaskCrontabSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
@api_view(['GET', 'POST' ])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_intervals_list(request,format=None):  
    if request.method == 'GET':     
        snippets = IntervalSchedule.objects.all()
        serializer = serializers.TaskIntervalsSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.TaskIntervalsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_intervals_detail(request, id,format=None):  
    try:
        snippet = IntervalSchedule.objects.get(id=id)
    except IntervalSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.TaskIntervalsSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.TaskIntervalsSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
@api_view(['GET', 'POST' ])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_task_list(request,format=None):  
    if request.method == 'GET':     
        snippets = PeriodicTask.objects.all()
        serializer = serializers.PeriodicTaskSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = serializers.PeriodicTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('djcelery.change_periodictask',raise_exception=True)
def celery_task_detail(request, id,format=None):  
    try:
        snippet = PeriodicTask.objects.get(id=id)
    except PeriodicTask.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = serializers.PeriodicTaskSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = serializers.PeriodicTaskSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       