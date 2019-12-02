#docker build -t opsmanage-app -f Dockerfile-app ..

FROM opsmanage-base

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]
