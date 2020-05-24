#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from abc import ABCMeta

class NotcieBase(object):
    __metaclass__ = ABCMeta
    
    def send(self,**kwargs): 
        pass
    

class NoticeException(Exception):  
    
    def __init__(self, notcie_type):  
        Exception.__init__(self)  
        self.notcie_type = notcie_type    