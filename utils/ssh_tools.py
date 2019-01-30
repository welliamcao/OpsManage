#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import os,threading
import paramiko


        
class SSH(threading.Thread):
    
    def __init__(self,ssh,hostname,model=None,
                 queue=None,thread=False,cmd=None,
                 cmd_args=None,localPath=None,
                 remotePath=None,remoteFile=None):
        threading.Thread.__init__(self)
        self.ssh = ssh
        self.queue = queue
        self.hostname = hostname
        self.model = model
        self.cmd = cmd
        self.cmd_args = cmd_args
        self.localPath = localPath
        self.remoteFile = remoteFile
        self.remotePath = remotePath
        
    def run(self):
        if self.model == 'command':
            self.queue.put(self.command(self.cmd,self.cmd_args))
            self.ssh.close()
        elif self.model == 'upload':
            self.queue.put(self.upload(self.localPath,self.remotePath))
            self.ssh.close()
    
    def command(self,cmd,cmd_args=None):
        try:
            data = {}
            stdin,stdout,stderr = self.ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            data["ip"] = self.hostname
            data["msg"] = ''.join(stdout.readlines()).replace("\n","<br>")
            if exit_status > 0:
                data["msg"] =  "%s" % (''.join(stderr.readlines())).replace("\n","<br>")
                data["status"] = 'faild'
            else:
                data["status"] = 'success'
            return  data
        except Exception,e:
            data["ip"] = self.hostname
            data["msg"] = str(e)
            data["status"] = 'faild'
            return  data


    def upload(self,localPath,remotePath):
        try:
            data = {}
            sftp = paramiko.SFTPClient.from_transport(self.ssh) 
            sftp.put(localPath,remotePath)
            data["ip"] = self.hostname
            data["status"] = 'success'
            data["msg"] = ""
            return data
        except Exception,e:
            data["ip"] = self.hostname
            data["status"] = 'failed'
            data["msg"] = str(e)
            return data  

            
    def download(self,localPath,remotePath,remoteFile):      
        try:
            sftp = paramiko.SFTPClient.from_transport(self.ssh) 
            if os.path.exists(localPath+remoteFile):
                rst_size = sftp.stat(remotePath+remoteFile).st_size
                lst_size = os.stat(localPath+remoteFile).st_size               
                if rst_size != lst_size:
                    sftp.get(remotePath+remoteFile,localPath+remoteFile)  
            else:
                sftp.get(remotePath+remoteFile,localPath+remoteFile)            
            return True
        except Exception,e:
            return False 

    def stop(self):
        self.thread_stop=True 
        
            
class SSHManage(object):
    def __init__(self,hostname,password,username,port):
        self.hostname = hostname
        self.password = password
        self.username = username
        self.port = port
    
    def ssh(self,model=None,queue=None,thread=None):
        self.sshConn = paramiko.SSHClient()
        self.ssh.load_system_host_keys() ####获取ssh key密匙，默认在~/.ssh/knows_hosts       
        self.sshConn.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        self.sshConn.connect(hostname = self.hostname,port=self.port,username=self.username, password=self.password)          
        ssh = SSH(ssh=self.sshConn,hostname=self.hostname,
                       queue=queue,thread=thread,model=model) 
        return ssh   
    
    def sftp(self,model=None,queue=None): 
        self.sshConn = paramiko.Transport((self.hostname,self.port))
        self.sshConn.connect(username=self.username, password=self.password)         
        sftp = SSH(ssh=self.sshConn,hostname=self.hostname,
                       queue=queue,model=model) 
        return sftp   
    
    def thread(self,model,queue,cmd=None,
               cmd_args=None,localPath=None,
               remotePath=None,remoteFile=None):           
        if model == 'command':         
            self.sshConn = paramiko.SSHClient()
            self.sshConn.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            self.sshConn.connect(hostname = self.hostname,port=self.port,
                                 username=self.username, password=self.password)          
            self.threads = SSH(ssh=self.sshConn,hostname=self.hostname,
                           queue=queue,model=model,cmd=cmd,
                           cmd_args=cmd_args,localPath=localPath,
                           remotePath=remotePath,remoteFile=remoteFile)
            
        elif model in ['upload','download']:
            self.sshConn = paramiko.Transport((self.hostname,self.port))
            self.sshConn.connect(username=self.username, password=self.password)         
            self.threads = SSH(ssh=self.sshConn,hostname=self.hostname,
                           queue=queue,model=model,cmd=cmd,
                           cmd_args=cmd_args,localPath=localPath,
                           remotePath=remotePath,remoteFile=remoteFile)            
        

        
    
    def start(self):
        self.threads.start()    
        
    def upload(self,localPath,remotePath):        
        sftp = self.sftp()
        return sftp.upload(localPath, remotePath)
    
    def command(self,cmd,cmd_args=None):
        ssh = self.ssh()
        return ssh.command(cmd=cmd, cmd_args=cmd_args)

    def download(self,localPath,remotePath,remoteFile):
        sftp = self.sftp()
        return sftp.download(localPath, remotePath,remoteFile)    
        
    def close(self):
        if self.sshConn:
            return self.sshConn.close()
        else:raise  ValueError("请先初始化链接")  
        
        
if __name__ == '__main__':
    for x in ['192.168.1.233','192.168.1.234']:
        sshRbt = SSHManage(hostname=x,password='welliam',username='root',port=22)
        sshRbt.thread(model='command',cmd='uptime;sleep 3;uptime',queue=True)
        sshRbt.start()
        sshRbt.thread(model='command',cmd='ls',queue=True)
        sshRbt.start()
#         sshRbt.thread(model='upload',localPath='D:\\application.yml',remotePath='/root/application.yml',queue=True)
#         sshRbt.start()
#         print sshRbt.command(cmd='uptime;sleep 3;uptime')
#         print sshRbt.command(cmd='ls')
#         sshRbt.close()