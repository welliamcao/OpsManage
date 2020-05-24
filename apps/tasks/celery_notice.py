#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from celery import task
from libs.notice import Notice

@task
def apsched_notice(jobs, jobLogs):
    status = "失败"
    
    if jobLogs.get("status") == 0:status = "成功"
    
    message = """<strong>节点: </strong> {job_node}<br>
                 <strong>命令: </strong> {job_cmd}<br>
                 <strong>执行结果: </strong> {result}<br>
                 <strong>执行状态: </strong> {status}""".format(job_node=jobs.get("job_node"),job_cmd=jobs.get("job_cmd"),
                                                                                                          result=jobLogs.get("result"), status=status)

    if jobs.get("notice_type") == 0:    
        message = {
                "e_content":message,
                "e_sub":"[OpsManage-任务通知] {job_name}".format(job_name=jobs.get("job_name")),
                "e_to":jobs.get("notice_number")
            }
        
    Notice(jobs.get("notice_type")).send(**message) 

