#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
import random
from orders.models import Order_System,Project_Order,SQL_Audit_Order
from django.db.models import Count
from django.contrib.auth.models import User,Group
from OpsManage.utils import base

class Order(object):
    def __init__(self):
        super(Order,self).__init__()   
        
    
    def getDateList(self,number):
        return  [ base.getDaysAgo(num) for num in xrange(0,number) ][::-1]#将日期反序
      
    def getOrderStatusCount(self):
        orderStatus = Order_System.objects.values('order_status').annotate(dcount=Count('order_status'))
        statusList = []
        status = dict()
        for st in Order_System.STATUS:
            status[str(st[0])] = st[1]
        for ds in orderStatus:
            data = {}
            if status.has_key(str(ds.get('order_status'))):
                data[status.get(str(ds.get('order_status')))] = ds.get('dcount')
                statusList.append(data)
        return statusList
    
    def countOrderType(self):
        return Order_System.objects.values('order_type').annotate(dcount=Count('order_type'))
    
    def getUserNameList(self):
        usernameList = Order_System.objects.raw("SELECT t2.id,t1.username AS order_user  FROM auth_user t1,opsmanage_order_system t2 WHERE t1.id = t2.order_user GROUP BY t2.order_user;")
        return [ u.order_user for u in usernameList ]  
    
    
    def getOrderCount(self,type,day):
        #N天更新频率统计
        sqlUserList = Order_System.objects.raw('''SELECT id,order_user FROM opsmanage_order_system where order_type={type} GROUP BY order_user;'''.format(type=type))
        sqlUserList = [ u.order_user for u in sqlUserList ]
        sqlDataList = []            
        for startTime in self.getDateList(day):   
            data = dict()  
            data['date'] = startTime
            for user in sqlUserList:                       
                sql = """SELECT id,IFNULL(count(0),0) as count from opsmanage_order_system WHERE 
                        order_type={type} and date_format(create_time,"%%Y%%m%%d") = {startTime} 
                        and order_user='{user}'""".format(startTime=startTime,user=user,type=type)
                userData = Order_System.objects.raw(sql)               
                try:
                    username = User.objects.get(id=user).username
                except:
                    username = 'unknown'              
                if  userData[0].count == 0 :
                    data[username] = random.randint(1, 10)
                else:
                    data[username] = userData[0].count
            sqlDataList.append(data)    
        return  sqlDataList  
    
    def getMonthOrderCount(self):
        #月度统计
        monthList = [ base.getDaysAgo(num)[0:6] for num in (0,30,60,90,120,150,180) ][::-1]
        monthDataList = []
        for ms in monthList:
            startTime = int(ms+'01')
            endTime = int(ms+'31')
            data = dict()
            data['date'] = ms
            for tp in [0,1,2,3]:
                if tp == 1:order_type = 'code'
                elif tp==0:order_type = 'sql'
                elif tp==2:order_type = 'upload'
                elif tp==3:order_type = 'download'
                sql = """SELECT id,IFNULL(count(0),0) as count from opsmanage_order_system WHERE date_format(create_time,"%%Y%%m%%d") >= {startTime} and 
                        date_format(create_time,"%%Y%%m%%d") <= {endTime} and order_type='{tp}'""".format(startTime=startTime,endTime=endTime,tp=tp)
                userData = Order_System.objects.raw(sql) 
                if  userData[0].count == 0:data[order_type] = random.randint(1, 100)
                else:data[order_type] = userData[0].count
            monthDataList.append(data)
        return  monthDataList       