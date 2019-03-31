#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import time,smtplib,os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart
from utils.logger import logger
from OpsManage.settings import config
from .base import NotcieBase

class EmailNotice(NotcieBase):
    
    def __init__(self):
        super(EmailNotice, self).__init__()
        self.e_from = config.get('email', 'smtp_account')
        self.e_host = config.get('email', 'smtp_host')
        self.e_passwd = config.get('email', 'smtp_passwd')
    
    def send(self,**kwargs):
        msg = MIMEMultipart() 
        EmailContent = MIMEText(kwargs.get('e_content'),_subtype='html',_charset='utf-8')
        msg['Subject'] = "%s " % kwargs.get('e_sub')
        msg['From'] = self.e_from
        if kwargs.get('e_to').find(',') == -1:
            msg['To'] = kwargs.get('e_to')
        else: 
            e_to = kwargs.get('e_to').split(',')
            msg['To'] = ';'.join(e_to)  
        if kwargs.get('cc_to'):
            if kwargs.get('cc_to').find(',') == -1:
                msg['Cc'] = kwargs.get('cc_to')
            else: 
                cc_to= kwargs.get('cc_to').split(',')
                msg['Cc'] = ';'.join(cc_to)       
        msg['date'] = time.strftime('%Y %H:%M:%S %z')
        try:
            if kwargs.get('attachFile'):
                EmailContent = MIMEApplication(open(kwargs.get('attachFile'),'rb').read()) 
                EmailContent["Content-Type"] = 'application/octet-stream'
                fileName = os.path.basename(kwargs.get('attachFile'))
                EmailContent["Content-Disposition"] = 'attachment; filename="%s"' % fileName
            msg.attach(EmailContent)
            smtp=smtplib.SMTP()
            smtp.connect(self.e_host)
            smtp.login(self.e_from,self.e_passwd)
            smtp.sendmail(self.e_from,e_to,msg.as_string())
            smtp.quit()
        except Exception as ex:
            logger.error("发送邮件失败：{ex}".format(ex=str(ex)))