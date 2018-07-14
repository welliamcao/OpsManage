#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
'''版本控制方法'''
import magic
from random import choice
import string,hashlib,calendar
import commands,os,time,smtplib
from datetime import datetime,timedelta,date
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart
from OpsManage.utils.logger import logger

def file_iterator(file_name, chunk_size=512):
    f = open(file_name, "rb")
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break 
    f.close()

def sendEmail(e_from,e_to,e_host,e_passwd,e_sub="It's a test email.",e_content="test",cc_to=None,attachFile=None):
    msg = MIMEMultipart() 
    EmailContent = MIMEText(e_content,_subtype='html',_charset='utf-8')
    msg['Subject'] = "%s " % e_sub
    msg['From'] = e_from
    if e_to.find(',') == -1:
        msg['To'] = e_to
    else: 
        e_to = e_to.split(',')
        msg['To'] = ';'.join(e_to)  
    if cc_to:
        if cc_to.find(',') == -1:
            msg['Cc'] = cc_to
        else: 
            cc_to= cc_to.split(',')
            msg['Cc'] = ';'.join(cc_to)       
    msg['date'] = time.strftime('%Y %H:%M:%S %z')
    try:
        if attachFile:
            EmailContent = MIMEApplication(open(attachFile,'rb').read()) 
            EmailContent["Content-Type"] = 'application/octet-stream'
            fileName = os.path.basename(attachFile)
            EmailContent["Content-Disposition"] = 'attachment; filename="%s"' % fileName
        msg.attach(EmailContent)
        smtp=smtplib.SMTP()
        smtp.connect(e_host)
        smtp.login(e_from,e_passwd)
        smtp.sendmail(e_from,e_to,msg.as_string())
        smtp.quit()
    except Exception , e:
        print e
  
def radString(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

def rsync(sourceDir,destDir,exclude=None):
    if exclude:cmd = "rsync -au --delete {exclude} {sourceDir} {destDir}".format(sourceDir=sourceDir,destDir=destDir,exclude=exclude)
    else:cmd = "rsync -au --delete {sourceDir} {destDir}".format(sourceDir=sourceDir,destDir=destDir)
    return commands.getstatusoutput(cmd)
    
def mkdir(dirPath):
    mkDir = "mkdir -p {dirPath}".format(dirPath=dirPath)
    return commands.getstatusoutput(mkDir)    
    
    
def cd(localDir):
    os.chdir(localDir)
    
def pwd():
    return os.getcwd()   

def cmds(cmds):
    return commands.getstatusoutput(cmds)

def chown(user,path):
    cmd = "chown -R {user}:{user} {path}".format(user=user,path=path)
    return commands.getstatusoutput(cmd)

def makeToken(strs):
    m = hashlib.md5()   
    m.update(strs)
    return m.hexdigest()  

def lns(spath,dpath):
    if spath and dpath:
        rmLn = "rm -rf {dpath}".format(dpath=dpath)
        status,result = commands.getstatusoutput(rmLn)
        mkLn = "ln -s {spath} {dpath}".format(spath=spath,dpath=dpath)
        return commands.getstatusoutput(mkLn)
    else:return (1,"缺少路径")    

def getDaysAgo(num):
    threeDayAgo = (datetime.now() - timedelta(days = num))
    timeStamp = int(time.mktime(threeDayAgo .timetuple()))
    otherStyleTime = threeDayAgo .strftime("%Y%m%d")
    return otherStyleTime

def getSQLAdvisor(host,port,user,passwd,dbname,sql):
    cmd = """/usr/bin/sqladvisor -h {host}  -P {port}  -u {user} -p '{passwd}' -d {dbname} -q '{sql}' -v 1""".format(host=host,port=port,user=user,passwd=passwd,dbname=dbname,sql=sql)
    return commands.getstatusoutput(cmd)

def getDayAfter(num,ft=None):
    #获取今天多少天以后的日期
    if ft:
        return time.strftime(ft ,time.localtime(time.time()+(num*86400)))
    else:
        return time.strftime('%Y-%m-%d' ,time.localtime(time.time()+(num*86400)))
    
def calcDays(startDate,endDate):
    #对比两个日期的时间差
    startDate=time.strptime(startDate,"%Y-%m-%d %H:%M:%S")
    endDate=time.strptime(endDate,"%Y-%m-%d %H:%M:%S")
    startDate=datetime(startDate[0],startDate[1],startDate[2],startDate[3],startDate[4],startDate[5])
    endDate=datetime(endDate[0],endDate[1],endDate[2],endDate[3],endDate[4],endDate[5])
    return (endDate-startDate).days
    
def getMonthFirstDayAndLastDay(year=None, month=None):
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year
    if month:
        month = int(month)
    else:
        month = datetime.date.today().month
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)
    firstDay = date(year=year, month=month, day=1)
    lastDay = date(year=year, month=month, day=monthRange)
    return firstDay, lastDay

def getFileType(filePath):
    try:
        files = magic.Magic(uncompress=True,mime=True)
        file_type = files.from_file(filePath)
    except Exception,ex:
        file_type = '未知'
        logger.error("获取文件类型失败: {ex}".format(ex=ex))
    return file_type
    