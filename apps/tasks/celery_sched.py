#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import pymysql
from celery import task
from asset.models import Assets,Server_Assets, NetworkCard_Assets
from databases.models import DataBase_Server_Config
from utils.ansible.runner import ANSRunner


    
@task() 
def schedule_update_assets():
    sList = []
    resource = []    
    for assets in Assets.objects.all():
        if assets.assets_type in ['vmser','server']:
            try:
                server_assets = Server_Assets.objects.get(assets=assets)
                sList.append(server_assets.ip)               
                if server_assets.keyfile != 1:
                    resource.append({"hostname": server_assets.ip,"ip": server_assets.ip, "port": int(server_assets.port),"username": server_assets.username,"password":server_assets.passwd})
                elif server_assets.keyfile_path:
                    resource.append({"hostname": server_assets.ip,"ip": server_assets.ip,"port": server_assets.port,"username": server_assets.username, "password": server_assets.passwd,"private_key":server_assets.keyfile_path})                
            except Exception as ex:
                print(ex)
                continue
    if len(sList) > 0:
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
                    except Exception as ex:
                        print(ex) 
                    for nk in ds.get('nks'):
                        macaddress = nk.get('macaddress')
                        count = NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).count()
                        if count > 0:
                            try:
                                NetworkCard_Assets.objects.filter(assets=assets,macaddress=macaddress).update(assets=assets,device=nk.get('device'),
                                                                                                                   ip=nk.get('address'),module=nk.get('module'),
                                                                                                                   mtu=nk.get('mtu'),active=nk.get('active'))
                            except Exception as ex:
                                print(ex)
                        else:
                            try:
                                NetworkCard_Assets.objects.create(assets=assets,device=nk.get('device'),
                                                              macaddress=nk.get('macaddress'),
                                                              ip=nk.get('address'),module=nk.get('module'),
                                                              mtu=nk.get('mtu'),active=nk.get('active'))
                            except Exception as ex:
                                print(ex)  
    else:
        return {"status":"failed","msg":"资产更新失败: 资产信息不正确"} 
                    
                    
@task 
def schedule_exec_sql(**kw):
    if 'sql' and 'dbId' in kw.keys():
        try:
            db = DataBase_Server_Config.objects.get(id=kw.get('dbId'))
        except Exception as ex:
            {"status":"failed","msg":str(ex)} 
        try:
            conn = pymysql.connect(host=db.db_assets.server_assets.ip,user=db.db_user,
                                   passwd=db.db_passwd,db=db.db_name,
                                   port=int(db.db_port))
            cur = conn.cursor()
            ret = cur.execute(kw.get('sql'))
            conn.commit()
            cur.close()
            conn.close()            
            return {"status":'success','msg':ret}
        except pymysql.Error as e:
            conn.rollback()
            cur.close()
            conn.close() 
            return {"status":'failed',"msg":"Mysql Error %d: %s" % (e.args[0], e.args[1])}      
    else:
        return {"status":"failed","msg":"参数不对"}     