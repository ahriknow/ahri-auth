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
