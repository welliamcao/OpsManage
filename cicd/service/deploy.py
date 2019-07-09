#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import time,uuid,json,os
from utils.deploy.git import GitTools
from cicd.models import Project_Config
from OpsManage.settings import WORKSPACES
from utils.logger import logger
from utils import base
from cicd.service.utils import tar_excludes_format,tar_includes_format
from dao.assets import AssetsSource
from utils.ansible.runner import ANSRunner



class DeployRunner(AssetsSource):
    dir_release, dir_webroot,exclude = None, None, None
    version_package, release_version = None, None
    deploy_status,failed_count = True, 0
    flist = []
    
    def __init__(self,apps_id=None,task=None,ws=None):
        super(DeployRunner, self).__init__()  
        self.ws = ws
        if task:
            self.task = task
            try: 
                self.apps = self.task.project 
                if self.apps.project_model == 'branch':
                    version = self.task.commit_id
                else: 
                    version = self.task.tag
            except:
                self.apps = None     
                                         
            self.release_version = '{code_base}{version}/'.format(
                code_base = WORKSPACES.rstrip('/') + '/deploy/' + self.apps.project_name + '/' + self.apps.project_env + '/',                                                              
                version=version
            )
            
            self.version_package = '{packname}{timestamp}.tar.gz'.format(
                packname =  self.apps.project_name + '-' + self.apps.project_env + '-',                                                              
                timestamp=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
            )
                       
        if apps_id:
            self.apps_id = apps_id
            self.apps = self.get_apps()
            self.version = GitTools(self.apps.project_repo_dir)                         

    
    def update_task_status(self,status):
        try:
            self.task.status = status
            self.task.save()
        except Exception as ex:
            logger.error("更新部署状态失败：{ex}".format(ex=str(ex)))       
    
    def deploy_workflow(self):
        if self.apps.project_type == 'compile':
            return  ["pre_deploy","post_deploy","package_deploy","pre_release","release","post_release"]
        else:
            return ["pre_deploy","package_deploy","pre_release","release","post_release"]        
    
    def rollback_workflow(self):
        return ["pre_release","release","post_release"]
    
    def get_apps(self):
        try:
            return Project_Config.objects.get(id=self.apps_id)
        except Exception as ex:
            logger.error("获取项目失败：{ex}".format(ex=str(ex)))
            return False  
               
    def list_branch(self):
        return self.version.branch() 

    def list_tag(self):
        return self.version.tag()    
    
    def list_commits(self,branch):
        return self.version.commits(branch)
        
    def init_apps(self):
        return self.version.init(url=self.apps.project_address)
    
    def checkout_branch(self, branch):
        return self.version.checkout_to_branch(branch)
    
    def checkout_commit(self, branch, commit):
        self.checkout_branch(branch=branch)
        return self.version.reset(path=self.apps.project_repo_dir, commintId=commit)
    
    def checkout_tag(self, tag):
        return self.version.checkout_to_tag(tag)   
    
    def cleanup_tmp_dir(self):
        if os.path.exists(self.release_version) is True:
            cmd = "rm -rf {dir}".format(dir=self.release_version)
            base.cmds(cmd)
    
    def judge_servers(self,hostList):
        success_server = list(set(hostList).difference(set(self.flist)))
        if len(success_server) > 0:return success_server
        else:
            self.ws.send(json.dumps({"progress":"summary","status":"error","msg":"没有可用的主机"}))              
            self.ws.disconnect(1000)              
                                            
    def handle_result(self,progress,result):
        if isinstance(result, list):
            for ds in result:
                if ds.get("status") != "succeed":
                    msg = '<strong><font color="red">' + ds.get("ip")+ '</font></strong><br>' + ds.get("msg")
                    self.update_task_status(status='已失败')
                    self.failed_count += 1
                    if ds.get("ip") not in self.flist:self.flist.append(ds.get("ip"))
                else:
                    msg = '<strong>' + ds.get("ip")+ '</strong><br>' + ds.get("msg")    
                self.ws.save_deploy_logs(key=progress, msg=msg, title=progress, task_id=self.task.task_id, status=ds.get("status")) 
                self.ws.send(json.dumps({
                                         "progress":progress,
                                         "msg":msg,
                                         "status":ds.get("status"),
                                         'ctime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                         'user':self.task.username}))
                
        elif isinstance(result, dict):
            if result.get("status") == "failed":   
                self.deploy_status = False 
                self.update_task_status(status='已失败')   
                self.ws.send(json.dumps({"progress":progress,"msg":result.get("msg"),"status":result.get("status")}))              
                self.ws.disconnect(1000)    
                       
            self.ws.save_deploy_logs(key=progress, msg=result.get("msg"), title=progress, task_id=self.task.task_id, status=result.get("status"))  
            
            if progress == "pre_deploy": 
                msg = self.task.get_version()
            else:
                msg = self.version_package.split("/")[-1]
                
            self.ws.send(json.dumps({
                                     "progress":progress,
                                     "msg":msg,
                                     "status":result.get("status"),
                                     'ctime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                     'user':self.task.username
                                     }))    
        
        
    def pre_deploy(self):
        '''检出代码'''
        try:
            self.init_apps()
                   
            repo = GitTools(self.release_version)
            
            self.handle_result("pre_deploy", self.version.rsync_to_release_version(self.release_version))   
            
            if self.apps.project_model == 'branch':
                repo.checkout_to_commit(branch=self.task.branch, commit=self.task.commit_id)
            else:
                repo.checkout_to_tag(tag=self.task.tag)   
                     
            self.update_task_status(status='进行中')    
        except Exception as ex:   
            self.handle_result("pre_deploy", {"msg":"代码检出失败:{ex}".format(ex=str(ex)),"status":"failed"}) 
            return False
                    
    def tar_code_package(self):
        self.version.mkdir(self.apps.project_dir)
        if self.apps.project_is_include == 0:
            exclude = tar_excludes_format(self.apps.project_exclude)
            cmds = "cd {release_version} && tar -zcf {desDir}{version_package} {exclude} .".format(
                                                                                            desDir=self.apps.project_dir,
                                                                                            release_version=self.release_version,
                                                                                            version_package=self.version_package,
                                                                                            exclude=exclude
                                                                                            )
        else:
            include = tar_includes_format(self.apps.project_exclude)
            cmds = "cd {release_version} && tar -zcf {desDir}{version_package} {include} ".format(
                                                                                                desDir=self.apps.project_dir,
                                                                                                release_version=self.release_version,
                                                                                                version_package=self.version_package,
                                                                                                include=include
                                                                                            )
        return base.cmds(cmds)    
        
    def post_deploy(self):
        '''编译代码'''
        # 用户自定义命令
        tmpFile = '/tmp/' + uuid.uuid4().hex[0:8] + '.sh'
        
        with open(tmpFile, 'w') as f:  
            f.write(self.apps.project_local_command)     
                             
        self.handle_result("post_deploy", base.cmds(cmds='dos2unix {tmpFile}'.format(tmpFile=tmpFile)))    
       
        self.handle_result("post_deploy", base.cmds(cmds='cd {project_repo_dir} && bash {tmpFile}'.format(tmpFile=tmpFile,project_repo_dir=self.release_version)))
        
    
    def package_deploy(self):    
        # 打包-排除|包含-文件发布 
        self.handle_result("package_deploy", self.tar_code_package()) 
        self.task.package =  self.apps.project_dir + self.version_package
        self.task.save()
        self.cleanup_tmp_dir()
    
    def pre_release(self):
        #目标服务器执行后续命令
        if self.apps.project_pre_remote_command:
            hostList, resource = self.idSourceList(ids=self.task.servers)  
            ansRbt = ANSRunner(resource) 
#             print(list(set(hostList).difference(set(self.flist))))
            ansRbt.run_model(host_list=self.judge_servers(hostList),module_name='raw',module_args=self.apps.project_pre_remote_command)
            #精简返回的结果
            dataList = ansRbt.handle_model_data(ansRbt.get_model_result() , 'raw', module_args=self.apps.project_remote_command) 
            self.handle_result("pre_release",dataList)       
        
    def release(self,package=None):
        if package:
            args = "src={srcDir} dest={desDir}".format(srcDir=package, desDir=self.apps.project_target_root)
        else:
            args = "src={srcDir} dest={desDir}".format(srcDir=self.apps.project_dir+self.version_package, desDir=self.apps.project_target_root)
        hostList, resource = self.idSourceList(ids=self.task.servers)
        ansRbt = ANSRunner(resource)
#         print(list(set(hostList).difference(set(self.flist))))
        ansRbt.run_model(host_list=self.judge_servers(hostList),module_name='unarchive',module_args=args)
        #精简返回的结果
        dataList = ansRbt.handle_model_data(ansRbt.get_model_result() , 'unarchive', module_args=args)        
        self.handle_result("release",dataList)


    def post_release(self): 
        #目标服务器执行后续命令
        if self.apps.project_remote_command:
            hostList, resource = self.idSourceList(ids=self.task.servers)  
            ansRbt = ANSRunner(resource) 
#             print(list(set(hostList).difference(set(self.flist))))
            ansRbt.run_model(host_list=self.judge_servers(hostList),module_name='raw',module_args=self.apps.project_remote_command)
            #精简返回的结果
            dataList = ansRbt.handle_model_data(ansRbt.get_model_result() , 'raw', module_args=self.apps.project_remote_command) 
            self.handle_result("post_release",dataList)

        
    def deploy(self):
        for func in self.deploy_workflow():     
            if hasattr(self,func):
                funcs= getattr(self,func)
                if self.deploy_status:funcs()
                
        if self.deploy_status:
            self.update_task_status(status='已部署')
         
    def rollback(self,package):  
        for func in self.rollback_workflow():     
            if hasattr(self,func):
                funcs= getattr(self,func)                
                if self.deploy_status:
                    if func == "release":
                        funcs(package)
                    else:
                        funcs()
                
        if self.deploy_status:
            self.update_task_status(status='已回滚')
    