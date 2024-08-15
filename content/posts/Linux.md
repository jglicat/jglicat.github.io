# Linux常用命令

## linux

### 添加用户

```shell
# 默认
sudo adduser jiange
su jiange
ssh-keygen
cd ~/.ssh
cat id_rsa.pub >> authorized_keys
sudo adduser jiange docker 
sudo adduser jiange sudo 
# 需要更改用户目录时
sudo useradd -d /data/home/guest -m -s /usr/bin/bash guest
sudo passwd guest
sudo chown -R guset:guest /data/home/guest
```

### 批量杀进程

```shell
ps -ef | grep 'python main_with_runtime.py --module' | grep -v grep | awk '{print $2}' | xargs kill -9
```

## wsl

### 设置ssh

```shell
# 在windows上查找wsl的ip
wsl ip a |wsl grep -w "inet" |wsl cut -d " " -f 6 |wsl cut -d "/" -f 1
# 删除之前的转发
netsh interface portproxy delete v4tov4 listenaddress=192.168.2.238  listenport=2222
# 添加新的转发
netsh interface portproxy add v4tov4 listenport=2222 listenaddress=192.168.2.238 connectport=2222 connectaddress=172.24.105.130
# 在wsl里重启ssh
sudo systemctl restart sshd 
# 测试
ssh -p 2222 jiange@192.168.2.238
```

### 设置代理

```shell
# 这句话是防止中文乱码的
export LC_ALL=C
# 这些是代理
export windows_host=`cat /etc/resolv.conf|grep nameserver|awk '{print $2}'`
export http_proxy="http://$windows_host:10811"
export https_proxy="http://$windows_host:10811"
export ALL_PROXY="socks5://$windows_host:10810"
 if [ "`git config --global --get http.proxy`" != "socks5://$windows_host:10810" ]; then
                     git config --global http.proxy socks5://$windows_host:10810
 fi
```

### 更换清华源更新报错

换回默认源，然后装一些关于https的包

```shell
sudo apt update
sudo apt install apt-transport-https
sudo apt install ca-certificates
```

## git

### 代理相关

#### 设置git代理

```shell
#http || https
git config --global http.proxy 127.0.0.1:10809
git config --global https.proxy 127.0.0.1:10809

#sock5代理
git config --global http.proxy socks5 127.0.0.1:10808
git config --global http.proxy socks5 127.0.0.1:10808
```

#### 查看代理

```shell
git config --global --get http.proxy
git config --global --get https.proxy
```

#### 取消代理

```shell
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 更改默认编辑器

```shell
git config --global core.editor vim
```

### 秘钥

```shell
git config --global user.name "Name"
git config --global user.email "Email"
ssh-keygen -t rsa -C "Email" 
clip < ~/.ssh/id_rsa.pub
```

## nginx

```shell
sudo vim /etc/nginx/sites-enabled/default
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl reload nginx
sudo systemctl restart nginx
sudo systemctl status nginx
lsof -i:443
curl localhost:80
```

## docker

### 停止删除容器

```shell
# 停止所有容器
docker stop $(docker ps -a -q)
# 停不了就删
docker rm $(docker ps -a -q)
# 删除所有none的镜像
docker rmi $(docker images | grep "none" | awk '{print $3}') 
```

### 文件互传

```shell
# 获取容器id或name
docker ps -a
# 获取全称
docker inspect -f '{{.Id}}' name
# 传输文件
docker cp 本地 Id全称:容器路径
docker cp Id全称:容器路径 本地
```

### 端口映射ssh登录

```shell
nvidia-docker run -p 5592:5592 -p 5593:5593 -p 8022:22 -it --name="ssh_pipetorch" -v /data:/data --ipc=host  pipetorch /bin/bash
apt update
apt install -yopenssh-server
passwd

