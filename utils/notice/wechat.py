#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from utils.logger import logger
from OpsManage.settings import config
from utils.notice.base import NotcieBase

class WechatNotice(NotcieBase):
    
    def __init__(self):
        super(WechatNotice, self).__init__()
    
    def send(self,**kwargs):
        print(kwargs)