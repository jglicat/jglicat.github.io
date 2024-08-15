# WSA

# 设置代理

```shell
# adb连接，需要在wsa设置里开启
./adb connect 127.0.0.1:58526
# 开启代理，ip地址可以在设置里看到
./adb shell settings put global http_proxy 172.26.208.1:10811
# 关闭代理
./adb shell settings put global http_proxy :0
# 断开连接
./adb disconnect 127.0.0.1:58526
```
