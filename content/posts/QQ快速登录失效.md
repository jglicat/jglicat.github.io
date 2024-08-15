本文解决的是某些神奇软件的全局代理导致的QQ快速登录失效问题

# 原因

参考：https://github.com/2dust/v2rayN/issues/1483

qq的网页快速登录时，会请求localhost.ptlogin2.qq.com域名，而此域名访问后指向的地址为127.0.0.1，导致使用时，此域名一直转发不出去，通过chrome或者firefox的开发者选项里面，可以看到localhost.ptlogin2.qq.com域名的请求response一直是空的。

# 修复

让相关域名不走代理即可。

打开`regedit`，定位到`HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings`，找到`ProxyOverride`项，添加`localhost.ptlogin2.qq.com;localhost.sec.qq.com;`，但是每次改变代理都会刷新。

为了方便可以写进.reg文件。

创建xxx.reg文件，写入（可以把剩余项换成你自己的）。

```shell
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings]
"ProxyOverride"="localhost;localhost.ptlogin2.qq.com;localhost.sec.qq.com;127.*;10.*;172.16.*;172.17.*;172.18.*;172.19.*;172.20.*;172.21.*;172.22.*;172.23.*;172.24.*;172.25.*;172.26.*;172.27.*;172.28.*;172.29.*;172.30.*;172.31.*;192.168.*"
```

需要的时候双击导入。