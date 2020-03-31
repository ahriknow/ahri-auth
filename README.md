# Ahri Auth

## Authority management system, authority verification, user management, etc.

## Build the image

```Dockerfile
FROM python:3.8
MAINTAINER "ahri"<ahriknow@ahriknow.cn>
ADD manage.py /project/manage.py
ADD db/db.sqlite3 /project/db.sqlite3
ADD AhriAuth /project/AhriAuth
ADD AuthManage /project/AuthManage
ADD DeptManage /project/DeptManage
ADD JurisdictionManage /project/JurisdictionManage
ADD UserManage /project/UserManage
ADD LoginManage /project/LoginManage
ADD requirements.txt /project/requirements.txt
COPY pip.conf /etc/pip.conf
WORKDIR /project
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:9000", "AhriAuth.wsgi"]
```

## Run a container

```bash
docker container run --name auth -p 80:9000 -d ahriknow/auth:v20200330
```

-   `--name image` 容器名为 image
-   `-p 80:9000` 将容器 9000 端口映射到宿主机 80 端口
-   `-d` 后台运行
-   `ahriknow/image:v20200330` 镜像

## Python requirements.txt

```py
asgiref==3.2.7
Django==3.0.4
django-cors-headers==3.2.1
django-shortuuidfield==0.1.3
djangorestframework==3.11.0
gunicorn==20.0.4
pytz==2019.3
shortuuid==1.0.1
six==1.14.0
sqlparse==0.3.1
```

## [Github](https://github.com/fox-ahri/ahri-auth)

## Powered By ahri 20200330
