#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json
from celery import task
from OpsManage.utils import base
from OpsManage.models import (Global_Config,Email_Config,
                              SQL_Execute_Histroy,SQL_Audit_Control)
from orders.models import Order_System
from django.contrib.auth.models import User
from channels import Group as CGroups

@task  
def recordSQL(exe_user,exe_db,exe_sql,exec_status,exe_result=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.sql == 1:
            SQL_Execute_Histroy.objects.create(
                                      exe_user = exe_user,
                                      exe_db = exe_db,
                                      exe_sql = exe_sql,
                                      exec_status = exec_status,
                                      exe_result = exe_result
                                      )
        return True
    except Exception,e:
        print e
        return False 
    
@task  
def sendOrderNotice(order_id,mask):
    try:
        email_config = Email_Config.objects.get(id=1)
    except:
        return '请配置邮件通知'
    try:        
        order = Order_System.objects.get(id=order_id)
    except:
        return '工单信息获取失败'
    try:
        sql_config = SQL_Audit_Control.objects.get(id=1)
    except:
        return '请先sql工单审核配置项'
    try:
        group_config = Global_Config.objects.get(id=1)
    except:
        return '请检查全局配置'
    if order.order_type == 1:
        order_type = '代码部署'
        order_content = order.project_order.order_content
        order_url = "/deploy_order/status/{order_id}/".format(order_id=order_id)
    else:
        order_type = 'SQL更新'
        order_content = order_content = str(order.sql_audit_order.order_sql).replace(';',';<br>')
        order_url = "/db/sql/order/run/{order_id}/".format(order_id=order_id)
    content = """<strong>申请人：</strong>{user}<br> 
                 <strong>工单类型：</strong>{order_type}<br>
                 <strong>更新内容：</strong><br>{order_content}<br>
                 <strong>工单地址：</strong><a href='{site}{order_url}'>点击查看工单</a><br>
                 <strong> 授权人：</strong>{auth}<br>
                 <strong>状态：</strong>{mask}<br>""".format(order_id=order_id,user=User.objects.get(id=order.order_user).username,
                                                          site=email_config.site,auth=User.objects.get(id=order.order_executor).username,
                                                          order_content=order_content,mask=mask,order_type=order_type,
                                                          order_url=order_url)
    try:
        to_user = User.objects.get(id=order.order_executor)
    except Exception, ex:
        return ex
    if order.order_status == 1:to_username = User.objects.get(id=order.order_executor).username
    else:to_username = User.objects.get(id=order.order_user).username
    #判断是否开启了部署通知
    if group_config.email == 1:CGroups(to_username).send({'text': json.dumps({"title":"你有一条新的工单需要处理<br>","type":"info","messages":content})})
    if order.order_cancel:
        content += "<strong>撤销原因：</strong>{order_cancel}".format(order_cancel=order.order_cancel)
    if email_config.subject:subject = "{sub} {oub} {mask}".format(sub=email_config.subject,oub=order.order_subject,mask=mask)
    else:subject = "{oub} {mask}".format(mask=mask,oub=order.order_subject)
    if email_config.cc_user:
        cc_to = email_config.cc_user
    else:cc_to = None
    if order.order_type==1 and group_config.email == 1:#如果是代码部署并且全局配置开启了邮件通知
        base.sendEmail(e_from=email_config.user,e_to=to_user.email,cc_to=cc_to,
                       e_host=email_config.host,e_passwd=email_config.passwd,
                       e_sub=subject,e_content=content)  
    elif order.order_type==0 and group_config.sql == 1:#如果是SQL部署并且全局配置开启了邮件通知      
        if sql_config.t_email == 1 and order.sql_audit_order.order_db.db_env == 'test': 
            base.sendEmail(e_from=email_config.user,e_to=to_user.email,cc_to=cc_to,
                           e_host=email_config.host,e_passwd=email_config.passwd,
                           e_sub=subject,e_content=content)
        elif sql_config.p_email == 1 and order.sql_audit_order.order_db.db_env == 'prod':
            base.sendEmail(e_from=email_config.user,e_to=to_user.email,cc_to=cc_to,
                           e_host=email_config.host,e_passwd=email_config.passwd,
                           e_sub=subject,e_content=content) 
    else:
        return  '请在全局配置开启相关邮件通知'        