#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
import random
from api import serializers
from cicd.models import *
from rest_framework import status
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from utils.logger import logger
from rest_framework.views import  APIView,Response
from rest_framework.pagination import CursorPagination
from dao.assets import AssetsBase
from dao.cicd import AppsManage
from utils import base

class AssetsMonitor(APIView,AssetsBase):
    
    def allowcator(self,sub,args,kwagrs):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args,kwagrs)
        else:       
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def ramdom_value(self,request):
        dataList = []
        for key in base.get_date_list(request.query_params.get('startTime'),
                                      request.query_params.get('endtime'),
                                      '%Y%m%d%H%M'):
            data = {}
            key = key[-4:-2] + ':' +key[-2:]
            data['dtime'] = key 
            data['value'] = random.randint(1,100)
            dataList.append(data)
        return dataList
    
    def ramdom_values(self,request,keyOne,keyTwo):
        dataList = []
        for key in base.get_date_list(request.query_params.get('startTime'),
                                      request.query_params.get('endtime'),
                                      '%Y%m%d%H%M'):
            data = {}
            key = key[-4:-2] + ':' +key[-2:]
            data['dtime'] = key 
            data[keyOne] = random.randint(1,500)
            data[keyTwo] = random.randint(1,500)
            dataList.append(data)
        return dataList    
            
            
    def mem(self,request, kwagrs):
#         assets = self.assets(id=kwagrs.get('id'))
        return Response(self.ramdom_value(request))    
    
    def cpu(self,request, kwagrs):
#         assets = self.assets(id=kwagrs.get('id'))
        return Response(self.ramdom_value(request)) 
    
    def disk(self,request, kwagrs):
        return Response(self.ramdom_values(request,'read','write')) 
    
    def taffic(self,request, kwagrs):
        return Response(self.ramdom_values(request,'in','out'))     
    
    def get(self,request,*args,**kwargs):
#         print(kwargs)
        return self.allowcator(sub=request.GET.get('type','mem'), args=request,kwagrs=kwargs)
    
    
class AppsMonitor(APIView,AppsManage):
    
    def allowcator(self,sub,args,kwagrs):
        if hasattr(self,sub):
            func= getattr(self,sub)
            return func(args,kwagrs)
        else:       
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def ramdom_value(self,request):
        dataList = []
        for key in base.get_date_list(request.query_params.get('startTime'),
                                      request.query_params.get('endtime'),
                                      '%Y%m%d%H%M'):
            data = {}
            key = key[-4:-2] + ':' +key[-2:]
            data['dtime'] = key 
            data['value'] = random.randint(1,100)
            dataList.append(data)
        return dataList
    
    def ramdom_values(self,request,keyOne,keyTwo):
        dataList = []
        for key in base.get_date_list(request.query_params.get('startTime'),
                                      request.query_params.get('endtime'),
                                      '%Y%m%d%H%M'):
            data = {}
            key = key[-4:-2] + ':' +key[-2:]
            data['dtime'] = key 
            data[keyOne] = random.randint(1,500)
            data[keyTwo] = random.randint(1,500)
            dataList.append(data)
        return dataList    
            
            
    def mem(self,request, kwagrs):
#         assets = self.get_apps(id=kwagrs.get('id'))
        return Response(self.ramdom_value(request))    
    
    def cpu(self,request, kwagrs):
#         assets = self.get_apps(id=kwagrs.get('id'))
        return Response(self.ramdom_value(request)) 
    
    def disk(self,request, kwagrs):
        return Response(self.ramdom_values(request,'read','write')) 
    
    def taffic(self,request, kwagrs):
        return Response(self.ramdom_values(request,'in','out'))     
    
    def qps(self,request, kwagrs):
        return Response(self.ramdom_value(request))  
    
    def http_error(self,request, kwagrs):
        return Response(self.ramdom_value(request))     
    
    def get(self,request,*args,**kwargs):
        return self.allowcator(sub=request.GET.get('type','mem'), args=request,kwagrs=kwargs)    