vim /etc/ssh/sshd_config
# 将PermitRootLogin的值从withoutPassword改为yes
service ssh restart
# ctrl+p+q退出
# 测试
ssh root@localhost -p 8022
```

### 权限管理

```shell
# 添加docker用户组
sudo groupadd docker 
# 把当前用户加入docker用户组
sudo gpasswd -a ${USER} docker
# 查看是否添加成功
cat /etc/group | grep ^docker
# 重启docker
sudo systemctl restart docker
# 更新用户组
newgrp docker 
# 测试docker命令是否可以正常使用
docker ps
```

## ssh

### 白名单设置

```shell
sudo vim /etc/hosts.allow
sshd:192.168.1.18:allow
#允许192.168.1.18通过SSH登录
sshd:192.168.1.0/24:allow
#允许192.168.1.0网段通过SSH登录

#或者改动这个文件，一般不同时改动
sudo vim /etc/hosts.deny
sshd:192.168.1.18:allow
#允许192.168.1.18通过SSH登录
sshd:192.168.1.0/24:allow
#允许192.168.1.0通过SSH登录
sshd:ALL
#ALL表示除了上面设置的IP。其他全部拒绝SSH登录

sudo systemctl restart ssh

#查看登录列表
who /var/log/wtmp
```

## mysql

### 开启远程访问

```shell
# 查看默认密码
sudo cat /etc/mysql/debian.cnf 
```

```shell
# 将其中的localhost改为0.0.0.0或者注释
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
```

```mysql
sudo mysql -uroot -p
use mysql;
CREATE USER 'root'@'%' IDENTIFIED BY 'your_pwd';
GRANT ALL ON *.* TO 'root'@'%';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'your_pwd';
FLUSH PRIVILEGES; 
```

### 甲骨文云关闭防火墙

```shell
#停止firewall
systemctl stop firewalld.service
#禁止firewall开机启动
systemctl disable firewalld.service
#关闭iptables
service iptables stop
#去掉iptables开机启动
chkconfig iptables off
#开放所有端口
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -F
#Oracle自带的Ubuntu镜像默认设置了Iptable规则，关闭它
apt-get purge netfilter-persistent
reboot
#强制删除
rm -rf /etc/iptables && reboot
除此之外如果创建了安全组还需要自行放行安全组
```

## dns 修改

```shell
vim /etc/resolvconf/resolv.conf.d/base  
sudo systemd-resolve --statistics 16以下   
sudo systemd-resolve --flush-caches 17以上   
```

## 查看系统配置

```shell
# sudo apt install screenfetch
sudo apt install neofetch 
sudo apt install inxi -Fxz
# -F 参数意味着你将得到完整的输出，x 增加细节信息，z 参数隐藏像 MAC 和 IP 等私人身份信息
inxi -Fxz
```

## 网络相关

### 内网测速

```shell
sudo apt install iperf
# 服务端
iperf -s
# 客户端
iperf -c ipadress
```

## pip

在 `C:\Users\$USER$\pip`或者 `~/`文件夹下新建pip.ini

ubuntu:

```shell
mkdir ~/.pip/
sudo vim ~/.pip/pip.conf
```

```shell
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
proxy     = https://127.0.0.1:10809
[install]
trusted-host = mirrors.aliyun.com
```

## gcc多版本共存

[参考链接](https://blog.csdn.net/ggggyj/article/details/117691948)

```shell
# 默认装的是高版本，现在想装低版本
sudo apt install gcc-7 g++-7
# 下面的命令配置每一个版本，并且设置了优先级。默认的版本是拥有最高优先级的那个，在我们的场景中是gcc-7
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 --slave /usr/bin/g++ g++ /usr/bin/g++-9 --slave /usr/bin/gcov gcov /usr/bin/gcov-9
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 70 --slave /usr/bin/g++ g++ /usr/bin/g++-7 --slave /usr/bin/gcov gcov /usr/bin/gcov-7
# 如果你想修改默认的版本，使用update-alternatives命令
sudo update-alternatives --config gcc
```

## cuda安装

`报错256`

```shell
# 卸载 NVIDIA 驱动:
sudo apt-get --purge remove "*nvidia*"
# 卸载 cuda:
cd /usr/local/cuda/bin
./cuda-uninstaller
```

## 挂载硬盘

```shell
# 查看容量
df -h
# 查看系统中连接的硬盘
sudo fdisk -l
# 如果没有格式化就格式化
sudo mkfs -t ext4 /dev/sda1
# 挂载到/data
sudo mkdir /data
sudo mount /dev/sda1 /data
```

## conda

### 设置conda代理

```shell
vim ~/.condarc

