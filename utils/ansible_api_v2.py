#!/usr/bin/env python
# -*- coding=utf-8 -*-
import json,sys,os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory,Host,Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
from OpsManage.data.DsRedisOps import DsRedis 

class MyInventory(Inventory):  
    """ 
    this is my ansible inventory object. 
    """  
    def __init__(self, resource, loader, variable_manager):  
        """ 
        resource的数据格式是一个列表字典，比如 
            { 
                "group1": { 
                    "hosts": [{"hostname": "10.0.0.0", "port": "22", "username": "test", "password": "pass"}, ...], 
                    "vars": {"var1": value1, "var2": value2, ...} 
                } 
            } 
 
                     如果你只传入1个列表，这默认该列表内的所有主机属于my_group组,比如 
            [{"hostname": "10.0.0.0", "port": "22", "username": "test", "password": "pass"}, ...] 
        """  
        self.resource = resource  
        self.inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[])  
        self.dynamic_inventory()  
  
    def add_dynamic_group(self, hosts, groupname, groupvars=None):  
        """ 
            add hosts to a group 
        """  
        my_group = Group(name=groupname)  
  
        # if group variables exists, add them to group  
        if groupvars:  
            for key, value in groupvars.iteritems():  
                my_group.set_variable(key, value)  
  
        # add hosts to group  
        for host in hosts:  
            # set connection variables  
            hostname = host.get("hostname")  
            hostip = host.get('ip', hostname)  
            hostport = host.get("port")  
            username = host.get("username")  
            password = host.get("password")  
            ssh_key = host.get("ssh_key")  
            my_host = Host(name=hostname, port=hostport)  
            my_host.set_variable('ansible_ssh_host', hostip)  
            my_host.set_variable('ansible_ssh_port', hostport)  
            my_host.set_variable('ansible_ssh_user', username)  
            my_host.set_variable('ansible_ssh_pass', password)  
            my_host.set_variable('ansible_ssh_private_key_file', ssh_key)  
  
            # set other variables  
            for key, value in host.iteritems():  
                if key not in ["hostname", "port", "username", "password"]:  
                    my_host.set_variable(key, value)  
            # add to group  
            my_group.add_host(my_host)  
  
        self.inventory.add_group(my_group)  
  
    def dynamic_inventory(self):  
        """ 
            add hosts to inventory. 
        """  
        if isinstance(self.resource, list):  
            self.add_dynamic_group(self.resource, 'default_group')  
        elif isinstance(self.resource, dict):  
            for groupname, hosts_and_vars in self.resource.iteritems():  
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars")) 


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

        
class ModelResultsCollectorToRedis(CallbackBase):  
  
    def __init__(self, redisKey,*args, **kwargs):
        super(ModelResultsCollectorToRedis, self).__init__(*args, **kwargs)  
        self.host_ok = {}  
        self.host_unreachable = {}  
        self.host_failed = {}  
        self.redisKey = redisKey
        
    def v2_runner_on_unreachable(self, result):  
        for remove_key in ('changed', 'invocation'):
            if remove_key in result._result:
                del result._result[remove_key] 
        data = "{host} | UNREACHABLE! => {stdout}".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))        
        DsRedis.OpsAnsibleModel.lpush(self.redisKey,data) 
   
        
    def v2_runner_on_ok(self, result,  *args, **kwargs):   
        for remove_key in ('changed', 'invocation'):
            if remove_key in result._result:
                del result._result[remove_key]       
        if result._result.has_key('rc') and result._result.has_key('stdout'):
            data = "{host} | SUCCESS | rc={rc} >> \n{stdout}".format(host=result._host.get_name(),rc=result._result.get('rc'),stdout=result._result.get('stdout'))
        else:
            data = "{host} | SUCCESS >> {stdout}".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))
        DsRedis.OpsAnsibleModel.lpush(self.redisKey,data)
  
    def v2_runner_on_failed(self, result,  *args, **kwargs):  
        for remove_key in ('changed', 'invocation'):
            if remove_key in result._result:
                del result._result[remove_key]         
        if result._result.has_key('rc') and result._result.has_key('stdout'):
            data = "{host} | FAILED | rc={rc} >> \n{stdout}".format(host=result._host.get_name(),rc=result._result.get('rc'),stdout=result._result.get('stdout'))
        else:
            data = "{host} | FAILED! => {stdout}".format(host=result._host.get_name(),stdout=json.dumps(result._result,indent=4))
        DsRedis.OpsAnsibleModel.lpush(self.redisKey,data)



