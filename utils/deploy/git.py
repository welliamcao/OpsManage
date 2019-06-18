#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
'''git版本控制方法'''
import git,re
from git import Repo
import subprocess,os

class GitTools(object):
    path = None

    def __init__(self, path=None):
        self.path = path
        self.mkdir(self.path)   
        
    def is_git_dir(self):
        git_dir = self.path + '/.git'
        if os.path.isdir(git_dir):  
            if os.path.isdir(os.path.join(git_dir, 'hooks')) and os.path.isdir(os.path.join(git_dir, 'refs')) and \
                os.path.isdir(os.path.join(git_dir, 'objects')):
                return True
        return False  

    def clone(self, url):
        return Repo.clone_from(url, self.path)

    def pull(self):       
        repo = Repo(self.path)
        return repo.remote().pull()

    def init(self, url):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
        if self.is_git_dir():
            return self.pull()       
        else:
            return self.clone(url)
          
    def branch(self):
        '''git remote update origin --prune'''
        bList = []
        for name in Repo(self.path).remote().refs:
            if not str(name).strip().startswith('origin/HEAD'):
                bList.append(str(name).strip().lstrip('origin').lstrip('/'))
        return bList

    def tag(self):
        tList = []
        for tag in Repo(self.path).tags:
            tList.append(str(tag))
        return tList

    def checkout_to_branch(self, branch):
        Repo(self.path).git.checkout(branch)
    
    def checkout_to_commit(self, branch, commit):
        self.checkout_to_branch(branch=branch)
        Repo(self.path).git.reset('--hard', commit)    
    
    def commits(self, branch):
        self.checkout_to_branch(branch)
        commitList = []
        commit_history = git.Git(self.path).log('--pretty=%h#@#%s#@#%cn#@#%ci#@#%H', max_count=50)
        for log in commit_history.split('\n'):
            log = log.split('#@#')
            data = dict()
            data['ver'] = log[0]
            data['desc'] = log[1]
            data['user'] = log[2]
            data['comid'] = log[4]
            commitList.append(data)
        return commitList    
    
    def checkout_to_tag(self, tag):
        Repo(self.path).git.checkout(tag)  
        
    def rsync_to_release_version(self, dest_path):
        cmd = "rsync -au --delete {sourceDir} {destDir}".format(sourceDir=self.path,destDir=dest_path)
        status,result = subprocess.getstatusoutput(cmd)  
        if status > 0:
            return {"status":"failed","msg":result}
        return {"status":"succeed","msg":result}                
                                    
    def mkdir(self,dir):
        if os.path.exists(dir) is False:os.makedirs(dir)  
