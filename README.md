# -
配置好Python3.6和pip3
安装EPEL和IUS软件源

yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
安装Python3.6

yum install python36u -y
yum install python36u-devel -y
创建python3连接符

ln -s /bin/python3.6 /bin/python3
安装pip3

yum install python36u-pip -y
创建pip3链接符

ln -s /bin/pip3.6 /bin/pip3

安装uwsgi
python3 -m pip install uwsgi

在线项目部署
在服务器上创建简单Django项目hello，结合uwsgi+Django+nginx。

然后使用如下命令启动uwsgi：

uwsgi –ini uwsgi.ini