FROM python:3.6-slim

WORKDIR /usr/src/app

VOLUME ["/usr/src/app/upload"]

RUN sed -i 's/http\:\/\/deb.debian.org/https\:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list \
 && sed -i 's/http\:\/\/security.debian.org/https\:\/\/mirrors.aliyun.com/g' /etc/apt/sources.list \
 && apt update \
 && apt install -y default-libmysqlclient-dev gcc python-dev libldap2-dev libsasl2-dev git sshpass \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]
