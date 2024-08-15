# Cygwin配置

## 下载安装

[Cygwin](https://www.cygwin.com/)

## windows terminal配置

```shell
# 生成guid
new-guid
```

添加配置文件，此处需要注意的一点是，Cygwin 中的 Bash 需要以交互式登录 shell（interactive login shell）的形式启动，否则的话，在运行一些包括 `ls` 在内的基本指令的时候会出 “command not found” 的消息。这个的原因是只有登录 shell 会在启动的时候运行 `/etc/profile`，然后 Cygwin 中的 `/etc/profile` 会把 `/usr/bin` 和 `/usr/local/bin` 加到 `PATH` 环境变量当中。如果开启的不是登录 shell，那么 `/etc/profile` 不会被运行，环境变量也就不会被设置。启动交互式登录 shell 的方法是使用 `-i -l` 选项。如果您想使用别的 shell，那么请自行确认下让 `/usr/bin` 和 `/usr/local/bin` 被添加到 `PATH` 下的方法。

```json
{
    "guid": "{38397ce3-6a93-4a63-be64-30bf0b270469}",
    "hidden": false,
    "name": "cygwin64",
    "commandline": "C:\\path\\cygwin64\\bin\\bash.exe -i -l",
    "icon": "C:/path/cygwin64/Cygwin-Terminal.ico"
}
```

## 参考链接

[在 Windows Terminal 中使用 Cygwin 命令行或 Git Bash - Leo3418 的个人网站](https://leo3418.github.io/zh/2020/05/24/cygwin-git-bash-in-wt.html)