class PlayBookResultsCollectorToRedis(CallbackBase):  
    CALLBACK_VERSION = 2.0    
    def __init__(self,redisKey,*args, **kwargs):  
        super(PlayBookResultsCollectorToRedis, self).__init__(*args, **kwargs)  
        self.task_ok = {}  
        self.task_skipped = {}  
        self.task_failed = {}  
        self.task_status = {} 
        self.task_unreachable = {}
        self.task_changed = {}
        self.redisKey = redisKey
        
    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]  = result._result
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if result._task.action in ('include', 'include_role'):
            return
        elif result._result.get('changed', False):
            if delegated_vars:
                msg = "changed: [%s -> %s]" % (result._host.get_name(), delegated_vars['ansible_host'])
            else:
                msg = "changed: [%s]" % result._host.get_name()
        else:
            if delegated_vars:
                msg = "ok: [%s -> %s]" % (result._host.get_name(), delegated_vars['ansible_host'])
            else:
                msg = "ok: [%s]" % result._host.get_name()  
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)    

        
    def v2_runner_on_failed(self, result, *args, **kwargs):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        self.task_failed[result._host.get_name()] = result._result
        if delegated_vars:
            msg = "fatal: [{host} -> {delegated_vars}]: FAILED! => {msg}".format(host=result._host.get_name(),delegated_vars=delegated_vars['ansible_host'],msg=json.dumps(result._result))
        else: 
            msg = "fatal: [{host}]: FAILED! => {msg}".format(host=result._host.get_name(),msg=json.dumps(result._result))
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg) 
        
    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result._result
        msg = "fatal: [{host}]: UNREACHABLE! => {msg}\n".format(host=result._host.get_name(),msg=json.dumps(result._result))        
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)     
   
    def v2_runner_on_changed(self, result):
        self.task_changed[result._host.get_name()] = result._result
        msg = "changed: [{host}]\n".format(host=result._host.get_name())
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg) 
        
    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()]  = result._result
        msg = "skipped: [{host}]\n".format(host=result._host.get_name())
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)

    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip()
        if not name:
            msg = u"PLAY"
        else:
            msg = u"PLAY [%s] " % name
        if len(msg) < 80:msg = msg + '*'*(79-len(msg))
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)
        
    def _print_task_banner(self, task):
        msg = "\nTASK [%s] " % (task.get_name().strip())
        if len(msg) < 80:msg = msg + '*'*(80-len(msg))
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)
#         args = ''
#         if not task.no_log and C.DISPLAY_ARGS_TO_STDOUT:
#             args = u', '.join(u'%s=%s' % a for a in task.args.items())
#             args = u' %s' % args        
#         print u"\nTASK [%s%s]" % (task.get_name().strip(), args)


    def v2_playbook_on_task_start(self, task, is_conditional):
        self._print_task_banner(task)

    def v2_playbook_on_cleanup_task_start(self, task):
        msg = "CLEANUP TASK [%s]" % task.get_name().strip()
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)

    def v2_playbook_on_handler_task_start(self, task):
        msg = "RUNNING HANDLER [%s]" % task.get_name().strip()
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)
        
    def v2_playbook_on_stats(self, stats):
        msg = "\nPLAY RECAP *********************************************************************"
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)
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
            msg = "{host}\t\t: ok={ok}\tchanged={changed}\tunreachable={unreachable}\tskipped={skipped}\tfailed={failed}".format(
                                                                                                              host=h,ok=t['ok'],changed=t['changed'],
                                                                                                              unreachable=t['unreachable'],
                                                                                                              skipped=t["skipped"],failed=t['failures']
                                                                                                              )
            DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)

            
    def v2_runner_item_on_ok(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        if result._task.action in ('include', 'include_role'):
            return
        elif result._result.get('changed', False):
            msg = 'changed'
        else:
            msg = 'ok'
        if delegated_vars:
            msg += ": [%s -> %s]" % (result._host.get_name(), delegated_vars['ansible_host'])
        else:
            msg += ": [%s]" % result._host.get_name()
        msg += " => (item=%s)" % (json.dumps(self._get_item(result._result)))
        if (self._display.verbosity > 0 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += " => %s" % json.dumps(result._result)
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)

    def v2_runner_item_on_failed(self, result):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        msg = "failed: "
        if delegated_vars:
            msg += "[%s -> %s]" % (result._host.get_name(), delegated_vars['ansible_host'])
        else:
            msg += "[%s]" % (result._host.get_name())
        msg = msg + " (item=%s) => %s\n" % (self._get_item(json.dumps(result._result)), json.dumps(result._result)),
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)

    def v2_runner_item_on_skipped(self, result):
        msg = "skipping: [%s] => (item=%s) " % (result._host.get_name(), self._get_item(result._result))
        if (self._display.verbosity > 0 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += " => %s" % json.dumps(result._result)
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)

    def v2_runner_retry(self, result):
        task_name = result.task_name or result._task
        msg = "FAILED - RETRYING: %s (%d retries left)." % (task_name, result._result['retries'] - result._result['attempts'])
        if (self._display.verbosity > 2 or '_ansible_verbose_always' in result._result) and not '_ansible_verbose_override' in result._result:
            msg += "Result was: %s" % json.dumps(result._result,indent=4)
        DsRedis.OpsAnsiblePlayBook.lpush(self.redisKey,msg)

