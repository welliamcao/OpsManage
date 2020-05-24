#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from libs.notice import Notice
from orders.models import Order_Notice_Config,Order_System,ORDER_AUDIT_STATUS_DICT,ORDER_EXECUTE_STATUS_DICT
from account.models import User, Structure
  
@task
def order_notice(order):
    try:
        order = Order_System.objects.get(id=order)
    except Exception as ex:
        print(ex)
        return {"status":"failed","msg":str(ex)}
    
    try:
        order_config = Order_Notice_Config.objects.get(order_type=order.order_type)
    except Exception as ex:
        print(ex)
        return {"status":"failed","msg":str(ex)}
    
    order_json = order.to_json()
    
    try:
        order_user = User.objects.get(id=order.order_user)
    except Exception as ex:
        return {"status":"failed","msg":str(ex)}

    try:
        order_executor = User.objects.get(id=order.order_executor)
    except Exception as ex:
        return {"status":"failed","msg":str(ex)}

    if order.order_type == 0:
        content = order.sql_audit_order.order_sql
        
    elif order.order_type == 1:
        content = order.service_audit_order.order_content

    elif order.order_type == 2:
        content = order.fileupload_audit_order.order_content   
        
    elif order.order_type == 3:
        content = order.filedownload_audit_order.order_content            

    message = """<strong>申请人: </strong> {order_user}<br>
                 <strong>主题: </strong> {order_subject}<br>
                 <strong>工单内容: </strong> {content}<br>
                 <strong>审核人: </strong> {order_executor}<br>
                 <strong>工单状态: </strong> {order_audit_status}<br>
                 <strong>工单进度: </strong> {order_execute_status}<br>
                 <strong>创建时间: </strong> {create_time}<br>
                 <strong>执行时间: </strong> {start_time} - {end_time}""".format(
                                                                                order_user = order_user.name,
                                                                                order_executor = order_executor.name,
                                                                                order_subject = order_json.get("order_subject"),
                                                                                content = content, 
                                                                                order_audit_status = ORDER_AUDIT_STATUS_DICT.get(str(order_json.get("order_audit_status"))),
                                                                                order_execute_status = ORDER_EXECUTE_STATUS_DICT.get(str(order_json.get("order_execute_status"))),
                                                                                start_time = order_json.get("start_time"),
                                                                                end_time = order_json.get("end_time"),
                                                                                create_time = order_json.get("create_time"),
                                                                            )


    if order_config.mode == 0:  
        
        if order_user.email and order_executor.email:
          
            message = {
                    "e_content":message,
                    "e_sub":"[OpsManage-工单通知] {order_subject}".format(order_subject = order_json.get("order_subject")),
                    "e_to":order_user.email,
                    "cc_to":order_executor.email
                }
        else:
            return {"status":"failed","msg":"未配置邮箱"}
   
    Notice(order_config.mode).send(**message) 