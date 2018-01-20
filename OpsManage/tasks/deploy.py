#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from OpsManage.utils import base
from OpsManage.models import (Project_Order,Log_Project_Config,Global_Config,Email_Config,)
from django.contrib.auth.models import User


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
def sendDeployEmail(order_id,mask):
    try:
        config = Email_Config.objects.get(id=1)
        order = Project_Order.objects.get(id=order_id)
    except:
        return False
    content = """申请人：{user}<br>                                          
                                         更新内容：{content}<br>
                                        工单地址：<a href='{site}/deploy_order/status/{order_id}/'>点击查看工单</a><br>
                                        授权人：{auth}<br>""".format(order_id=order_id,user=order.order_user,
                                           site=config.site,auth=order.order_audit,
                                           content=order.order_content)
    if order.order_cancel:
        content += "撤销原因：<strong>{order_cancel}</strong>".format(order_cancel=order.order_cancel)
    to_user = User.objects.get(username=order.order_audit).email
    if config.subject:subject = "{sub} {oub} {mask}".format(sub=config.subject,oub=order.order_subject,mask=mask)
    else:subject = "{oub} {mask}".format(mask=mask,oub=order.order_subject)
    if config.cc_user:
        cc_to = config.cc_user
    else:cc_to = None
    base.sendEmail(e_from=config.user,e_to=to_user,cc_to=cc_to,
                   e_host=config.host,e_passwd=config.passwd,
                   e_sub=subject,e_content=content)
    return True