class PlayBookResultsCollector(CallbackBase):  
    CALLBACK_VERSION = 2.0    
    def __init__(self, *args, **kwargs):  
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)  
        self.task_ok = {}  
        self.task_skipped = {}  
        self.task_failed = {}  
        self.task_status = {} 
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]  = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()]  = result

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
            
class ANSRunner(object):  
    """ 
    This is a General object for parallel execute modules. 
    """  
    def __init__(self,resource,redisKey=None,*args, **kwargs):  
        self.resource = resource  
        self.inventory = None  
        self.variable_manager = None  
        self.loader = None  
        self.options = None  
        self.passwords = None  
        self.callback = None  
        self.__initializeData()  
        self.results_raw = {}  
        self.redisKey = redisKey
  
    def __initializeData(self):  
        """ 初始化ansible """  
        Options = namedtuple('Options', ['connection','module_path', 'forks', 'timeout',  'remote_user',  
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',  
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',  
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax'])  
   
        self.variable_manager = VariableManager()  
        self.loader = DataLoader()  
        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,  
                remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,  
                sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,  
                become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,  
                listtasks=False, listtags=False, syntax=False)  
  
        self.passwords = dict(sshpass=None, becomepass=None)  
        self.inventory = MyInventory(self.resource, self.loader, self.variable_manager).inventory
        self.variable_manager.set_inventory(self.inventory)  
  
    def run_model(self, host_list, module_name, module_args):  
        """ 
        run module from andible ad-hoc. 
        module_name: ansible module_name 
        module_args: ansible module args 
        """  
        play_source = dict(  
                name="Ansible Play",  
                hosts=host_list,  
                gather_facts='no',  
                tasks=[dict(action=dict(module=module_name, args=module_args))]  
        )  
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)  
        tqm = None  
        if self.redisKey:self.callback = ModelResultsCollectorToRedis(self.redisKey)  
        else:self.callback = ModelResultsCollector()  
        try:  
            tqm = TaskQueueManager(  
                    inventory=self.inventory,  
                    variable_manager=self.variable_manager,  
                    loader=self.loader,  
                    options=self.options,  
                    passwords=self.passwords,  
            )  
            tqm._stdout_callback = self.callback  
            tqm.run(play)  
        finally:  
            if tqm is not None:  
                tqm.cleanup()  
  
    def run_playbook(self, host_list, playbook_path,extra_vars=None): 
        """ 
        run ansible palybook 
        """         
        try: 
            if self.redisKey:self.callback = PlayBookResultsCollectorToRedis(self.redisKey)  
            else:self.callback = PlayBookResultsCollector()  
            if extra_vars:self.variable_manager.extra_vars = extra_vars 
            executor = PlaybookExecutor(  
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager, loader=self.loader,  
                options=self.options, passwords=self.passwords,  
            )  
            executor._tqm._stdout_callback = self.callback  
            executor.run()  
        except Exception as e: 
            return False
            
    def get_model_result(self):  
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}  
        for host, result in self.callback.host_ok.items():  
            self.results_raw['success'][host] = result._result  


        for host, result in self.callback.host_failed.items():  
            self.results_raw['failed'][host] = result._result 

  
        for host, result in self.callback.host_unreachable.items():  
            self.results_raw['unreachable'][host]= result._result 

        return json.dumps(self.results_raw)  

    def get_playbook_result(self):  
        self.results_raw = {'skipped':{}, 'failed':{}, 'ok':{},"status":{},'unreachable':{},"changed":{}} 
        
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result 
  
        for host, result in self.callback.task_failed.items():  
            self.results_raw['failed'][host] = result 
 
        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result 

        for host, result in self.callback.task_changed.items():
            self.results_raw['changed'][host] = result 

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result 

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result
        return self.results_raw

    def handle_cmdb_data(self,data):
        '''处理setup返回结果方法'''
        data_list = []
        for k,v in json.loads(data).items():
            if k == "success":
                for x,y in v.items():
                    cmdb_data = {}
                    data = y.get('ansible_facts')
                    disk_size = 0
                    cpu = data['ansible_processor'][-1]
                    for k,v in data['ansible_devices'].items():
                        if k[0:2] in ['sd','hd','ss','vd']:
                            disk = int((int(v.get('sectors')) * int(v.get('sectorsize')))/1024/1024/1024)
                            disk_size = disk_size + disk
                    cmdb_data['serial'] = data['ansible_product_serial'].split()[0]
                    cmdb_data['ip'] = x
                    cmdb_data['cpu'] = cpu.replace('@','')
                    ram_total = str(data['ansible_memtotal_mb'])
                    if len(ram_total) == 4:ram_total=ram_total[0] + 'GB'
                    elif len(ram_total) == 5:ram_total=ram_total[0:2] + 'GB'
                    elif len(ram_total) > 5:ram_total=ram_total[0:3] + 'GB'
                    else:
                        ram_total = ram_total + 'MB'
                    cmdb_data['ram_total'] = ram_total
                    cmdb_data['disk_total'] = str(disk_size) + 'GB'
                    cmdb_data['system'] =  data['ansible_distribution'] + ' ' + data['ansible_distribution_version'] + ' ' + data['ansible_userspace_bits']
                    cmdb_data['model'] = data['ansible_product_name'].split(':')[0]
                    cmdb_data['cpu_number'] = data['ansible_processor_count']
                    cmdb_data['vcpu_number'] = data['ansible_processor_vcpus']
                    cmdb_data['cpu_core'] = data['ansible_processor_cores']
                    cmdb_data['hostname'] = data['ansible_hostname']
                    cmdb_data['kernel'] = str(data['ansible_kernel'])
                    cmdb_data['manufacturer'] = data['ansible_system_vendor']
                    if data['ansible_selinux']: 
                        cmdb_data['selinux'] = data['ansible_selinux'].get('status')
                    else: 
                        cmdb_data['selinux'] = 'disabled'
                    cmdb_data['swap'] = str(data['ansible_swaptotal_mb']) + 'MB'
                    cmdb_data['status'] = 0
                    data_list.append(cmdb_data)    
            elif  k == "unreachable":
                for x,y in v.items():
                    cmdb_data = {}
                    cmdb_data['status'] = 1
                    cmdb_data['ip'] = x
                    data_list.append(cmdb_data)
        if data_list:
            return  data_list
        else:
            return False 
    
    def handle_cmdb_crawHw_data(self,data):
        data_list = []
        for k,v in json.loads(data).items():
            if k == "success":
                for x,y in v.items():
                    cmdb_data = {}
                    cmdb_data['ip'] = x
                    data = y.get('ansible_facts')
                    cmdb_data['mem_info'] = data.get('ansible_mem_detailed_info')
                    cmdb_data['disk_info'] = data.get('ansible_disk_detailed_info')
                    data_list.append(cmdb_data)
        if data_list:
            return  data_list
        else:
            return False                    
                    
    def handle_model_data(self,data,module_name,module_args=None):
        '''处理ANSIBLE 模块输出内容'''
        module_data = json.loads(data)
        failed = module_data.get('failed')
        success = module_data.get('success')
        unreachable = module_data.get('unreachable')
        data_list = []
        if module_name == "raw":
            if failed:
                for x,y in failed.items():   
                    data = {}                  
                    data['ip'] = x
                    try:
                        data['msg'] = y.get('stdout').replace('\t\t','<br>').replace('\r\n','<br>').replace('\t','<br>')
                    except:
                        data['msg'] = None
                    if y.get('rc') == 0:
                        data['status'] = 'succeed' 
                    else:
                        data['status'] = 'failed'
                    data_list.append(data)
            elif success:
                for x,y in success.items(): 
                    data = {}                    
                    data['ip'] = x
                    try:
                        data['msg'] = y.get('stdout').replace('\t\t','<br>').replace('\r\n','<br>').replace('\t','<br>')
                    except:
                        data['msg'] = None
                    if y.get('rc') == 0:
                        data['status'] = 'succeed' 
                    else:
                        data['status'] = 'failed'  
                    data_list.append(data)
                    
        elif module_name == "ping":
            if success:
                for x,y in success.items():
                    data = {}
                    data['ip'] = x
                    if y.get('ping'):
                        data['msg'] = y.get('ping')
                        data['status'] = 'succeed'
                    data_list.append(data)                    
        else:
            if success:
                for x,y in success.items():
                    data = {}
                    data['ip'] = x
                    if y.get('invocation'):
                        data['msg'] = "Ansible %s with %s execute success." % (module_name,module_args)
                        data['status'] = 'succeed'
                    data_list.append(data) 
                    
            elif failed:
                for x,y in failed.items():   
                    data = {}                  
                    data['ip'] = x
                    data['msg'] = y.get('msg')
                    data['status'] = 'failed'
                    data_list.append(data)  
                                                  
        if unreachable:
            for x,y in unreachable.items(): 
                data = {}                    
                data['ip'] = x
                data['msg'] = y.get('msg')
                data['status'] = 'failed'  
                data_list.append(data)            
        if data_list:
            return  data_list
        else:
            return False 
      
        
