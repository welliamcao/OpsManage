#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
def rsync_excludes_format(path,split_string=','):
    exclude = ''
    for s in path.split(','):
        exclude =  "--exclude={file}".format(file=s.replace('\r\n','').replace('\n','').strip()) + split_string + exclude
    return exclude[:-1]

def rsync_includes_format(path,split_string=','):
    exclude = ''
    for s in path.split(','):
        exclude =  "--include={file}".format(file=s.replace('\r\n','').replace('\n','').strip()) + split_string + exclude
    return exclude[:-1]  

def tar_excludes_format(path):
    exclude = ''
    for s in path.split(','):
        exclude =  "--exclude={file}".format(file=s.replace('\r\n','').replace('\n','').strip()) + ' ' + exclude
    return exclude[:-1]

def tar_includes_format(path):
    exclude = ''
    for s in path.split(','):
        exclude =  "{file}".format(file=s.replace('\r\n','').replace('\n','').strip()) + ' ' + exclude
    return exclude[:-1]  