# 搭建

## 部署环境

` Ubuntu 20.04.3 LTS (GNU/Linux 5.11.0-1022-oracle x86_64)`

## 安装软件

```shell
sudo apt-get update
sudo apt-get upgrade
# 这里的php是ubuntu的默认安装版本
sudo apt-get install -y nginx mysql-server php php-mysql php-gd php-fpm php-cgi php-xml php-mbstring php-curl
```

## 配置mysql

```shell
sudo service mysql start
sudo mysql
```

```mysql
# root为用户名,pwd为密码，根据情况自己设定
sudo mysql -uroot -p
use mysql;
CREATE USER 'root'@'%' IDENTIFIED BY 'your_pwd';
GRANT ALL ON *.* TO 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'your_pwd';
FLUSH PRIVILEGES; 
```

## 配置nginx

```shell
sudo cp /etc/nginx/sites-enabled/default /etc/nginx/sites-enabled/default.bak
sudo vim /etc/nginx/sites-enabled/default
```

找到 index index.html index.htm index.nginx-debian.html; 这句，加入 index.php

```ini
# Add index.php to the list if you are using PHP
index index.php index.html index.htm index.nginx-debian.html;
```

接着往下查找到 location ~ .php 这句修改一下，再按照下面，把这几行前面的 # 号去掉，记得还有花括号前的 # 号。

```ini
# pass PHP scripts to FastCGI server
location ~ .*\.php(\/.*)*$ {
       include snippets/fastcgi-php.conf;
       # With php-fpm (or other unix sockets):
       fastcgi_pass unix:/var/run/php/php-fpm.sock;
       # With php-cgi (or other tcp sockets):
#       fastcgi_pass 127.0.0.1:9000;
}
```

```shell
sudo service nginx restart
# 如果还是访问不到
sudo rm -f /etc/iptables/rules.v4
sudo rm -f /etc/iptables/rules.v6
```

## 部署typecho

```shell
cd /var/www/html
sudo wget http://typecho.org/downloads/1.1-17.10.30-release.tar.gz
sudo tar -zxvf 1.1-17.10.30-release.tar.gz
sudo mv build/* ./
```

然后访问机器的ip，按照说明配置即可

```shell
cd /var/www/html
sudo vim config.inc.php
```

# 迁移

## 备份

```shell
sudo zip -r nginx.zip /etc/nginx
sudo mysqldump -ujiange -p --all-databases > sqlfile.sql
sudo zip -r html.zip /var/www/html
```

## 恢复

```shell
sudo unzip nginx.zip -d /
sudo mysql -uroot -p < sqlfile.sql
sudo unzip html.zip -d /
sudo systemctl restart mysql 
sudo systemctl restart nginx
```

提桶跑路

# 参考

https://www.igisv.com/archives/3.html
