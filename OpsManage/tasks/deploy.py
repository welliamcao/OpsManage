#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json
from celery import task
from OpsManage.utils import base
from OpsManage.models import (Project_Order,Log_Project_Config,Global_Config,Email_Config,)
from django.contrib.auth.models import User
from channels import Group as CGroups

@task  
def recordProject(project_user,project_id,project_name,project_content,project_branch=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.project == 1:
            Log_Project_Config.objects.create(
                                      project_id = project_id,
                                      project_user = project_user,
                                      project_name = project_name,
                                      project_content = project_content,
                                      project_branch = project_branch
                                      )
        return True
    except Exception,e:
        print e
        return False
    
    
@task  
def sendDeployNotice(order_id,mask):
    try:
        config = Email_Config.objects.get(id=1)
        order = Project_Order.objects.get(id=order_id)
    except:
        return False
    content = """<strong>申请人：</strong>{user}<br>                                          
            <strong>更新内容：</strong>{content}<br>
            <strong>工单地址：</strong><a href='{site}/deploy_order/status/{order_id}/'>点击查看工单详情</a><br>
            <strong>授权人：</strong>{auth}<br>
            <strong>状态：</strong>{mask}<br>""".format(order_id=order_id,user=order.order_user,
                                                     site=config.site,auth=order.order_audit,
                                                     content=order.order_content,mask=mask)
    if order.order_status == 2:to_user = order.order_audit
    else: to_user = order.order_user
    CGroups(to_user).send({'text': json.dumps({"title":"你有一条新的工单需要处理<br>","type":"info","messages":content})})
    if order.order_cancel:
        content += "撤销原因：<strong>{order_cancel}</strong>".format(order_cancel=order.order_cancel)
    to_user = User.objects.get(username=to_user).email
    if config.subject:subject = "{sub} {oub} {mask}".format(sub=config.subject,oub=order.order_subject,mask=mask)
    else:subject = "{oub} {mask}".format(mask=mask,oub=order.order_subject)
    if config.cc_user:
        cc_to = config.cc_user
    else:cc_to = None
    base.sendEmail(e_from=config.user,e_to=to_user,cc_to=cc_to,
                   e_host=config.host,e_passwd=config.passwd,
                   e_sub=subject,e_content=content)
    return True