#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os,re
from collections import Mapping,namedtuple
from ansible import constants
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.vars import load_extra_vars
from ansible.utils.vars import load_options_vars
from .callback import *
from .inventory import get_inventory




                    
            
class ANSRunner(object):  
    
    
    def __init__(
        self,
        hosts=constants.DEFAULT_HOST_LIST,
        module_name=constants.DEFAULT_MODULE_NAME,   
        module_args=constants.DEFAULT_MODULE_ARGS,    
        forks=constants.DEFAULT_FORKS,               
        timeout=constants.DEFAULT_TIMEOUT,            
        pattern="all",                       
        remote_user=constants.DEFAULT_REMOTE_USER,   
        module_path=None,
        connection_type="smart",
        become=True,
        become_method='sudo',
        become_user='root',
        check=False,
        passwords=None,
        extra_vars = None,
        private_key_file=None,
        listtags=False,
        listtasks=False,
        listhosts=False,
        ssh_common_args=None,
        ssh_extra_args=None,
        sftp_extra_args=None,
        scp_extra_args=None,
        verbosity=None,
        syntax=False,        
        websocket=None,
        mysql=None
    ):
        self.Options = namedtuple("Options", [
                                                'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
                                                'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
                                                'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args',
                                                'become', 'become_method', 'become_user', 'verbosity', 'check',
                                                'extra_vars', 'diff'
                                                ]
                                            )
        self.results_raw = {}
        self.pattern = pattern
        self.module_name = module_name
        self.module_args = module_args
        self.gather_facts = 'no'
        self.options = self.Options(
            listtags=listtags,
            listtasks=listtasks,
            listhosts=listhosts,
            syntax=syntax,
            timeout=timeout,
            connection=connection_type,
            module_path=module_path,
            forks=forks,
            remote_user=remote_user,
            private_key_file=private_key_file,
            ssh_common_args=ssh_common_args or "",
            ssh_extra_args=ssh_extra_args or "",
            sftp_extra_args=sftp_extra_args,
            scp_extra_args=scp_extra_args,
            become=become,
            become_method=become_method,
            become_user=become_user,
            verbosity=verbosity,
            extra_vars=extra_vars or [],
            check=check,
            diff=False
        )
        self.websocket = websocket      
        self.mysql = mysql 
        self.loader = DataLoader()
        self.inventory = get_inventory(hosts)
        self.variable_manager = VariableManager(self.loader, self.inventory)
        self.variable_manager.extra_vars = load_extra_vars(loader=self.loader, options=self.options)
        self.variable_manager.options_vars = load_options_vars(self.options, "")
        self.passwords = passwords or {}
        
  
    def run_model(self,host_list, module_name, module_args):
        self.callback = AdHoccallback(self.websocket,self.mysql)  
        play_source = dict(
            name="Ansible Ad-hoc",
            hosts=host_list,
            gather_facts=self.gather_facts,
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )        
        play = Play().load(play_source,loader=self.loader,variable_manager=self.variable_manager)
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.callback
            )        
            tqm._stdout_callback = self.callback  
            constants.HOST_KEY_CHECKING = False #关闭第一次使用ansible连接客户端是输入命令

            tqm.run(play)  
        except Exception as err: 
            logger.error(msg="run model failed: {err}".format(err=str(err)))
            if self.websocket:self.websocket.send(str(err))              
        finally:  
            if tqm is not None:  
                tqm.cleanup()  
            if self.loader:
                self.loader.cleanup_all_tmp_files()  
  
    def run_playbook(self, host_list, playbook_path,extra_vars=dict()): 
        """ 
        run ansible palybook 
        """   
        try: 
            self.callback = Playbookcallback(self.websocket,self.mysql) 
            extra_vars['host'] = ','.join(host_list)
            self.variable_manager.extra_vars = extra_vars            
            executor = PlaybookExecutor(  
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager, loader=self.loader,  
                options=self.options, passwords=self.passwords,  
            )  
            executor._tqm._stdout_callback = self.callback  
            constants.HOST_KEY_CHECKING = False #关闭第一次使用ansible连接客户端是输入命令
            constants.DEPRECATION_WARNINGS = False
            constants.RETRY_FILES_ENABLED = False  
            executor.run()  
        except Exception as err: 
            logger.error(msg="run playbook failed: {err}".format(err=str(err)))
            if self.websocket:self.websocket.send(str(err))       
            return False
            
    def get_model_result(self):  
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}  
        
        for host, result in self.callback.host_ok.items():  
            self.results_raw['success'][host] = result._result  


        for host, result in self.callback.host_failed.items():  
            self.results_raw['failed'][host] = result._result 

  
        for host, result in self.callback.host_unreachable.items():  
            self.results_raw['unreachable'][host]= result._result 

        return json.dumps(self.results_raw,indent=4)  

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
                    cmdb_data['ram_total'] = int(data['ansible_memtotal_mb'])/1000
                    cmdb_data['disk_total'] = int(disk_size)
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
                    cmdb_data['swap'] = int(data['ansible_swaptotal_mb'])/1000 
                    #获取网卡资源
                    nks = []
                    for nk in data.keys():
                        if re.match(r"^ansible_(eth|bind|eno|ens|em)\d+?",nk):
                            device = data.get(nk).get('device')
                            try:
                                address = data.get(nk).get('ipv4').get('address')
                            except:
                                address = 'unkown'
                            macaddress = data.get(nk).get('macaddress')
                            module = data.get(nk).get('module')
                            mtu = data.get(nk).get('mtu')
                            if data.get(nk).get('active'):active = 1
                            else:active = 0
                            nks.append({"device":device,"address":address,"macaddress":macaddress,"module":module,"mtu":mtu,"active":active})
                    cmdb_data['status'] = 0
                    cmdb_data['nks'] = nks
                    data_list.append(cmdb_data)   
            elif  k == "unreachable":
                for x,y in v.items():
                    cmdb_data = {}
                    cmdb_data['status'] = 1
                    cmdb_data['ip'] = x
                    data_list.append(cmdb_data)                     
        return  data_list

    
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
        return  data_list
                
                    
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
                        data['msg'] = y.get('stderr').replace('\t\t','<br>').replace('\r\n','<br>').replace('\t','<br>')
                    except:
                        data['msg'] = None
                    if y.get('rc') == 0:
                        data['status'] = 'succeed' 
                    else:
                        data['status'] = 'failed'
                    data_list.append(data)
            if success:
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
                    data['msg'] = "success"
                    data['ip'] = x
                    if y.get('invocation') and y.get('stdout'):
                        data['msg'] = y.get('stdout').replace('\t\t','<br>').replace('\r\n','<br>').replace('\t','<br>').replace('\n','<br>')                          
                    data['status'] = 'succeed'    
                    data_list.append(data) 
                    
            if failed:
                for x,y in failed.items():                      
                    data = {}   
                    data['msg'] = "failed"               
                    data['ip'] = x
                    if y.get('stderr'):
                        data['msg'] = y.get('stderr') + y.get('msg')
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
    
    rbt = ANSRunner(resource)
    rbt.run_model(host_list=["192.168.1.235","192.168.1.234","192.168.1.233"],module_name='ping',module_args="")
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