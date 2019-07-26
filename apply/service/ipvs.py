#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from dao.assets import AssetsSource
from utils.ansible.runner import ANSRunner

class IPVSRunner(AssetsSource):
    
    def __init__(self,vip=None,realserver=None,ws=None):
        super(IPVSRunner, self).__init__()     
        
        self.ws = ws
        
        self.vip = vip
            
        self.realserver = realserver    
 
    
    def run(self,func,request=None):
        if hasattr(self,func):
            funcs= getattr(self,func)
            return funcs(request)
    
    def get_vip_ans(self):
        if isinstance(self.vip, list):
            sList,resource = self.idSourceList([ x.ipvs_assets.id for x in self.vip])
            return sList,ANSRunner(resource)    
        else:         
            sList,resource = self.idSource(self.vip.ipvs_assets.id)
            return sList,ANSRunner(resource) 
        return [],{} 

    def get_rs_ans(self):
        if isinstance(self.realserver, list):
            sList,resource = self.idSourceList([ x.ipvs_vip.ipvs_assets.id for x in self.realserver])
            return sList,ANSRunner(resource)    
        else:         
            sList,resource = self.idSource(self.realserver.ipvs_vip.ipvs_assets.id)
            return sList,ANSRunner(resource)
        return [],{} 
                 
    def add_vip(self,request=None):       
        host_list,AnsRbt = self.get_vip_ans()
        cmd = self.vip.add_vip()
        rs_cmd = ''
        if hasattr(self.vip,'ipvs_rs'):
            for ds in self.vip.ipvs_rs.all():
                if ds.is_active == 1:rs_cmd = rs_cmd +';'+ ds.add_realsever()
            cmd = cmd + rs_cmd        
        return self.run_ans_cmd(host_list, AnsRbt, cmd)

  
                    
    def modf_vip(self,request=None):
        if self.vip.is_active == 1:
            host_list,AnsRbt = self.get_vip_ans()
            return self.run_ans_cmd(host_list, AnsRbt, self.vip.modf_vip())                   

    def del_vip(self,request=None):       
        host_list,AnsRbt = self.get_vip_ans()
        return self.run_ans_cmd(host_list, AnsRbt, self.vip.del_vip())
               

    def add_rs(self,request=None):
        if self.vip.is_active == 1:
            host_list,AnsRbt = self.get_rs_ans()
            return self.run_ans_cmd(host_list, AnsRbt, self.realserver.add_realsever())
        

    def modf_rs(self,request=None):
        if self.vip.is_active == 1:
            cmd = self.realserver.modf_realsever()
            if request.get('is_active'):
                if int(request.get('is_active')) == 0:
                    cmd = self.realserver.del_realsever()
                elif int(request.get('is_active')) == 1:
                    cmd = self.realserver.add_realsever()
            host_list,AnsRbt = self.get_rs_ans()
            return self.run_ans_cmd(host_list, AnsRbt, cmd)

            
    def del_rs(self,request=None):
        if self.vip.is_active == 1:
            host_list,AnsRbt = self.get_rs_ans()
            return self.run_ans_cmd(host_list, AnsRbt, self.realserver.del_realsever())  
        
    def batch_modf_rs(self,request=None):
        batch_result = ''
        host_list,AnsRbt = self.get_vip_ans()
        rsList = [ ds.id for ds in self.realserver ]
        for ds in self.vip:
#             print(ds.ipvs_assets.server_assets.ip,ds.vip)
            cmds = ''
            for rs in ds.ipvs_rs.all():
                if int(rs.is_active) == 1 and rs.id in rsList:
                    cmds =  rs.modf_realsever() + '&&' + cmds
                    
            if len(cmds) > 0:
                result = self.run_ans_cmd(ds.ipvs_assets.server_assets.ip,AnsRbt,cmds[:-1])
            
                if result:batch_result += batch_result + str(result)
            
        if len(batch_result) > 0:return batch_result
        

    def batch_del_rs(self,request=None):
        batch_result = ''
        host_list,AnsRbt = self.get_vip_ans()
        rsList = [ ds.id for ds in self.realserver ]
        for ds in self.vip:
#             print(ds.ipvs_assets.server_assets.ip,ds.vip)
            cmds = ''
            for rs in ds.ipvs_rs.all():
                if int(rs.is_active) == 1 and rs.id in rsList:
                    cmds =  rs.del_realsever() + '&&' + cmds
            
            if len(cmds) > 0:
                result = self.run_ans_cmd(ds.ipvs_assets.server_assets.ip,AnsRbt,cmds[:-1])
                
                if result:batch_result += batch_result + str(result)
            
        if len(batch_result) > 0:return batch_result

    def vip_rate(self,request=None):
        host_list,AnsRbt = self.get_vip_ans()
        AnsRbt.run_model(host_list, 'shell', self.vip.rate_vip())
        return AnsRbt.handle_model_data(AnsRbt.get_model_result(), 'shell', self.vip.rate_vip())        
        
    def vip_stats(self,request=None):                        
        host_list,AnsRbt = self.get_vip_ans()
        AnsRbt.run_model(host_list, 'shell', self.vip.stats_vip())
        return AnsRbt.handle_model_data(AnsRbt.get_model_result(), 'shell', self.vip.stats_vip())  
                
            
    def run_ans_cmd(self,host_list,AnsRbt,cmd): 
#         print(cmd)
        AnsRbt.run_model(host_list, 'shell', cmd)
        result = AnsRbt.handle_model_data(AnsRbt.get_model_result(), 'shell', cmd)
        for ds in result:
            if ds.get('status') != 'succeed':return result  