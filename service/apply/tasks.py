#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os, threading, time, json
from multiprocessing import Process
import subprocess, signal
from utils.logger import logger
from dao.apply import ApplyTaskManager
from libs.ansible.runner import ANSRunner
from OpsManage.settings import _deploy_tasks
from dao.assets import AssetsSource
from utils.base import changeTotimestamp


# signal.signal(signal.SIGCHLD, signal.SIG_IGN) #设置全局父进程忽略子进程退出信号，以免杀掉子进程之后而变成僵尸进程

def startup_apply_tasks():
    logger.info('----------------------- startup deploy task -----------------------')
    task_thread = ApplyTaskManagerThread()
    task_thread.daemon = True
    task_thread.start()

class ApplyTaskProcess(Process):
    def __init__(self, deploy_task):
        super(ApplyTaskProcess, self).__init__()
        self.deploy_task = deploy_task
        self.deplytask = self.deploy_task.get('deplytask')
        self.ansible = ANSRunner(
                                    hosts=self.deploy_task.get('resource'),
                                    deplytask=self.deplytask
                                )
   
#     def teminate(self):         
#         try:
#             self._kill_childs()
#         except Exception as ex:
#             pass
#         Process.terminate(self)
#         os.waitpid(self.pid,0) #杀掉子进程之后，调用操作系统api获取子进程的退出码，以免被当做僵尸进程
   
    def _get_childs(self, parent_id=None):
        if parent_id is None:
            parent_id = self.pid
        if parent_id is None:
            return []
        ps_command = subprocess.Popen(["ps", "-o", "pid", "--ppid", str(parent_id), "--noheaders"],
                                      stdout=subprocess.PIPE)
        ps_command.wait()
        ps_output = str(ps_command.stdout.read().decode('utf-8').strip())
        if len(ps_output) > 0:
            childs = ps_output.split("\n")
            if childs:
                res = childs
                for child in childs:
                    if int(child) not in res:
                        res.extend(self._get_childs(int(child)))
                return res
            else:
                return childs
        return []
   
    def _kill_childs(self,parent_id=None):
        for pid_str in self._get_childs(parent_id=None):
            try:
                os.kill(int(pid_str), signal.SIGHUP) #发送退出信号
            except Exception as ex:
                pass      
   
   
    def launch_playbook(self):
        self.ansible.run_playbook(host_list=self.deploy_task.get('host_list'),
                                        playbook_path=self.deploy_task.get('playbook_path',''),
                                        extra_vars=self.deploy_task.get('extra_vars',{}))

           
    def launch_model(self):
        self.ansible.run_model(host_list=self.deploy_task.get('host_list'), module_name=self.deploy_task.get('module_name'), module_args=self.deploy_task.get('module_args'))

   
    def run(self):
        try:
            if self.deploy_task.get('task_type') == 'playbook':
                self.launch_playbook()
            else:
                self.launch_model()
        except Exception as ex:
            logger.error(ex)
            self.deplytask.status = 'failed'
            self.deplytask.error_msg = ex
            self.deplytask.save()                
        finally:
            self._kill_childs()  
            


class ApplyTaskManagerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.task_manager = ApplyTaskManager()


    def get_payload(self,deploy_task):
        assets_source = AssetsSource()
        try:
            task_info = deploy_task.to_json()
            task_payload = json.loads(task_info.get('payload'))
        except Exception as ex:
            logger.error('get deploy task [{task_id}] payload failed: {ex}'.format(task_id=deploy_task.task_id,ex=str(ex)))
            return False
        
        try:    
            task_payload['host_list'], task_payload['resource'] = assets_source.queryAssetsByIp(task_payload.get('hosts'))
        except Exception as ex:
            logger.error('format deploy task [{task_id}] payload failed: {ex}'.format(task_id=deploy_task.task_id,ex=str(ex)))  
            return False
        
        del assets_source
        
        task_payload['task_type'] = deploy_task.deploy_type
        task_payload['deplytask'] = deploy_task
        
        return task_payload

    def run_task(self, deploy_task):
        task_id = deploy_task.task_id
        task_payload = self.get_payload(deploy_task)
        deploy_task_process = ApplyTaskProcess(task_payload)
        deploy_task_process.start()
        logger.info("start process run deploy task task_id:{task_id}, task_pid: {pid}".format(task_id=task_id, pid=deploy_task_process.pid))        
        self.task_manager.update_deploy_task_status(task_id, 'running')
        _deploy_tasks[task_id] = {'instance': deploy_task, 'process': deploy_task_process}
        
    def clean_task(self, deploy_task):
        if deploy_task.task_id in _deploy_tasks.keys():
            task_process = _deploy_tasks[deploy_task.task_id].get('process')
            task_process.terminate()
            if task_process.is_alive():  #判断进程是否存活，如果还存活就调用os模块，强制杀掉
                os.kill(task_process.pid, signal.SIGKILL)                    
            del _deploy_tasks[deploy_task.task_id] 
            logger.info("cleanup task task_name:{task_name} task_pid:{pid} task_id:{task_id} succeeded.".format(task_id=deploy_task.task_id, task_name=task_process.name, pid=task_process.pid))       
            

    def run(self):
        max_tasks = 10
        while True:
            current_time = int(time.time())
            task_queue_size = len(_deploy_tasks.keys())
            if task_queue_size >= max_tasks: 
                logger.warn("deploy task queue is full, waiting for other tasks finish")
                time.sleep(5)
                continue              
            
            #获取新创建的任务
            _ready_tasks =  self.task_manager.get_ready_deploy_task()
            if isinstance(_ready_tasks, str):
                logger.error('get ready deploy task failed: {ex}'.format(ex=_ready_tasks))
                continue

            for deploy_task in _ready_tasks:
                #判断任务是否过期，暂时设置超过1天，防止队列满了阻塞了其他提交未执行的任务
                create_time = changeTotimestamp(deploy_task.to_json().get('create_time'))
                if current_time - create_time > 3600:
                    try:
                        deploy_task.status = 'expired'
                        deploy_task.save()
                        logger.info("task {task_id} expired and not executing".format(deploy_task.task_id))
                    except Exception as ex:
                        logger.error(str(ex))
                    continue
                #如果队列超过10个任务就跳过    
                task_count = 0
                if task_count > max_tasks:
                    logger.warn("deploy task queue is full, waiting for other tasks finish")        
                    continue  
                #如果任务不在全局配置就添加任务              
                if deploy_task.task_id not in _deploy_tasks.keys():
                    self.run_task(deploy_task)
                    task_count = task_count + 1
                    time.sleep(0.1)
                else:
                    logger.info("The deploy task [{task_id}] is still running. skip this task".format(task_id=deploy_task.task_id))     
            logger.info('there are {task_queue_size} tasks running in the task queue, wait 5 seconds to check for new tasks'.format(task_queue_size=task_queue_size))  
            time.sleep(5)
            
            #获取已经运行过的任务，从全局配置里面删除掉
            _not_ready_tasks =  self.task_manager.get_not_ready_deploy_task()
            if isinstance(_not_ready_tasks, str):
                logger.error('get not ready deploy task failed: {ex}'.format(ex=_not_ready_tasks))
                continue  
            
            for deploy_task in _not_ready_tasks:
                self.clean_task(deploy_task)
#                 if deploy_task.task_id in _deploy_tasks.keys():
#                     task_process = _deploy_tasks[deploy_task.task_id].get('process')
#                     task_process.terminate()
#                     if task_process.is_alive():  #判断进程是否存活，如果还存活就调用os模块，强制杀掉
#                         os.kill(task_process.pid, signal.SIGKILL)                    
#                     del _deploy_tasks[deploy_task.task_id]
                
                      
            