#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api.serializers import  TagSerializer,CategorySerializer,PostSerializer
from wiki.models import Category,Tag,Post
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required

@api_view(['GET', 'POST' ])
@permission_required('wiki.wiki_can_add_wiki_tag',raise_exception=True)
def tag_list(request,format=None):
    if request.method == 'GET':      
        snippets = Tag.objects.all()
        serializer = TagSerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('wiki.wiki_can_change_wiki_tag',raise_exception=True)
def tag_detail(request, id,format=None):
    try:
        snippet = Tag.objects.get(id=id)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = TagSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = TagSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('wiki.wiki_can_delete_wiki_tag'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
@api_view(['GET', 'POST' ])
@permission_required('wiki.wiki_can_add_wiki_category',raise_exception=True)
def category_list(request,format=None):
    if request.method == 'GET':      
        snippets = Category.objects.all()
        serializer = CategorySerializer(snippets, many=True)
        return Response(serializer.data)     
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('wiki.wiki_can_change_wiki_category',raise_exception=True)
def category_detail(request, id,format=None):
    try:
        snippet = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = CategorySerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = CategorySerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('wiki.wiki_can_delete_wiki_category'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_required('wiki.wiki_can_delete_wiki_post',raise_exception=True)
def archive_detail(request, id,format=None):
    try:
        snippet = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'GET':
        serializer = PostSerializer(snippet)
        return Response(serializer.data)
 
    elif request.method == 'PUT':
        serializer = PostSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('wiki.wiki_can_delete_wiki_post'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      