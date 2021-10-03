#!/usr/bin/env python
# -*- coding=utf-8 -*-
import json
from ansible.plugins.callback import CallbackBase
from dao.dispos import DeploySaveResult
from apply.models import Apply_Tasks_Result
from utils.logger import logger

class ModelResultsCollector(CallbackBase):  
  
    def __init__(self, *args, **kwargs):  
        super(ModelResultsCollector, self).__init__(*args, **kwargs)  
        self.host_ok = {}  
        self.host_unreachable = {}  
        self.host_failed = {}  
  
    def v2_runner_on_unreachable(self, result): 
        self.host_unreachable[result._host.get_name()] = result 
  
    def v2_runner_on_ok(self, result,  *args, **kwargs):  
        self.host_ok[result._host.get_name()] = result  
  
    def v2_runner_on_failed(self, result,  *args, **kwargs): 
        self.host_failed[result._host.get_name()] = result  

class PlayBookResultsCollector(CallbackBase):  
    CALLBACK_VERSION = 2.0    
    
    def __init__(self, *args, **kwargs):  
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)  
        self.task_ok = {}  
        self.task_skipped = {}  
        self.task_failed = {}  
        self.task_status = {} 
        self.task_unreachable = {}
        self.task_changed = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]  = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_skipped[result._host.get_name()]  = result

    def v2_runner_on_changed(self, result):
        self.task_changed[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                                       "ok":t['ok'],
                                       "changed" : t['changed'],
                                       "unreachable":t['unreachable'],
                                       "skipped":t['skipped'],
                                       "failed":t['failures']
                                   }

class ModelResultsCollectorToWebSocket(CallbackBase):  
  
    def __init__(self, websocket,*args, **kwargs):
        super(ModelResultsCollectorToWebSocket, self).__init__(*args, **kwargs)  
        self.host_ok = {}  
        self.host_unreachable = {}  
        self.host_failed = {}  
        self.websocket = websocket
    
    def save_msg(self,data):
        self.websocket.send_msg(data,self.websocket.logId)            
       
    def v2_runner_on_unreachable(self, result):  
        for remove_key in ('changed', 'invocation'):
            if remove_key in result._result:
                del result._result[remove_key] 
        data = "<font color='#FA8072'>{host} | UNREACHABLE! => {stdout}</font>".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))    
        self.save_msg(data)
        
    def v2_runner_on_ok(self, result,  *args, **kwargs):   
        for remove_key in ('changed', 'invocation','_ansible_parsed','_ansible_no_log'):
            if remove_key in result._result:
                del result._result[remove_key]    
        if 'rc' in result._result and 'stdout' in result._result:
            data = "<font color='green'>{host} | SUCCESS | rc={rc} >> \n{stdout}".format(host=result._host.get_name(),rc=result._result.get('rc'),stdout=result._result.get('stdout'))
        else:
            data = "<font color='green'>{host} | SUCCESS >> {stdout}</font>".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))
        self.save_msg(data)

  
    def v2_runner_on_failed(self, result,  *args, **kwargs): 
        for remove_key in ('changed', 'invocation'):
            if remove_key in result._result:
                del result._result[remove_key]
        if 'rc' in result._result and 'stderr' in result._result:
            data = "<font color='#DC143C'>{host} | FAILED | rc={rc} >> \n{stderr}</font>".format(host=result._host.get_name(),rc=result._result.get('rc'),stderr=result._result.get('stderr') + result._result.get('stdout') + result._result.get('msg'))
        else:
            data = "<font color='#DC143C'>{host} | FAILED! => {stderr}</font>".format(host=result._host.get_name(),stderr=json.dumps(result._result,indent=4))
        self.save_msg(data)

