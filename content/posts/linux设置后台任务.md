---
title: linux设置后台任务
date: 2021-12-09 03:29:25
tags:
- Linux
---

# 设置后台任务（以scp为例）



## 正常执行命令
```shell
[root@oradb30 ~]# scp -r /u01/media/Disk1/ 192.168.1.31:/u01/media/
reverse mapping checking getaddrinfo for bogon failed - POSSIBLE BREAK-IN ATTEMPT!
root@192.168.1.31's password: 
...
filegroup2.jar                                                                                                                                              100%   84KB  83.8KB/s   00:00    
filegroup9.jar       
```

## 暂停
输入ctrl + z 暂停

```shell
[1]+  Stopped                 scp -r /u01/media/Disk1/ 192.168.1.31:/u01/media/
[root@oradb30 ~]# 
```
此时查看jobs：

```shell
[root@oradb30 ~]# jobs
[1]+  Stopped                 scp -r /u01/media/Disk1/ 192.168.1.31:/u01/media/
[root@oradb30 ~]# 
```
## bg将其放入后台
bg将该任务号放入后台:

```shell
[root@oradb30 media]# bg %1
[1]+ scp -r Disk1/ 192.168.1.31:/u01/media/ &
```
查看任务已经在后台运行:

```shell
[root@oradb30 media]# jobs
[1]+  Running                 scp -r Disk1/ 192.168.1.31:/u01/media/ &
```

## disown -h 将这个作业忽略HUP信号

```shell
[root@oradb30 media]# disown -h %1
[root@oradb30 media]# jobs
[1]+  Running                 scp -r Disk1/ 192.168.1.31:/u01/media/ &
```
查看任务运行状态和父进程号:

```shell
[root@oradb30 media]# ps -ef|grep scp
root     12704 12638  0 05:19 pts/0    00:00:01 scp -r Disk1  192.168.1.31 /u01/media/
root     12705 12704  8 05:19 pts/0    00:00:17 /usr/bin/ssh -x -oForwardAgent no -oPermitLocalCommand no -oClearAllForwardings yes 192.168.1.31 scp -r -t /u01/media/
root     12823 12638  0 05:22 pts/0    00:00:00 grep scp
```
