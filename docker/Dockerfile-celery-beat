#docker build -t opsmanage-celery-beat -f Dockerfile-celery-beat ..

FROM opsmanage-app

CMD celery -A OpsManage beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
