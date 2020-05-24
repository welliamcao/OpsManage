#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
from .email import EmailNotice
from .wechat import WechatNotice
from .dingtalk import DtalkNotice
from .base import NoticeException

def Notice(notcie_type):
    if notcie_type == 0:
        return EmailNotice()
    
    elif notcie_type== 1:
        return WechatNotice()
    
    elif notcie_type== 2:
        return DtalkNotice()
    
    else:
        raise NoticeException(notcie_type)