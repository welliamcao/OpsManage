#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
from ansible.inventory.host import Host
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.errors import AnsibleError, AnsibleParserError

class HostInventory(Host):
    def __init__(self, host_data):
        self.host_data = host_data
        hostname = host_data.get('hostname') or host_data.get('ip')
        port = host_data.get('port') or 22
        super(HostInventory,self).__init__(hostname, port)
        self.__set_required_variables()
        self.__set_extra_variables()

                    
    def __set_required_variables(self):
        host_data = self.host_data
        self.set_variable('ansible_host', host_data['ip'])
        self.set_variable('ansible_port', host_data['port'])
        if host_data.get('username'):
            self.set_variable('ansible_user', host_data['username'])
        if host_data.get('password'):
            self.set_variable('ansible_ssh_pass', host_data['password'])
        if host_data.get('private_key'):
            self.set_variable('ansible_ssh_private_key_file', host_data['private_key'])
        become = host_data.get("become", False)
        if become:
            self.set_variable("ansible_become", True)
            self.set_variable("ansible_become_method", become.get('method', 'sudo'))
            self.set_variable("ansible_become_user", become.get('user', 'root'))
            self.set_variable("ansible_become_pass", become.get('pass', ''))
        else:
            self.set_variable("ansible_become", False)
            
    def __set_extra_variables(self):
        for k, v in self.host_data.get('vars', {}).items():
            self.set_variable(k, v)
            
    def __repr__(self):
        return self.name


class DynamicInventory(InventoryManager):
    def __init__(self, resource=None):
        self.resource = resource
        self.loader = DataLoader()
        self.variable_manager = VariableManager()
        super(DynamicInventory,self).__init__(self.loader)

        
    def get_groups(self):
        return self._inventory.groups
    
    def get_group(self, name):
        return self._inventory.groups.get(name, None)
    
    def parse_sources(self, cache=False):
        group_all = self.get_group('all')
        ungrouped = self.get_group('ungrouped')
        if isinstance(self.resource, list):
            for host_data in self.resource:
                host = HostInventory(host_data=host_data)
                self.hosts[host_data['hostname']] = host
                groups_data = host_data.get('groups')
                if groups_data:
                    for group_name in groups_data:
                        group = self.get_group(group_name)
                        if group is None:
                            self.add_group(group_name)
                            group = self.get_group(group_name)
                        group.add_host(host)
                else:
                    ungrouped.add_host(host)
                group_all.add_host(host)
                
        elif isinstance(self.resource, dict):
            for k,v in self.resource.items():
                group = self.get_group(k)
                if group is None:
                    self.add_group(k)  
                    group = self.get_group(k)   
                if 'hosts' in v:
                    if not isinstance(v['hosts'], list):
                        raise AnsibleError("You defined a group '%s' with bad data for the host list:\n %s" % (group, v))
                    for host_data in v['hosts']:
                        host = HostInventory(host_data=host_data)
                        self.hosts[host_data['hostname']] = host
                        group.add_host(host)   
                                        
                if 'vars' in v:
                    if not isinstance(v['vars'], dict):
                        raise AnsibleError("You defined a group '%s' with bad data for variables:\n %s" % (group, v))
        
                    for x, y in v['vars'].items():
                        self._inventory.groups[k].set_variable( x, y)

                                          
    def get_matched_hosts(self, pattern):
        return self.get_hosts(pattern)
    
def get_inventory(hosts):
    if isinstance(hosts, str):
        if os.path.isfile(hosts):
            return InventoryManager(loader=DataLoader(), sources=hosts)
        else:
            return False
    else:
        return DynamicInventory(hosts)    