---
title: ssh相关问题
date: 2021-12-09 03:24:44
tags: 
- Linux
- ssh
---

# 配置别名

```shell
sudo vim ~/.ssh/config

Host 别名名称
    HostName IP或者域名
    Port 端口
    User 用户名
    IdentitiesOnly yes

```

# 登录安全性

## 配置免密登录

```shell
# 先在客户端生成密钥对（一路回车就行）
ssh-keygen

# 上传公钥到服务器
ssh-copy-id -i ~/.ssh/id_rsa.pub 用户名@IP
# 如果已配置别名，也可以
ssh-copy-id -i ~/.ssh/id_rsa.pub 别名

```

## 秘钥登录

### 添加公钥

首先将私钥`~/.ssh/id_rsa`保存下来

https://wangdoc.com/ssh/key.html

OpenSSH 自带一个`ssh-copy-id`命令，可以自动将公钥拷贝到远程服务器的`~/.ssh/authorized_keys`文件。如果`~/.ssh/authorized_keys`文件不存在，`ssh-copy-id`命令会自动创建该文件

```shell
ssh-copy-id -i key_file user@host
```

上面命令中，`-i`参数用来指定公钥文件，`user`是所要登录的账户名，`host`是服务器地址。如果省略用户名，默认为当前的本机用户名。执行完该命令，公钥就会拷贝到服务器。

注意，公钥文件可以不指定路径和`.pub`后缀名，`ssh-copy-id`会自动在`~/.ssh`目录里面寻找。

```shell
# 将公钥添加到authorized_keys文件末尾
ssh-copy-id -i id_rsa user@localhost
```

上面命令中，公钥文件会自动匹配到`~/.ssh/id_rsa.pub`。

`ssh-copy-id`会采用密码登录，系统会提示输入远程服务器的密码。

注意，`ssh-copy-id`是直接将公钥添加到`authorized_keys`文件的末尾。如果`authorized_keys`文件的末尾不是一个换行符，会导致新的公钥添加到前一个公钥的末尾，两个公钥连在一起，使得它们都无法生效。所以，如果`authorized_keys`文件已经存在，使用`ssh-copy-id`命令之前，务必保证`authorized_keys`文件的末尾是换行符（假设该文件已经存在）。

### 关闭密码登录

```shell
sudo vim /etc/ssh/sshd_config
# 添加
DenyUsers root@127.0.0.1
Match User root
PasswordAuthentication yes
Match all
PasswordAuthentication no
# 重启ssh服务
sudo systemctl restart ssh
```

root用户可以用密码登录，其他用户必须采用秘钥登录，同时禁止root在本地登录（frp跳转后实际上是本地登录）

