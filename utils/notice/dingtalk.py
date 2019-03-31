#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from utils.logger import logger
from OpsManage.settings import config
from .base import NotcieBase

class DtalkNotice(NotcieBase):
    
    def __init__(self):
        super(DtalkNotice, self).__init__()
    
    def send(self,**kwargs):
        print(kwargs)