if __name__ == '__main__':
    resource = [
                 {"hostname": "192.168.1.235"},
                 {"hostname": "192.168.1.234"},
                 {"hostname": "192.168.1.233"},
                 ]
#     resource =  { 
#                     "dynamic_host": { 
#                         "hosts": [
#                                     {"hostname": "192.168.1.34", "port": "22", "username": "root", "password": "jinzhuan2015"},
#                                     {"hostname": "192.168.1.130", "port": "22", "username": "root", "password": "jinzhuan2015"}
#                                   ], 
#                         "vars": {
#                                  "var1":"ansible", 
#                                  "var2":"saltstack"
#                                  } 
#                     } 
#                 } 
    
    rbt = ANSRunner(resource,redisKey='1')
    rbt.run_model(host_list=["192.168.1.235","192.168.1.234","192.168.1.233"],module_name='yum',module_args="name=htop state=present")
#     data = rbt.get_model_result()
#     print data
#     print data
#     print rbt.handle_model_data(data, 'synchronize', module_args='src=/data/webserver/VManagePlatform/ dest=/data/webserver/VManagePlatform/ compress=yes delete=yes recursive=yes')
    #rbt.run_model(host_list=["192.168.1.34","192.168.1.130","192.168.1.1"],module_name='ping',module_args="")
#     rbt.run_playbook(["192.168.1.34","192.168.1.130"],playbook_path='/etc/ansible/api/init/system_init.yml')
#     data = rbt.get_model_result()
#     data = rbt.get_playbook_result()
#     print data
#     print rbt.handle_playbook_data_to_html(data)
    #print rbt.handle_model_data(module_name='copy',module_args="src=/root/git.log dest=/tmp/test.txt",data=data)

