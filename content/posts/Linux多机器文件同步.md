有多台机器又要重复配置是一项很不优雅的操作，理应由软件帮我们完成

## rsync+inotify

https://www.jianshu.com/p/fc2f3ec661c0

https://segmentfault.com/a/1190000002427568

比较老的解决方案，缺点就是文件过多时目录文件太大 ，后期一个小更新都要传递10MB+的目录文件，资源浪费

## lsyncd

https://www.cnblogs.com/shione/p/10775649.html

先配置ssh免密登录

```shell
# 先在客户端生成密钥对（一路回车就行）
ssh-keygen
# 上传公钥到服务器
ssh-copy-id -i ~/.ssh/id_rsa.pub 用户名@IP
# 此处为ssh-copy-id -i ~/.ssh/id_rsa.pub jiange@172.22.4.11
# 如果已配置别名，也可以
ssh-copy-id -i ~/.ssh/id_rsa.pub 别名

# 但是我们的服务是在root下运行的，所以需要复制一份
sudo cp ~/.ssh/id_rsa.pub /root/.ssh/id_rsa.pub

# 测试
sudo su
ssh jiange@172.22.4.11
```

安装然后新建配置文件

```shell
sudo apt install lsyncd
# 创建日志目录
sudo mkdir /var/log/lsyncd
# 这是ubuntu的配置文件,centos的似乎在/etc/lsyncd.conf
sudo mkdir /etc/lsyncd
sudo vim /etc/lsyncd/lsyncd.conf.lua
```

写入配置文件，注意default.rsyncssh只能单线程

```lua
settings {
    logfile = "/var/log/lsyncd/lsyncd.log",
    statusFile = "/tmp/lsyncd.stat",
    statusInterval = 1,
    maxProcesses = 1
}

servers = {"jiange@172.22.4.12", "jiange@172.22.4.13", "jiange@172.22.4.207", "jiange@172.22.4.208"}

for _, server in ipairs(servers) do
    sync {
        default.rsyncssh,
        source = "/data/sync",
        host = server,
        targetdir = "/data/sync",
        delete = true,
        -- excludeFrom="/etc/lsyncd-excludes.txt",
        -- maxDelays = 5,
        delay = 0,
        rsync = {
            binary = "/usr/bin/rsync",
            compress = true,
            archive = true,
            verbose = true
        },
        ssh = {
            port = 22
        }
    }

end

```

然后启动

```shell
sudo systemctl start lsyncd
```

## 文件数量问题

`Lsyncd fails with Out of inotify Watches Error`

```shell
sudo systemctl stop lsyncd.service
sudo sysctl fs.inotify.max_user_watches=4000000
sudo systemctl start lsyncd.service
# 永久生效
sudo sysctl -w fs.inotify.max_user_watches=4000000 | tee -a /etc/sysctl.conf && sysctl -p
```
