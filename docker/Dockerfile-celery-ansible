#docker build -t opsmanage-celery-ansible -f Dockerfile-celery-ansible ..

FROM opsmanage-app

CMD celery -A OpsManage worker --loglevel=info -E -Q ansible -n worker-ansible@%%h
