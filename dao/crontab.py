#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
#coding: utf8
from sched.models import Cron_Config
from utils.logger import logger
from .assets import AssetsSource,AssetsBase
from django.http import QueryDict
import os,uuid
from django.core.files.storage import FileSystemStorage
from utils.ansible.runner import ANSRunner



class CrontabManage(AssetsBase):
    def __init__(self):
        super(CrontabManage, self).__init__()  
        self.assets_source = AssetsSource()
        self.fList = []
        self.sList = []
    
    def crontab(self,request):
        if request.method == 'GET':cid = request.GET.get('id')
        elif request.method == 'POST':cid = request.POST.get('id')
        elif request.method in ['PUT','DELETE']:cid = QueryDict(request.body).get('id')
        try:
            cron = Cron_Config.objects.get(id=cid)
            return cron
        except Exception as ex:
            logger.warn(msg="获取计划任务失败: {ex}".format(ex=ex))
            return False    
        
    def get_crontab(self,request):
        data = {}
        cron = self.crontab(request)
        if isinstance(cron, Cron_Config):
            data = self.convert_to_dict(cron)
            if cron.cron_type == 'online':
                cron_script = os.getcwd() + '/upload/' + str(cron.cron_script)
                if os.path.exists(cron_script):
                    content = ''
                    with open(cron_script,"r") as f:
                        for line in f.readlines(): 
                            content =  content + line 
                    data['cron_script'] = content  
        return data
    
    def crontabList(self):
        return Cron_Config.objects.all()
        
    def get_assets_list(self,request):
        assetsList = []
        for ids in request.POST.get('custom').split(","):
            assetsList.append(self.assets(ids))
        return assetsList
    
    def get_assets_source(self,request):   
        return self.assets_source.allowcator(request.POST.get('server_model'),request)
    
    def save_file(self,request):
        cron_script = None
        ram_str = uuid.uuid4().hex[0:8]
        if request.POST.get('cron_type') == 'online': 
            fileName = '/upload/cron/cron-{ram_str}'.format(ram_str=ram_str) 
            filePath = os.getcwd() + fileName
            self.saveScript(content=request.POST.get('cron_script'),filePath=filePath)    
            cron_script = fileName.replace('/upload/','')
        elif request.POST.get('cron_type') == 'upload':
            cron_script = request.FILES['cron_script']
            location = os.getcwd() + '/upload/cron/'
            fs = FileSystemStorage(location= location)
            fs.save(cron_script.name + ram_str, cron_script) 
            cron_script = fs.path(cron_script.name).replace(os.getcwd() + '/upload/','') + ram_str 
        return cron_script       
             
    def create_crontab(self,request):
        slist = []
        for assets in self.get_assets_list(request):              
            try:
                cron = Cron_Config.objects.create(
                                            cron_server = assets,
                                            cron_minute = request.POST.get('cron_minute'),
                                            cron_hour = request.POST.get('cron_hour'),
                                            cron_day = request.POST.get('cron_day'),
                                            cron_week = request.POST.get('cron_week'),
                                            cron_month = request.POST.get('cron_month'),
                                            cron_user = request.POST.get('cron_user'),
                                            cron_name = request.POST.get('cron_name'),
                                            cron_type = request.POST.get('cron_type'),
                                            cron_log_path = request.POST.get('cron_log_path'),
                                            cron_command = request.POST.get('cron_command'),
                                            cron_script = self.save_file(request),#request.POST.get('cron_script'),
                                            cron_script_path =  request.POST.get('cron_script_path'),
                                            cron_status = request.POST.get('cron_status',0),
                                        )
                self.sList.append({'assets':assets,'cron':cron})
            except Exception as ex:
                self.fList.append({'assets':assets.server_assets.ip,'result':str(ex)})
                logger.warn(msg="添加计划任务失败: {ex}".format(ex=ex))  
        if len(self.sList) > 0:
            assetsList = [ s.get('assets') for s in self.sList ]
            sList,resource = self.assets_source.source(assetsList)
            ANS = ANSRunner(resource)               
            if cron.cron_type in ['upload','online']:
                self.rsync_script(ANS,sList)
                self.rsync_cron(ANS,sList)
            elif cron.cron_type == 'command':
                self.rsync_cron(ANS,sList)
            for s in self.sList:
                if hasattr(s.get('assets'),'server_assets') and s.get('assets').server_assets.ip \
                    not in [ f.get('assets') for f in self.fList ]:
                    slist.append({'assets':s.get('assets').server_assets.ip,'result':'success'})
        return self.fList + slist   
    
    def update_crontab(self,request):
        slist = []
        cron = self.crontab(request)        
        try:
            if cron.cron_type == 'online':
                filePath = os.getcwd() + '/upload/' + str(cron.cron_script)
                self.saveScript(content=QueryDict(request.body).get('cron_script'),filePath=filePath)            
            cron.cron_minute = QueryDict(request.body).get('cron_minute')
            cron.cron_hour = QueryDict(request.body).get('cron_hour')
            cron.cron_day = QueryDict(request.body).get('cron_day')
            cron.cron_week = QueryDict(request.body).get('cron_week')
            cron.cron_month = QueryDict(request.body).get('cron_month')
            cron.cron_log_path = QueryDict(request.body).get('cron_log_path')
            cron.cron_script_path = QueryDict(request.body).get('cron_script_path')
            cron.cron_command = QueryDict(request.body).get('cron_command')
            cron.save()
            self.sList.append({'assets':cron.cron_server,'cron':cron})
        except Exception as ex:
            logger.warn(msg="修改计划任务失败: {ex}".format(ex=ex))
            return str(ex)  
        sList,resource = self.assets_source.idSource(cron.cron_server.id)
        ANS = ANSRunner(resource)               
        if cron.cron_type in ['upload','online']:
            self.rsync_script(ANS,sList)
            self.rsync_cron(ANS,sList)
        elif cron.cron_type == 'command':
            self.rsync_cron(ANS,sList)
        for s in self.sList:
            if hasattr(s.get('assets'),'server_assets') and s.get('assets').server_assets.ip \
                not in [ f.get('assets') for f in self.fList ]:
                slist.append({'assets':s.get('assets').server_assets.ip,'result':'success'})
        return self.fList + slist         
    
    def view_logs(self,request):
        result = []
        cron = self.crontab(request) 
        if isinstance(cron, Cron_Config):
            sList,resource = self.assets_source.idSource(cron.cron_server.id)
            if cron.cron_log_path == '/var/log/cron':module_args="""grep '{cron_command}' {cron_log_path}| tail -n 10 """.format(cron_command=cron.cron_command,cron_log_path=cron.cron_log_path) 
            else:module_args="""tail -n 100 {cron_log_path}""".format(cron_log_path=cron.cron_log_path) 
            ANS = ANSRunner(resource)
            ANS.run_model(host_list=sList, module_name='raw', module_args=module_args) 
            result = ANS.handle_model_data(ANS.get_model_result(), 'raw', module_args)                     
        return result  
    
    def delete_crontab(self,request):
        cron = self.crontab(request) 
        if isinstance(cron, Cron_Config):
            sList,resource = self.assets_source.idSource(cron.cron_server.id)
            ANS = ANSRunner(resource)    
            module_args="""name={name} state=absent""".format(name=cron.cron_name)  
            ANS.run_model(host_list=sList,module_name="cron",module_args=module_args) 
            result = ANS.handle_model_data(ANS.get_model_result(), 'cron', module_args)  
            for ds in result:
                if ds.get('status') == 'succeed':
                    try:
                        cron.delete()
                    except Exception as ex:
                        logger.error(msg="删除计划任务失败: {ex}".format(ex=ex))
                        return str(ex)
                else:
                    return result[0].get('msg')
        return True
    
    def disabled(self,request):   
        cron = self.crontab(request) 
        if isinstance(cron, Cron_Config):
            sList,resource = self.assets_source.idSource(cron.cron_server.id)
            ANS = ANSRunner(resource)    
            module_args="""name={name} state=absent""".format(name=cron.cron_name)  
            ANS.run_model(host_list=sList,module_name="cron",module_args=module_args) 
            result = ANS.handle_model_data(ANS.get_model_result(), 'cron', module_args)  
            for ds in result:
                if ds.get('status') == 'succeed':
                    try:
                        cron.cron_status = 2
                        cron.save()
                    except Exception as ex:
                        logger.error(msg="删除计划任务失败: {ex}".format(ex=ex))
                        return str(ex)
                else:
                    return result[0].get('msg')            
        return True

    def enable(self,request):   
        cron = self.crontab(request) 
        if isinstance(cron, Cron_Config):
            sList,resource = self.assets_source.idSource(cron.cron_server.id)
            ANS = ANSRunner(resource)    
            module_args = """name='{name}' minute='{minute}' hour='{hour}' day='{day}' weekday='{weekday}' month='{month}' user='{user}' job='{job}'""".format(
                                                                                                name=cron.cron_name,minute=cron.cron_minute,
                                                                                                hour=cron.cron_hour,day=cron.cron_day,
                                                                                                weekday=cron.cron_week,month=cron.cron_month,
                                                                                                user=cron.cron_user,job=cron.cron_command
                                                                                                )   
            ANS.run_model(host_list=sList, module_name='cron', module_args=module_args)
            result = ANS.handle_model_data(ANS.get_model_result(), 'cron',module_args)  
            for ds in result:
                if ds.get('status') == 'succeed':
                    try:
                        cron.cron_status = 1
                        cron.save()
                    except Exception as ex:
                        logger.error(msg="删除计划任务失败: {ex}".format(ex=ex))
                        return str(ex)
                else:
                    return result[0].get('msg')            
        return True
                             
        
    def rsync_script(self,ANS,sList):
        cronList =  [ s.get('cron') for s in self.sList ]
        cron = cronList[0]        
        src = os.getcwd() + '/upload/' + str(cron.cron_script)
        module_args = """src={src} dest={dest} owner={user} group={user} mode=755""".format(src=src,dest=cron.cron_script_path,user=cron.cron_user)
        ANS.run_model(host_list=sList, module_name='copy', module_args=module_args)
        result = ANS.handle_model_data(ANS.get_model_result(), 'copy',module_args)     
        fList,sList = self.format_result(result)  
        self.update_cron_status(cronList, fList, sList) 
        
    def rsync_cron(self,ANS,sList):
        cronList =  [ s.get('cron') for s in self.sList ]
        cron = cronList[0]
        module_args = """name='{name}' minute='{minute}' hour='{hour}' day='{day}' weekday='{weekday}' month='{month}' user='{user}' job='{job}'""".format(
                                                                                            name=cron.cron_name,minute=cron.cron_minute,
                                                                                            hour=cron.cron_hour,day=cron.cron_day,
                                                                                            weekday=cron.cron_week,month=cron.cron_month,
                                                                                            user=cron.cron_user,job=cron.cron_command
                                                                                            )   
        ANS.run_model(host_list=sList, module_name='cron', module_args=module_args)
        result = ANS.handle_model_data(ANS.get_model_result(), 'cron',module_args)        
        fList,sList = self.format_result(result)            
        self.update_cron_status(cronList, fList, sList)
    
    def update_cron_status(self,cronList,fList,sList):
        for cron in cronList:
            if hasattr(cron.cron_server,'server_assets'):
                if cron.cron_server.server_assets.ip in fList:
                    cron.cron_status = 0
                    cron.save()
                elif cron.cron_server.server_assets.ip in sList:
                    cron.cron_status = 1
                    cron.save()        
    
    def format_result(self,result):
        fList,sList = [],[]
        for ds in result:
            if ds.get('status') in ['failed','unreachable'] :
                if ds.get('ip') not in [ f.get('assets') for f in self.fList]:
                    fList.append(ds.get('ip'))  
                    self.fList.append({'assets':ds.get('ip'),'result':ds.get('msg')}) 
            elif ds.get('status') == 'succeed':sList.append(ds.get('ip'))
        return fList,sList