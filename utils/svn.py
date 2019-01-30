#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
'''svn版本控制方法'''

import subprocess,os



class SvnTools(object):
       
    def reset(self,path,commintId):
        cmd = "cd {path} && svn update -r {commintId}".format(path=path,commintId=commintId)
        return subprocess.getstatusoutput(cmd)
    
    def log(self,path,number=None):
        vList = []
        cmd = "cd {path} && svn log -l {number} -q".format(path=path,number=number)
        status,result = subprocess.getstatusoutput(cmd)
        if status == 0: 
            for log in result.split('\n'):
                if log.startswith('---'):continue
                log = log.split('|')
                data = dict()
                data['ver'] = log[0].strip()
                data['user'] = log[1].strip()
                data['comid'] = log[0].strip()                
                log = log[2].strip().split(' ',2)
                ctime = log[0] + ' ' + log[1]
                data['desc'] = ctime
                vList.append(data)
        return vList 
    
    def branch(self,path):
        '''获取分支列表'''
        return []
    
    def tag(self,path):
        '''获取分支列表'''
        return []    

    def checkOut(self,path,name=None):
        cmd = "cd {path} && svn update".format(path=path)
        return subprocess.getstatusoutput(cmd) 
         
    def clone(self,url,dir,user=None,passwd=None):    
        if user and passwd:cmd = "svn co {url}  --username {user} --password {passwd} {dir}".format(url=url,user=user,passwd=passwd,dir=dir)
        else:cmd = "svn co {url}  {dir}".format(url=url,dir=dir)
        return subprocess.getstatusoutput(cmd)    
    
    def pull(self,path):     
        cmd = "cd {path} && svn update".format(path=path)           
        return subprocess.getstatusoutput(cmd)   
    
    def show(self,path,cid,branch=None): 
        cmd = "cd {path} && svn update && svn diff -r {cid}".format(path=path,cid=cid)
        return subprocess.getstatusoutput(cmd)    

    def mkdir(self,dir):
        if os.path.exists(dir) is False:os.makedirs(dir) 