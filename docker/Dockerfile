FROM python:3.6-slim

WORKDIR /data/apps/opsmanage

VOLUME ["/data/apps/opsmanage/upload"]

RUN sed -i 's/http\:\/\/deb.debian.org/https\:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list \
 && sed -i 's/http\:\/\/security.debian.org/https\:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list \
 && apt update \
 && apt install -y default-libmysqlclient-dev gcc python-dev libldap2-dev libsasl2-dev git sshpass mariadb-client supervisor rsync\
 && rm -rf /var/lib/apt/lists/*

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir  -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r /tmp/requirements.txt && rm -rf /tmp/requirements.txt

