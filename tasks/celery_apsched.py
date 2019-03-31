#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from utils.notice import Notice

@task 
def apsched_notice(**kwargs):
    print(kwargs)
    print(kwargs.get("jobs").notice_type)
    notice = Notice(kwargs.get("jobs").notice_type)
    notice.send(**kwargs)
    