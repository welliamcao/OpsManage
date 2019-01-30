#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json
import ansible.runner
import ansible.playbook
from ansible import callbacks
from ansible import utils

class ANSTools(object): 
    def __init__(self,pattern=None,module_name=None,module_args=None,playbook=None,host_list=None):
        self.module_name = module_name
        self.module_args = module_args
        self.pattern = pattern   
        self.playbook = playbook 
        self.host_list = host_list  
         
    def cmdb(self):
        runner = ansible.runner.Runner(
               module_name = self.module_name,
               module_args = self.module_args,
               pattern = self.pattern,
               forks = 100
            )
        data_list = []
        data = runner.run()
        data = json.dumps(data,indent=4)
        for k,v in json.loads(data).items():
            if k == "contacted":
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
            elif  k == "dark":
                for x,y in v.items():
                    cmdb_data = {}
                    cmdb_data['status'] = 1
                    cmdb_data['ip'] = x
                    data_list.append(cmdb_data)
        if data_list:
            return  data_list
        else:
            return False
            
    def model(self):
        runner = ansible.runner.Runner(
               module_name = self.module_name,
               module_args = self.module_args,
               pattern = self.pattern,
               host_list = self.host_list,
               forks = 100
            )
        data_list = []
        data = runner.run()
        data = json.dumps(data,indent=4)
        for k,v in json.loads(data).items():
            if k == "contacted":
                if self.module_name == "raw":
                    for x,y in v.items():  
                        data = {}                      
                        data['ip'] = x
                        data['msg'] = y.get('stdout').replace('\t\t','<br>').replace('\r\n','<br>').replace('\t','<br>')
                        if y.get('rc') == 0:
                            data['status'] = 'succeed' 
                        else:
                            data['status'] = 'failed' 
                        data_list.append(data)
                elif self.module_name == "ping":
                    for x,y in v.items():
                        data = {}
                        data['ip'] = x
                        if y.get('failed'):
                            data['msg'] = y.get('msg')
                            data['status'] = 'failed'
                        else:
                            data['msg'] = y.get('ping')
                            data['status'] = 'succeed' 
                        data_list.append(data)
                else:
                    for x,y in v.items():
                        data = {}                      
                        data['ip'] = x
                        if y.get('failed'):
                            data['msg'] = y.get('msg')
                            data['status'] = 'failed'                            
                        else:
                            data['msg'] = "%s %s succeed" % (self.module_name,self.module_args)
                            data['status'] = 'succeed' 
                        data_list.append(data)                        
                    
            elif  k == "dark":
                for x,y in v.items():
                    data = {}
                    data['status'] = 'failed'
                    data['ip'] = x
                    data['msg'] = y.get('msg')
                    data_list.append(data)                       
        if data_list:
            return  data_list
        else:
            return False       
    
    def conf(self):
        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.DefaultRunnerCallbacks()
        res = ansible.playbook.PlayBook(
                    playbook = self.playbook, #'/etc/ansible/playbooks/user.yml',
                    stats = stats,#输出详细结果
                    callbacks = playbook_cb,
                    runner_callbacks = runner_cb,
                    host_list = self.host_list,
                    extra_vars = self.module_args
            ).run()
        data = json.dumps(res,indent=4)
        data_list = []    
        for k,v in json.loads(data).items():
            data = {} 
            for x,y in v.items():  
                data['ip'] = k 
                data[x] = y
            data_list.append(data)   
        if data_list:
            return  data_list
        else:
            return False  