#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from api import serializers
from dao.apsched import ApschedNodeManage,ApschedNodeJobsManage,ApschedBase
from django.http import JsonResponse
from sched.models import *
from rest_framework import status
from django.http import Http404
from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.base import method_decorator_adaptor

@api_view(['GET', 'POST' ])
@permission_required('sched.cron_can_add_cron_config',raise_exception=True)
def node_list(request,format=None):
    """
    List all order, or create a server assets order.
    """
    if request.method == 'GET':      
        snippets = Sched_Node.objects.all()
        serializer = serializers.ApschedNodeSerializer(snippets, many=True)
        return Response(serializer.data)      


class ApschedCount(ApschedBase,APIView):
    def get(self,request,*args,**kwargs):
        return JsonResponse({"code":200,"data":{
                                                "allNodes":self.get_nodes_count(),
                                                "allJobs":self.get_jobs_count(),
                                                "jobsSucess":self.get_jobs_status_count(status=0),
                                                "jobsFalied":self.get_jobs_status_falied(),
                                                }})  

class ApschedNodeJobs(APIView):
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_read_cron_config","/403/")     
    def get(self,request,*args,**kwargs):
        query_params = dict()
        for ds in request.query_params.keys():
            query_params[ds] = request.query_params.get(ds)
        try:
            jobs_list = Sched_Job_Config.objects.filter(**query_params)
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=jobs_list, request=request, view=self)
        ser = serializers.ApschedNodeJobsSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data) 


class ApschedNodeJobsLogs(APIView):
    
    @method_decorator_adaptor(permission_required, "sched.cron_can_read_cron_config","/403/")        
    def get(self,request,*args,**kwargs):
        try:
            jobs = Sched_Job_Config.objects.get(id=request.query_params.get("id"))
        except Exception as ex:
            return Response(str(ex),status=status.HTTP_400_BAD_REQUEST)
        jobs_logs_list = Sched_Job_Logs.objects.filter(job_id=jobs)
        page = serializers.PageConfig()  # 注册分页
        page_user_list = page.paginate_queryset(queryset=jobs_logs_list, request=request, view=self)
        ser = serializers.ApschedNodeJobsLogsSerializer(instance=page_user_list, many=True)
        return page.get_paginated_response(ser.data) 
    

class ApschedNodeJobsQuery(ApschedNodeManage,View):

    @method_decorator(csrf_exempt)  
    def dispatch(self, request, *args, **kwargs):
        return super(ApschedNodeJobsQuery, self).dispatch(request, *args, **kwargs)
        
    def post(self,request, *args, **kwargs):
        return JsonResponse({"code":200,"data":self.get_node_jobs_by_token(request.POST.get('token'))})  
    
class ApschedNodeJobsRecord(ApschedNodeJobsManage,View):

    @method_decorator(csrf_exempt)  
    def dispatch(self, request, *args, **kwargs):
        return super(ApschedNodeJobsRecord, self).dispatch(request, *args, **kwargs)
        
    def post(self,request, *args, **kwargs):
        params = dict()
        for ds in request.POST.keys():
            params[ds] = request.POST.get(ds)     
        res = self.insert_jobs_logs_by_jid(params)
        if isinstance(res, str):
            return JsonResponse({"code":500,"msg":res,"data":{}})    
        else:
            return JsonResponse({"code":200,"msg":"push sucess","data":res})          