#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import MySQLdb
from celery import task
from OpsManage.utils import base
from OpsManage.models import Assets,Email_Config,Server_Assets, \
                             DataBase_Server_Config,NetworkCard_Assets
from django.contrib.auth.models import User
from OpsManage.utils.ansible_api_v2 import ANSRunner

@task 
def expireAssets(**kw):   
    if kw.has_key('expire') and kw.has_key('user'): 
        try:
            config = Email_Config.objects.get(id=1)
        except Exception ,ex:
            return ex        
        expired = []
        expire_soon = []
        serverList = Assets.objects.raw('SELECT id,management_ip,expire_date,expire_date - CURDATE() as diff from opsmanage_assets where expire_date - CURDATE() is not null;')
        for ds in serverList:
            if  ds.diff < 0:expired.append(ds)
            elif ds.diff >= 0 and ds.diff < kw.has_key('expire'):expire_soon.append(ds)
        if  expired or  expire_soon:
            trs = ''    
            for s in expired + expire_soon:
                tr = '''
                <tr>
                   <td><a href="{url}/assets_view/{sid}/">{host}</a></td>
                   <td>{exdate}</td>
                   <td>{day}</td>
                </tr>'''.format(url=config.site,sid=s.id,host=s.management_ip,exdate=s.expire_date,day=s.diff)
                trs = trs + tr
            table = '''<table border="1" width="600" rules="all">
                         <caption>Assets Expire Alert </caption>
                         <colgroup span="1" width="200"></colgroup>
                         <colgroup span="3" width="400"></colgroup>
                            <tbody align='center'>
                            <tr>
                               <td bgColor=#C0C0C0>主机ip</td>
                               <td bgColor=#C0C0C0>过期日期</td>
                               <td bgColor=#C0C0C0>剩余</td>
                            </tr>
                              %s
                            </tbody>
                        </table> ''' % trs
            content = table + """注：负数表示<strong>按照预警规则</strong>已经过期多少天"""
            try:
                to_user = User.objects.get(username=kw.get('user')).email
            except Exception, ex:
                return ex                                            
            if config.subject:subject = "{sub} 资产过期提醒  【重要】".format(sub=config.subject)
            else:subject = "资产过期提醒  【重要】"
            if config.cc_user:
                cc_to = config.cc_user
            else:cc_to = None
            base.sendEmail(e_from=config.user,e_to=to_user,cc_to=cc_to,
                           e_host=config.host,e_passwd=config.passwd,
                           e_sub=subject,e_content=content)
            return True 
        
@task() 
def updateAssets():
    sList = []
    resource = []    
    for assets in Assets.objects.all():
        if assets.assets_type in ['vmser','server']:
            try:
                server_assets = Server_Assets.objects.get(assets=assets)
            except Exception, ex:
                print ex
                continue
            sList.append(server_assets.ip)
            if server_assets.keyfile == 1:resource.append({"hostname": server_assets.ip, "port": int(server_assets.port),"username": server_assets.username})
            else:resource.append({"hostname": server_assets.ip, "port": server_assets.port,"username": server_assets.username, "password": server_assets.passwd})  
    ANS = ANSRunner(resource)
    ANS.run_model(host_list=sList,module_name='setup',module_args="")
    data = ANS.handle_cmdb_data(ANS.get_model_result())    
    if data:
        for ds in data:
            status = ds.get('status')
            if status == 0:
                try:
                    assets = Server_Assets.objects.get(ip=ds.get('ip')).assets
                    Server_Assets.objects.filter(ip=ds.get('ip')).update(cpu_number=ds.get('cpu_number'),kernel=ds.get('kernel'),
                                                                          selinux=ds.get('selinux'),hostname=ds.get('hostname'),
                                                                          system=ds.get('system'),cpu=ds.get('cpu'),
                                                                          disk_total=ds.get('disk_total'),cpu_core=ds.get('cpu_core'),
                                                                          swap=ds.get('swap'),ram_total=ds.get('ram_total'),
                                                                          vcpu_number=ds.get('vcpu_number')
                                                                          )
                    sList.append(server_assets.ip)
                except Exception, ex:
                    print ex 
                for nk in ds.get('nks'):
                    macaddress = nk.get('macaddress')
                    count = NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).count()
                    if count > 0:
                        try:
                            NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).update(assets=assets,device=nk.get('device'),
                                                                                                               ip=nk.get('address'),module=nk.get('module'),
                                                                                                               mtu=nk.get('mtu'),active=nk.get('active'))
                        except Exception, ex:
                            print ex
                    else:
                        try:
                            NetworkCard_Assets.objects.create(assets=assets,device=nk.get('device'),
                                                          macaddress=nk.get('macaddress'),
                                                          ip=nk.get('address'),module=nk.get('module'),
                                                          mtu=nk.get('mtu'),active=nk.get('active'))
                        except Exception, ex:
                            print ex  
                    
                    
@task 
def orderSql(**kw):
    if kw.has_key('sql') and kw.has_key('dbId'):
        try:
            db = DataBase_Server_Config.objects.get(id=kw.get('dbId'))
        except Exception, ex:
            return ex
        try:
            conn = MySQLdb.connect(host=db.db_host,user=db.db_user,passwd=db.db_passwd,db=db.db_name,port=int(db.db_port))
            cur = conn.cursor()
            ret = cur.execute(kw.get('sql'))
            conn.commit()
            cur.close()
            conn.close()            
            return {"status":'success','data':ret}
        except MySQLdb.Error,e:
            conn.rollback()
            cur.close()
            conn.close() 
            return {"status":'error',"errinfo":"Mysql Error %d: %s" % (e.args[0], e.args[1])}      
    else:
        return "参数不对"    