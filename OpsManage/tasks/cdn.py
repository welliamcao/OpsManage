from celery import task
from OpsManage.utils.cdnrefresh_v2_1 import Cdn

@task
def commitcdn(args):
    cdn = Cdn()
    try:
        cdn.parse_args(args)
        return True
    except Exception,e:
        print e
        return False