class PlayBookResultsCollectorWebSocket(CallbackBase):  
    CALLBACK_VERSION = 2.0   
     
    def __init__(self,websocket,total_tasks,*args, **kwargs):  
        super(PlayBookResultsCollectorWebSocket, self).__init__(*args, **kwargs)  
        self.task_ok = {}  
        self.task_skipped = {}  
        self.task_failed = {}  
        self.task_status = {} 
        self.task_unreachable = {}
        self.task_changed = {}
        self.websocket = websocket
        self.total_tasks = total_tasks
        self.count = 0
        self.taks_check = {}
     
    def save_msg(self,msg):
        self.websocket.send_msg(msg, self.websocket.logId)
        
    def v2_runner_on_ok(self, result, *args, **kwargs):  
        self._clean_results(result._result, result._task.action)    
        self.task_ok[result._host.get_name()]  = result._result
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        for remove_key in ('changed', 'invocation','_ansible_parsed','_ansible_no_log','_ansible_verbose_always'):
            if remove_key in result._result:
                del result._result[remove_key]         
        if result._task.action in ('include', 'include_role','_ansible_parsed','_ansible_no_log'):
            return
        elif result._result.get('changed', False):
            if delegated_vars:
                msg = "<font color='yellow'>changed: [%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
            else:
                msg = "<font color='yellow'>changed: [%s]</font>" % result._host.get_name()
        else:
            if delegated_vars:
                msg = "<font color='green'>ok: [%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
            elif 'msg' in result._result:
                msg = "<font color='green'>ok: [{host}] => \n{msg}</font>".format(host=result._host.get_name(), msg=result._result.get('msg'))                
            elif 'rc' in result._result and 'stdout' in result._result:
                msg = "<font color='green'>ok: [{host}] => \n{stdout}</font>".format(host=result._host.get_name(), stdout=result._result.get('stdout'))
            else:
                msg = "<font color='green'>ok: [%s]</font>" % result._host.get_name()  
        if result._task.loop and 'results' in result._result:
            self._process_items(result)   
        else:             
            self.save_msg(msg)
  
        
        
    def v2_runner_on_failed(self, result, *args, **kwargs):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        self.task_failed[result._host.get_name()] = result._result
        if 'exception' in result._result:
            msg = result._result['exception'].strip().split('\n')[-1]
            logger.error(msg=msg)
            del result._result['exception']
        if result._task.loop and 'results' in result._result:
            self._process_items(result)
        else:            
            if delegated_vars:
                msg = "<font color='#DC143C'>fatal: [{host} -> {delegated_vars}]: FAILED! => {msg}</font>".format(host=result._host.get_name(),delegated_vars=delegated_vars['ansible_host'],msg=json.dumps(result._result))
            else: 
                msg = "<font color='#DC143C'>fatal: [{host}]: FAILED! => {msg}</font>".format(host=result._host.get_name(),msg=json.dumps(result._result))
            self.save_msg(msg)

        
    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result._result
        msg = "<font color='#DC143C'>fatal: [{host}]: UNREACHABLE! => {msg}</font>\n".format(host=result._host.get_name(),msg=json.dumps(result._result))        
        self.save_msg(msg)
 
    
    def v2_runner_on_changed(self, result):
        self.task_changed[result._host.get_name()] = result._result
        msg = "<font color='yellow'>changed: [{host}]</font>\n".format(host=result._host.get_name())
        self.save_msg(msg)

         
    def v2_runner_on_skipped(self, result):
        self.task_skipped[result._host.get_name()]  = result._result
        msg = "<font color='#00FFFF'>skipped: [{host}]</font>\n".format(host=result._host.get_name())
        if result._task.loop and 'results' in result._result:
            self._process_items(result)        
        else:
            self.save_msg(msg)

    
    def v2_runner_on_no_hosts(self, task):
        msg = "<font color='#DC143C'>skipping: no hosts matched</font>"
        self.save_msg(msg)
       

    def v2_playbook_item_on_skipped(self, result):
        msg = "<font color='yellow'>skipping: [%s] => (item=%s)</font>" % (result._host.get_name(), result._result['item'])
        self.save_msg(msg)

    
    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip()
        if not name:
            msg = u"<font color='#FFFFFF'>PLAY"
        else:
            msg = u"<font color='#FFFFFF'>PLAY [%s]" % name
        if len(msg) < 80:msg = msg + '*'*(79-len(msg)) + '</font>'
        self.save_msg(msg)

        
    def _print_task_banner(self, task):
        task_detail = ''
        if task.get_name().strip() not in ['Gathering Facts']:
            task_progress = int((self.count/self.total_tasks)*100)
            if task_progress == 100:task_progress = 99
            task_detail = "Progress: {count}/{total_tasks} Percentage: {task_progress}%".format(count=self.count,total_tasks=self.total_tasks,task_progress=str(task_progress))     
        msg = "<font color='#FFFFFF'>\nTASK [%s]  %s " % (task.get_name().strip(),task_detail)
        if len(msg) < 80:msg = msg + '*'*(80-len(msg)) + '</font>'
        self.count = self.count + 1
        self.save_msg(msg)


    def v2_playbook_on_task_start(self, task, is_conditional):
        self._print_task_banner(task)

    def v2_playbook_on_cleanup_task_start(self, task):
        msg = "<font color='#FFFFFF'>CLEANUP TASK [%s]</font>" % task.get_name().strip()
        self.save_msg(msg)


    def v2_playbook_on_handler_task_start(self, task):
        msg = "<font color='#FFFFFF'>RUNNING HANDLER [%s]</font>" % task.get_name().strip()
        self.save_msg(msg)
        
    def v2_playbook_on_stats(self, stats):
        msg = "<font color='#FFFFFF'>\nPLAY RECAP *********************************************************************</font>"
        self.save_msg(msg)
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                                       "ok":t['ok'],
                                       "changed" : t['changed'],
                                       "unreachable":t['unreachable'],
                                       "skipped":t['skipped'],
                                       "failed":t['failures']
                                   }
            f_color,u_color,c_color,s_color,o_color,h_color = '#FFFFFF','#FFFFFF','#FFFFFF','#00FFFF','green','green'
            if t['failures'] > 0 :f_color,h_color = '#DC143C','#DC143C' 
            elif t['unreachable'] > 0:u_color,h_color = '#DC143C','#DC143C'
            elif t['changed'] > 0:c_color,h_color = 'yellow','yellow'
            elif t['ok'] > 0:o_color = 'green'
            elif t["skipped"] > 0:s_color='yellow'
            msg = """<font color='{h_color}'>{host}</font>\t\t: <font color='{o_color}'>ok={ok}</font>\t<font color='{c_color}'>changed={changed}</font>\t<font color='{u_color}'>unreachable={unreachable}</font>\t<font color='{s_color}'>skipped={skipped}</font>\t<font color='{f_color}'>failed={failed}</font>""".format(
                                                                          host=h,ok=t['ok'],changed=t['changed'],
                                                                          unreachable=t['unreachable'],
                                                                          skipped=t["skipped"],failed=t['failures'],
                                                                          f_color = f_color,h_color=h_color,
                                                                          u_color=u_color,c_color=c_color,
                                                                          o_color=o_color,s_color=s_color
                                                                         )                
            self.save_msg(msg)


            
    def v2_runner_item_on_ok(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if result._task.action in ('include', 'include_role'):
            return
        elif result._result.get('changed', False):
            msg = "<font color='yellow'>changed"
        else:
            msg = "<font color='green'>ok"
        if delegated_vars:
            msg += ": [%s -> %s]" % (result._host.get_name(), delegated_vars['ansible_host'])
        else:
            msg += ": [%s]" % result._host.get_name()
        msg += " => (item=%s)</font>" % (json.dumps(self._get_item(result._result)))
        if (self._display.verbosity > 0 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += " => %s</font>" % json.dumps(result._result)
        self.save_msg(msg)


    def v2_runner_item_on_failed(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if 'exception' in result._result:
            msg = result._result['exception'].strip().split('\n')[-1]
            logger.error(msg=msg)
            del result._result['exception']        
        msg = "<font color='#DC143C'>failed: "
        if delegated_vars:
            msg += "[%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
        else:
            msg += "[%s] => (item=%s) => %s</font>" % (result._host.get_name(), result._result['item'], self._dump_results(result._result))
        self.save_msg(msg)


    def v2_runner_item_on_skipped(self, result):
        msg = "<font color='yellow'>skipping: [%s] => (item=%s)</font>" % (result._host.get_name(), self._get_item(result._result))
        if (self._display.verbosity > 0 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += " => %s</font>" % json.dumps(result._result)
        self.save_msg(msg)


    def v2_runner_retry(self, result):
        task_name = result.task_name or result._task
        msg = "<font color='#DC143C'>FAILED - RETRYING: %s (%d retries left).</font>" % (task_name, result._result['retries'] - result._result['attempts'])
        if (self._display.verbosity > 2 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += "Result was: %s</font>" % json.dumps(result._result,indent=4)
        self.save_msg(msg)

class PlayBookResultsCollectorApplyTask(CallbackBase):  
    CALLBACK_VERSION = 2.0   
     
    def __init__(self, deplytask, total_tasks, *args, **kwargs):  
        super(PlayBookResultsCollectorApplyTask, self).__init__(*args, **kwargs)  
        self.task_ok = {}  
        self.task_skipped = {}  
        self.task_failed = {}  
        self.task_status = {} 
        self.task_unreachable = {}
        self.task_changed = {}
        self.deplytask = deplytask
        self.total_tasks = total_tasks
        self.count = 0
        self.taks_check = {}
     
    def save_msg(self,task_msg, task_name, task_type='name'):
        try:
            return Apply_Tasks_Result.objects.create(
                                      logId= self.deplytask,
                                      task_msg = task_msg,
                                      task_name = task_name,
                                      task_type = task_type
                                      )
        except Exception as ex:
            logger.error(msg="记录剧本执行日志失败:{ex}".format(ex=ex))
            return False         
        
#     def v2_runner_on_ok(self, result, *args, **kwargs):  
#         self._clean_results(result._result, result._task.action)    
#         self.task_ok[result._host.get_name()]  = result._result
#         delegated_vars = result._result.get('_ansible_delegated_vars', None)
#         for remove_key in ('changed', 'invocation','_ansible_parsed','_ansible_no_log','_ansible_verbose_always'):
#             if remove_key in result._result:
#                 del result._result[remove_key]         
#         if result._task.action in ('include', 'include_role','_ansible_parsed','_ansible_no_log'):
#             return
#         elif result._result.get('changed', False):
#             if delegated_vars:
#                 msg = "<font color='yellow'>changed: [%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
#             else:
#                 msg = "<font color='yellow'>changed: [%s]</font>" % result._host.get_name()
#         else:
#             if delegated_vars:
#                 msg = "<font color='green'>ok: [%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
#             elif 'msg' in result._result:
#                 msg = "<font color='green'>ok: [{host}] => \n{msg}</font>".format(host=result._host.get_name(), msg=result._result.get('msg'))                
#             elif 'rc' in result._result and 'stdout' in result._result:
#                 msg = "<font color='green'>ok: [{host}] => \n{stdout}</font>".format(host=result._host.get_name(), stdout=result._result.get('stdout'))
#             else:
#                 msg = "<font color='green'>ok: [%s]</font>" % result._host.get_name()  
#         if result._task.loop and 'results' in result._result:
#             self._process_items(result)   
#         else:             
#             self.save_msg(msg)
  
        
        
    def v2_runner_on_failed(self, result, *args, **kwargs):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        self.task_failed[result._host.get_name()] = result._result
        if 'exception' in result._result:
            msg = result._result['exception'].strip().split('\n')[-1]
            logger.error(msg=msg)
            del result._result['exception']
        if result._task.loop and 'results' in result._result:
            self._process_items(result)
        else:            
            if delegated_vars:
                msg = "<font color='#DC143C'>fatal: [{host} -> {delegated_vars}]: FAILED! => {msg}</font>".format(host=result._host.get_name(),delegated_vars=delegated_vars['ansible_host'],msg=json.dumps(result._result))
            else: 
                msg = "<font color='#DC143C'>fatal: [{host}]: FAILED! => {msg}</font>".format(host=result._host.get_name(),msg=json.dumps(result._result))
            self.save_msg(msg, result.task_name, 'msg')
            
    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result._result
        msg = "<font color='#DC143C'>fatal: [{host}]: UNREACHABLE! => {msg}</font>\n".format(host=result._host.get_name(),msg=json.dumps(result._result))        
        self.save_msg(msg, result.task_name, 'msg')
        
    def _print_task_banner(self, task):
        if task.get_name().strip() not in ['Gathering Facts']:
            task_per = str(int((self.count/self.total_tasks)*100)) 
            if task_per == '100':task_per = '99' 
            try:
                self.deplytask.status =  'running' 
                self.deplytask.task_per =  task_per 
                self.deplytask.save()
            except Exception as ex:
                logger.error(msg='保存任务进度失败: {ex}'.format(ex=str(ex))) 
            self.count = self.count + 1    
        msg = "<font color='#FFFFFF'>\nTASK [%s]" % (task.get_name().strip())
        if len(msg) < 80:msg = msg + '*'*(80-len(msg)) + '</font>'
        self.save_msg(msg, task.get_name().strip(), 'banner') 
              
 
    def v2_playbook_on_task_start(self, task, is_conditional):
        self._print_task_banner(task)


    def v2_playbook_on_stats(self, stats):
        self.deplytask.status = 'finished'
#         msg = "<font color='#FFFFFF'>\nPLAY RECAP *********************************************************************</font>"
#         self.save_msg(msg, 'playbook_on_stats', 'stats')
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                                       "ok":t['ok'],
                                       "changed" : t['changed'],
                                       "unreachable":t['unreachable'],
                                       "skipped":t['skipped'],
                                       "failed":t['failures']
                                   }
            f_color,u_color,c_color,s_color,o_color,h_color = '#FFFFFF','#FFFFFF','#FFFFFF','#00FFFF','green','green'
            if t['failures'] > 0 :
                f_color,h_color = '#DC143C','#DC143C' 
                self.deplytask.status = 'failed'
                
            elif t['unreachable'] > 0:
                u_color,h_color = '#DC143C','#DC143C'
                self.deplytask.status = 'failed'
                
            elif t['changed'] > 0:c_color,h_color = 'yellow','yellow'
            elif t['ok'] > 0:o_color = 'green'
            elif t["skipped"] > 0:s_color='yellow'
            msg = """<font color='{h_color}'>{host}</font>\t\t: <font color='{o_color}'>ok={ok}</font>\t<font color='{c_color}'>changed={changed}</font>\t<font color='{u_color}'>unreachable={unreachable}</font>\t<font color='{s_color}'>skipped={skipped}</font>\t<font color='{f_color}'>failed={failed}</font>""".format(
                                                                          host=h,ok=t['ok'],changed=t['changed'],
                                                                          unreachable=t['unreachable'],
                                                                          skipped=t["skipped"],failed=t['failures'],
                                                                          f_color = f_color,h_color=h_color,
                                                                          u_color=u_color,c_color=c_color,
                                                                          o_color=o_color,s_color=s_color
                                                                         )                
            self.save_msg(msg, 'playbook_on_stats', 'stats')
            
            try:
                self.deplytask.task_per =  100
                self.deplytask.save()
            except Exception as ex:
                logger.error(msg='保存任务状态失败: {ex}'.format(ex=str(ex))) 

    def v2_runner_item_on_failed(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if 'exception' in result._result:
            msg = result._result['exception'].strip().split('\n')[-1]
            logger.error(msg=msg)
            del result._result['exception']        
        msg = "<font color='#DC143C'>failed: "
        if delegated_vars:
            msg += "[%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
        else:
            msg += "[%s] => (item=%s) => %s</font>" % (result._host.get_name(), result._result['item'], self._dump_results(result._result))
        self.save_msg(msg, result.task_name, 'msg')

class ModelResultsCollectorBackground(CallbackBase):  
  
    def __init__(self, background,*args, **kwargs):
        super(ModelResultsCollectorBackground, self).__init__(*args, **kwargs)  
        self.host_ok = {}  
        self.host_unreachable = {}  
        self.host_failed = {}  
        self.background = background
    
    def save_msg(self,data):
        DeploySaveResult.Model.insert(self.background, data)          
       
    def v2_runner_on_unreachable(self, result):  
        for remove_key in ('changed', 'invocation'):
            if remove_key in result._result:
                del result._result[remove_key] 
        data = "<font color='#FA8072'>{host} | UNREACHABLE! => {stdout}</font>".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))    
        self.save_msg(data)
        
    def v2_runner_on_ok(self, result,  *args, **kwargs):   
        for remove_key in ('changed', 'invocation','_ansible_parsed','_ansible_no_log'):
            if remove_key in result._result:
                del result._result[remove_key]    
        if 'rc' in result._result and 'stdout' in result._result:
            data = "<font color='green'>{host} | SUCCESS | rc={rc} >> \n{stdout}".format(host=result._host.get_name(),rc=result._result.get('rc'),stdout=result._result.get('stdout'))
        else:
            data = "<font color='green'>{host} | SUCCESS >> {stdout}</font>".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))
        self.save_msg(data)

  
    def v2_runner_on_failed(self, result,  *args, **kwargs):   
        for remove_key in ('changed', 'invocation'):
            if remove_key in result._result:
                del result._result[remove_key]
        if 'rc' in result._result and 'stderr' in result._result:
            data = "<font color='#DC143C'>{host} | FAILED | rc={rc} >> \n{stderr}</font>".format(host=result._host.get_name(),rc=result._result.get('rc'),stderr=result._result.get('stderr') + result._result.get('stdout') + result._result.get('msg'))
        else:
            data = "<font color='#DC143C'>{host} | FAILED! => {stderr}</font>".format(host=result._host.get_name(),stderr=json.dumps(result._result,indent=4))
        self.save_msg(data)        

class PlayBookResultsCollectorBackground(CallbackBase):  
    CALLBACK_VERSION = 2.0   
     
    def __init__(self,background,*args, **kwargs):  
        super(PlayBookResultsCollectorBackground, self).__init__(*args, **kwargs)  
        self.task_ok = {}  
        self.task_skipped = {}  
        self.task_failed = {}  
        self.task_status = {} 
        self.task_unreachable = {}
        self.task_changed = {}
        self.background = background
        self.taks_check = {}
     
    def save_msg(self,msg):
        DeploySaveResult.PlayBook.insert(self.background, msg)
        
    def v2_runner_on_ok(self, result, *args, **kwargs):  
        self._clean_results(result._result, result._task.action)    
        self.task_ok[result._host.get_name()]  = result._result
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        for remove_key in ('changed', 'invocation','_ansible_parsed','_ansible_no_log','_ansible_verbose_always'):
            if remove_key in result._result:
                del result._result[remove_key]         
        if result._task.action in ('include', 'include_role','_ansible_parsed','_ansible_no_log'):
            return
        elif result._result.get('changed', False):
            if delegated_vars:
                msg = "<font color='yellow'>changed: [%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
            else:
                msg = "<font color='yellow'>changed: [%s]</font>" % result._host.get_name()
        else:
            if delegated_vars:
                msg = "<font color='green'>ok: [%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
            elif 'msg' in result._result:
                msg = "<font color='green'>ok: [{host}] => {stdout}</font>".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))  
            else:
                msg = "<font color='green'>ok: [%s]</font>" % result._host.get_name()  
        if result._task.loop and 'results' in result._result:
            self._process_items(result)   
        else:             
            self.save_msg(msg)
  
        
        
    def v2_runner_on_failed(self, result, *args, **kwargs):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        self.task_failed[result._host.get_name()] = result._result
        if 'exception' in result._result:
            msg = result._result['exception'].strip().split('\n')[-1]
            logger.error(msg=msg)
            del result._result['exception']
        if result._task.loop and 'results' in result._result:
            self._process_items(result)
        else:            
            if delegated_vars:
                msg = "<font color='#DC143C'>fatal: [{host} -> {delegated_vars}]: FAILED! => {msg}</font>".format(host=result._host.get_name(),delegated_vars=delegated_vars['ansible_host'],msg=json.dumps(result._result))
            else: 
                msg = "<font color='#DC143C'>fatal: [{host}]: FAILED! => {msg}</font>".format(host=result._host.get_name(),msg=json.dumps(result._result))
            self.save_msg(msg)

        
    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result._result
        msg = "<font color='#DC143C'>fatal: [{host}]: UNREACHABLE! => {msg}</font>\n".format(host=result._host.get_name(),msg=json.dumps(result._result))        
        self.save_msg(msg)
 
    
    def v2_runner_on_changed(self, result):
        self.task_changed[result._host.get_name()] = result._result
        msg = "<font color='yellow'>changed: [{host}]</font>\n".format(host=result._host.get_name())
        self.save_msg(msg)

         
    def v2_runner_on_skipped(self, result):
        self.task_skipped[result._host.get_name()]  = result._result
        msg = "<font color='#00FFFF'>skipped: [{host}]</font>\n".format(host=result._host.get_name())
        if result._task.loop and 'results' in result._result:
            self._process_items(result)        
        else:
            self.save_msg(msg)

    
    def v2_runner_on_no_hosts(self, task):
        msg = "<font color='#DC143C'>skipping: no hosts matched</font>"
        self.save_msg(msg)
       

    def v2_playbook_item_on_skipped(self, result):
        msg = "<font color='yellow'>skipping: [%s] => (item=%s)</font>" % (result._host.get_name(), result._result['item'])
        self.save_msg(msg)

    
    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip()
        if not name:
            msg = u"<font color='#FFFFFF'>PLAY"
        else:
            msg = u"<font color='#FFFFFF'>PLAY [%s]" % name
        if len(msg) < 80:msg = msg + '*'*(79-len(msg)) + '</font>'
        self.save_msg(msg)

        
    def _print_task_banner(self, task):
        msg = "<font color='#FFFFFF'>\nTASK [%s]" % (task.get_name().strip())
        if len(msg) < 80:msg = msg + '*'*(80-len(msg)) + '</font>'
        self.save_msg(msg)


    def v2_playbook_on_task_start(self, task, is_conditional):
        self._print_task_banner(task)

    def v2_playbook_on_cleanup_task_start(self, task):
        msg = "<font color='#FFFFFF'>CLEANUP TASK [%s]</font>" % task.get_name().strip()
        self.save_msg(msg)


    def v2_playbook_on_handler_task_start(self, task):
        msg = "<font color='#FFFFFF'>RUNNING HANDLER [%s]</font>" % task.get_name().strip()
        self.save_msg(msg)
        
    def v2_playbook_on_stats(self, stats):
        msg = "<font color='#FFFFFF'>\nPLAY RECAP *********************************************************************</font>"
        self.save_msg(msg)
        if self.background:DeploySaveResult.PlayBook.insert(self.background, msg)
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                                       "ok":t['ok'],
                                       "changed" : t['changed'],
                                       "unreachable":t['unreachable'],
                                       "skipped":t['skipped'],
                                       "failed":t['failures']
                                   }
            f_color,u_color,c_color,s_color,o_color,h_color = '#FFFFFF','#FFFFFF','#FFFFFF','#00FFFF','green','green'
            if t['failures'] > 0 :f_color,h_color = '#DC143C','#DC143C' 
            elif t['unreachable'] > 0:u_color,h_color = '#DC143C','#DC143C'
            elif t['changed'] > 0:c_color,h_color = 'yellow','yellow'
            elif t['ok'] > 0:o_color = 'green'
            elif t["skipped"] > 0:s_color='yellow'
            msg = """<font color='{h_color}'>{host}</font>\t\t: <font color='{o_color}'>ok={ok}</font>\t<font color='{c_color}'>changed={changed}</font>\t<font color='{u_color}'>unreachable={unreachable}</font>\t<font color='{s_color}'>skipped={skipped}</font>\t<font color='{f_color}'>failed={failed}</font>""".format(
                                                                          host=h,ok=t['ok'],changed=t['changed'],
                                                                          unreachable=t['unreachable'],
                                                                          skipped=t["skipped"],failed=t['failures'],
                                                                          f_color = f_color,h_color=h_color,
                                                                          u_color=u_color,c_color=c_color,
                                                                          o_color=o_color,s_color=s_color
                                                                         )                
            self.save_msg(msg)


            
    def v2_runner_item_on_ok(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if result._task.action in ('include', 'include_role'):
            return
        elif result._result.get('changed', False):
            msg = "<font color='yellow'>changed"
        else:
            msg = "<font color='green'>ok"
        if delegated_vars:
            msg += ": [%s -> %s]" % (result._host.get_name(), delegated_vars['ansible_host'])
        else:
            msg += ": [%s]" % result._host.get_name()
        msg += " => (item=%s)</font>" % (json.dumps(self._get_item(result._result)))
        if (self._display.verbosity > 0 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += " => %s</font>" % json.dumps(result._result)
        self.save_msg(msg)


    def v2_runner_item_on_failed(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if 'exception' in result._result:
            msg = result._result['exception'].strip().split('\n')[-1]
            logger.error(msg=msg)
            del result._result['exception']        
        msg = "<font color='#DC143C'>failed: "
        if delegated_vars:
            msg += "[%s -> %s]</font>" % (result._host.get_name(), delegated_vars['ansible_host'])
        else:
            msg += "[%s] => (item=%s) => %s</font>" % (result._host.get_name(), result._result['item'], self._dump_results(result._result))
        self.save_msg(msg)


    def v2_runner_item_on_skipped(self, result):
        msg = "<font color='yellow'>skipping: [%s] => (item=%s)</font>" % (result._host.get_name(), self._get_item(result._result))
        if (self._display.verbosity > 0 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += " => %s</font>" % json.dumps(result._result)
        self.save_msg(msg)


    def v2_runner_retry(self, result):
        task_name = result.task_name or result._task
        msg = "<font color='#DC143C'>FAILED - RETRYING: %s (%d retries left).</font>" % (task_name, result._result['retries'] - result._result['attempts'])
        if (self._display.verbosity > 2 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += "Result was: %s</font>" % json.dumps(result._result,indent=4)
        self.save_msg(msg)

def AdHoccallback(websocket,background=None):
    if websocket:
        return ModelResultsCollectorToWebSocket(websocket) 
    
    elif background:
        return ModelResultsCollectorBackground(background)
    
    else:
        return ModelResultsCollector()
    
def Playbookcallback(websocket,deplytask=None,background=None,total_tasks=None):
    if websocket:
        return PlayBookResultsCollectorWebSocket(websocket,total_tasks) 
    
    elif background:
        return PlayBookResultsCollectorBackground(background)    
    
    elif deplytask:
        return PlayBookResultsCollectorApplyTask(deplytask=deplytask,total_tasks=total_tasks)    
    
    else:
        return PlayBookResultsCollector()    
    
    