channels:
  - defaults
show_channel_urls: true
proxy_servers:
  http: http://127.0.0.1:10809
  https: http://127.0.0.1:10809
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud

```

## 升级Ubuntu

升级系统相关软件

```shell
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoclean
sudo apt autoremove -y
```

升级内核

```shell
sudo apt install update-manager-core
sudo do-release-upgrade -d
```

参考：<https://www.bandwagonhost.net/12638.html>

### 合盖不休眠

```shell
sudo /etc/systemd/logind.conf

# 添加
HandleLidSwitch=ignore

sudo service systemd-logind restart
```

### 关闭休眠

```shell
sudo systemctl status sleep.target
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

### 自动启动

sudo vim /usr/lib/systemd/system/frp.service

```ini
[Unit]
Description=frpc
After=network.target
Wants=network.target

[Service]
Restart=on-failure
RestartSec=5
ExecStart=/home/jiange/Downloads/frp/frps -c /home/jiange/Downloads/frp/frps.ini

[Install]
WantedBy=multi-user.target
```
# 扩容

2. 用fdisk创建新分区
指创建物理上的分区(Partition)
需要管理员权限，因为我是root操作，所以所有的提权命令都省略了。如果权限不够就sudo一下

fdisk /dev/sda
进入fdisk后，command输入n，代表要新建分区
按下4，回车，再跳过两个默认的选项，最后键入w回车保存。这样，新的分区4就创建好了。

Command (m for help): n
Partition number (4-128, default 4): 4
First sector (20969472-41943006, default 20969472):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (20969472-41943006, default 41943006):

Created a new partition 4 of type 'Linux filesystem' and of size 60 GiB.

Command (m for help): w
The partition table has been altered.
Syncing disks.
3. 用pvcreat创建物理卷
意为，在分区上标记：这个分区是空闲的

pvcreate /dev/sda4
运行结束后，可以用pvscan查看一下物理卷的情况：

PV /dev/sda3   VG ubuntu-vg       lvm2 [<19.00 GiB / 0    free]
PV /dev/sda4                      lvm2 [60.00 GiB]
Total: 2 [<79.00 GiB] / in use: 1 [<19.00 GiB] / in no VG: 1 [60.00 GiB]
可以看到，/dev/sda3 在卷组ubuntu-vg里，而 /dev/sda4 不在。

4. 用vgextend把新物理卷添加到卷组
先前有描述错误，由Wing0v0和scchen9966指出。先前的描述为：

vgextend ubuntu=-vf /dev/sda4
应当是：

vgextend ubuntu-vg /dev/sda4
5. 用lvextend给逻辑卷扩容
查看一下磁盘叫啥

df -h
找到Mounted on是\的磁盘，比如，我这是：

/dev/mapper/ubuntu—vg-ubuntu—lv
就运行命令扩容：

lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
6. 用resize2fs让逻辑卷的扩容生效
如果不执行该命令，扩容不会生效！

resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
好了，磁盘就扩展好了！用df -h看看：

Filesystem                         Size  ...
...
/dev/mapper/ubuntu--vg-ubuntu--lv   79G  ...
...
OK，扩容完成！尽管造吧！啊哈哈哈哈哈！

此文就到此结束啦！欢迎大家在评论区留言哦ヾ(^▽^*)))
Ciallo～(∠・ω< )⌒☆​
写文不易，如果你觉得我的文章对你有帮助，欢迎打赏！

hy-v 虚拟机会自动分配端口，每次打开都不一样，有一台好就是恰好端口没有占用到。
临时解决方法：
cmd -> netsh winsock reset
就是重置网络适配器，让后端口再次随机分配。如果恰好不占用就好了。
勉强算是永久的方法：
netsh int ipv4 set dynamicport tcp start=50000 num=10000
netsh int ipv4 set dynamicport udp start=50000 num=10000
netsh int ipv6 set dynamicport tcp start=50000 num=10000
netsh int ipv6 set dynamicport udp start=50000 num=10000