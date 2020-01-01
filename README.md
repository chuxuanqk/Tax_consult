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

安装nginx
cd ~
yum install pcre pcre-devel
yum install openssl openssl-devel
wget http://nginx.org/download/nginx-1.5.6.tar.gz
tar xf nginx-1.5.6.tar.gz
cd nginx-1.5.6
./configure --prefix=/usr/local/nginx-1.5.6 \
--with-http_stub_status_module \
--with-http_gzip_static_module
make && make install
ln -s /usr/local/nginx-1.5.6/sbin/nginx /bin/nginx 


在线项目部署
在服务器上创建简单Django项目hello，结合uwsgi+Django+nginx。

然后使用如下命令启动uwsgi：

uwsgi –ini uwsgi.ini

启动uwsgi：
uwsgi –ini /root/Code/Tax_consult/mysite_uwsgi.ini

启动nginx：
nginx -c /root/Code/Tax_consult/mysite_nginx.conf


以下包含了 Nginx 常用的几个命令：

/usr/local/webserver/nginx/sbin/nginx -s reload            # 重新载入配置文件
/usr/local/webserver/nginx/sbin/nginx -s reopen            # 重启 Nginx
/usr/local/webserver/nginx/sbin/nginx -s stop              # 停止 Nginx
