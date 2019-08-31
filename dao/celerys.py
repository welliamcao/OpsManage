#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django_celery_beat.models  import PeriodicTask,CrontabSchedule,IntervalSchedule
from django.contrib.auth.decorators import login_required
from celery import task
from celery.registry import tasks as cTasks
from celery import registry
from celery.task.control import revoke
from celery.five import keys, items

class CeleryTaskManage(object):
    def __init__(self):
        super(CeleryTaskManage, self).__init__()  
        
    def crontabList(self):
        return CrontabSchedule.objects.all().order_by("-id")
    
    def intervalList(self):
        return IntervalSchedule.objects.all().order_by("-id")
    
    def taskList(self):
        return PeriodicTask.objects.all().order_by("-id")
    
    def regTaskList(self):
        regTaskList = []
        for task in list(keys(cTasks)):
            if task.startswith('apps.tasks.celery_deploy') or task.startswith('apps.tasks.celery_sched'):
                regTaskList.append(task)
        return regTaskList
    
    def base(self):
        return {
                "crontabList":self.crontabList(),
                "intervalList":self.intervalList(),
                "taskList":self.taskList(),
                "regTaskList":self.regTaskList()
                }         