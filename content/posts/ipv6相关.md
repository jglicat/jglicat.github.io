[参考链接：设置openwrt软路由，通过ipv6外网访问家中电脑nas等设备系列教程 - 学长の生活志 (65.chat)](https://65.chat/toss/71.html)

# 设置openwrt软路由，通过ipv6外网访问家中电脑nas等设备系列教程

## [和强君](https://65.chat/author/1/) • 2021 年 03 月 12 日 • 阅读: 11873 • [记录](https://65.chat/toss/)

### **教程开始之前，先思考两个问题：**

* **没有公网怎么办？**

解答：目前移动、联通、电信这三家[运营](https://65.chat/operate/ "运营")商，以云南地区为例，三家都已经实现 百分之百 IPV6 [公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/ "公网")，电信有 ipv4 [公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/ "公网")，联通部分有 ipv4 [公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/ "公网")，移动没有 ipv4 [公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/ "公网")。

如何查看自己有没有[公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/ "公网")请自行百度。

* **确定有公网，但是只能内网访问。**

解答：把光猫改成桥接模式，进行路由器拨号，修改方式记住自己光猫相关参数，按照下图进行修改（记得替换相关值）。

![image.png](https://65.chat/usr/uploads/2021/03/3586096122.png "image.png")

# 教程正式开始

### **路由器拨号上网**

* 准备一个已经刷好 [openwrt](https://65.chat/tag/openwrt/ "openwrt") 的软路由，以 K3 为例，按照下图方式连接光猫的 LAN 与路由器的 WAN 即可，如果有多级可继续以相同方式进行串联。

![image.png](https://65.chat/usr/uploads/2021/03/3626658225.png "image.png")

* 启动路由器，输入 192.168.2.1（一级路由）登陆管理界面，依次网络 —— 接口 ——WAN—— 修改（如图所示）

![image.png](https://65.chat/usr/uploads/2021/03/3674710323.png "image.png")

* 协议选择 PPPOE ，之后填入宽带账号密码，其他默认不用修改即可完成设置上网。

![image.png](https://65.chat/usr/uploads/2021/03/836582041.png "image.png")

### **路由器开启 IPV6**

如果有 IPV4 [公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/ "公网")那直接申请域名做动态域名解析和端口转发即可。

openwort 设置 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 比较繁琐 需要先按照下图配置方式完成设置。

* 在接口处根据需求选择已有接口或者新建接口，删除 IPV6 前缀 保存。

![image.png](https://65.chat/usr/uploads/2021/03/2163790520.png "image.png")![image.png](https://65.chat/usr/uploads/2021/03/1621338926.png "image.png")

* 选择需要设置的 IPV6 接口 —— 高级设置 —— 地址选择自动。

![image.png](https://65.chat/usr/uploads/2021/03/3024584929.png "image.png")

* 网络 ——DHCP/DNS—— 高级设置静止解析去掉 —— 保存应用。

![image.png](https://65.chat/usr/uploads/2021/03/3992904763.png "image.png")

* 网络 —— 防火墙如图 2345 设置保存应用。

![image.png](https://65.chat/usr/uploads/2021/03/3768945224.png "image.png")

* 最后一步网络 —— 负载均衡 —— 策略 —— 改成默认保存即可。

![image.png](https://65.chat/usr/uploads/2021/03/1912518098.png "image.png")

* 打开网站[ http://www.test-ipv6.com/](http://www.test-ipv6.com/) 如图所示显示说明已经正确获取到[公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/ "公网") IPV6。

![image.png](https://65.chat/usr/uploads/2021/03/2900917412.png "image.png")

* 此时路由器下的所有设备已经获取获取到 IPV6 真实地址，通过电脑指令 ping 已经能够正常联通。

![image.png](https://65.chat/usr/uploads/2021/03/2170535817.png "image.png")

### 外网设置 IPV6

这是最后一步也是最难设置的一步，开始之前需要详细了解 IPV6 的构成和原理。

* **使用无状态的 eui64 地址** , 它的后缀是不变的。
* 内网设备的 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 地址，前半部分是 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 前缀，是[运营](https://65.chat/operate/ "运营")商分配的。重拨后会变化。后半部分，如果不是 eui64，就是随机生成的，也会变。如果是 eui64，则与 mac 地址相关，不会变化，除非换网卡。
* 如果整个 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 都会变，防火墙规则就没办法写了。除非全网放行 (内网目标地址掩码填 `::/0` 或 `any`)。或关闭防火墙。(本次教程是 eui64）
* 所以配置内网设备的 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 地址为 eui64，防火墙的内网目标地址掩码填 `::xxxx:xxxx:xxxx:xxxx/::FFFF:FFFF:FFFF:FFFF`, 这样就比较安全了。
  ([ipv6](https://65.chat/tag/ipv6/ "ipv6") 地址掩码比 v4 灵活，v6 可以掩前面，也可以掩后面。v4 就只能掩前面)
* **还有一个 ipv6 地址可以使用** (有状态地址), 即 dhcpdv6 分配的地址。每台客户机都会自己提供一个 DUID, 且不会变，分配的 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 后缀也就不变，相对固定。
  (结论：不能指定。) 在 [openwrt](https://65.chat/tag/openwrt/ "openwrt") 中 `Network`->`DHCP and DNS`->`Static Leases(静态地址)` 中，([openwrt](https://65.chat/tag/openwrt/ "openwrt") **不支持**直接指定新的 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 后缀 / 或指定 DUID。除非客户机自己没有提供 DUID)

  添加一条[记录](https://65.chat/toss/ "记录")，指定 `MAC-Address`，指定 `IPv6-Suffix`(格式为四个 hex 数，如 AABB)，这个办法**不能指定** [ipv6](https://65.chat/tag/ipv6/ "ipv6") 后缀。

  添加一条[记录](https://65.chat/toss/ "记录")，指定 `MAC-Address`，指定 `DUID`，重启客户机。看看拿到什么 IP。这个办法也**不能指定** DUID，不能得到新 [ipv6](https://65.chat/tag/ipv6/ "ipv6") 后缀。

  修改客户机的 DUID ，看 [[Linux ipv6 无状态 设置为 eui64](https://www.cnblogs.com/osnosn/p/11396868.html)] 中 “有状态 ipv6” 部分。指定新的 DUID，就有一个新的固定的 IPv6 后缀。
* 确定客户机的 ipv6 后缀之后。比如 `2408:ebcd:ebcd:ebcd::789`, 那么防火墙规则中的目标地址写 `::789/::ffff:ffff:ffff:ffff`

> 比如：你的 ipv6 地址为，2408:ebcd:ebcd:ebcd:5678:5678:5678:5678
> 则目标地址掩码填， 0:0:0:0:5678:5678:5678:5678/0:0:0:0:FFFF:FFFF:FFFF:FFFF
> 连续的 0 简写为两个冒号，即，::5678:5678:5678:5678/::FFFF:FFFF:FFFF:FFFF

#### **在接口 —— 防火墙 —— 流量规则 —— 新增 forward 规则**

如图所示填写

* 协议族选择 `ipv6 only`
* 协议按需 `TCP`, `UDP`, `TCP/UDP` ...
* Source zone 选 WAN (包含 wan6)
* Destination Zone (目标区域)，选择 `Any zone(forward)` 或者 `lan`
* 目标端口，按需填写。多个端口用空格隔开。

![image.png](https://65.chat/usr/uploads/2021/03/954286686.png "image.png")

* 这个图片中的设置，本质上就是添加了多条 forward 规则 (tcp/udp/ 一个端口，各一条)([openwrt](https://65.chat/tag/openwrt/ "openwrt")-18.06)。
  * 如果选 `Any zone(forward)`
    `ip6tables -A FORWARD -i pppoe-wan -d ::5678:5678:5678/::ffff:ffff:ffff:ffff -p tcp -m tcp --dport 443 -j ACCEPT`
    `ip6tables -A FORWARD -i pppoe-wan -d ::5678:5678:5678/::ffff:ffff:ffff:ffff -p udp -m udp --dport 443 -j ACCEPT`
  * 如果选 `lan`
    `ip6tables -A FORWARD -i pppoe-wan -o br-lan -d ::5678:5678:5678/::ffff:ffff:ffff:ffff -p tcp -m tcp --dport 443 -j ACCEPT`
  * `Device (input)` 不是用来开放内网机器访问的。是用来开放路由器本身的端口访问，这时候 Destination address (目标地址) 要留空，或写路由器自己的 IP。
    `ip6tables -A INPUT -i pppoe-wan -p tcp -m tcp --dport 443 -j ACCEPT`
* 另外，现在的[运营](https://65.chat/operate/ "运营")商**已经封禁 80,443** 两个端口 (ipv4 和 ipv6)。所以这两个端口开放了也用不了。其他端口可以用。

#### **防火墙中的默认规则 drop/reject**

Network -> Firewall -> General Settings 中:* General Settings 的 Forward 默认规则改为 drop， 影响从外网访问内网 lan, 不开放的 ipv6 地址和端口。
修改的是 `iptables/ip6tables` 的 filter->FORWARD 的最后一条
`-A FORWARD -j DROP`

* Zones 的 WAN => [--] 的 Input 默认规则改为 drop，影响从外网访问路由器本身的 wan (ipv4/6),lan (ipv6) 地址，不开放的端口。不影响端口映射。
  修改的是 `iptables/ip6tables` 的 filter->INPUT 的最后一条
  `-A INPUT -i pppoe-wan -j DROP`,
  `-A INPUT -i vwan1 -j DROP`
* Zones 的 WAN => [--] 的 Forward 默认规则改为 drop，影响从外网访问非 lan (包括 wan, 未设置为 lan 的其他接口), 不开放的地址和端口。
  修改的是 `iptables/ip6tables` 的 filter->FORWARD 的倒数第二条
  `-A FORWARD -i pppoe-wan -j zone_wan_dest_DROP`,
  `-A FORWARD -i vwan1 -j zone_wan_dest_DROP`,
  `-A zone_wan_dest_DROP -o pppoe-wan -j DROP`,
  `-A zone_wan_dest_DROP -o vwan1 -j DROP`

具体参考图片

![image.png](https://65.chat/usr/uploads/2021/03/384273838.png "image.png")

点击保存应用。

现在设备已经整个暴露在互联网状态下，通过设置域名解析即可通过网址访问访问此设置。

**ipv6 已经是公网地址，无需 nat 转换 / 端口映射，只需转发即可。**

教程到此结束，因为 IPV6 和 IPV4 一样，地址每天都会重置，且不一样，为了省去手动解析的不必要麻烦，以路由器下的 [NAS](https://65.chat/tag/NAS/ "NAS") [威联通](https://65.chat/tag/%E5%A8%81%E8%81%94%E9%80%9A/ "威联通")为例，通过阿里云的 DDNS 自动解析设备地址到域名方便快捷，教程请点击这里 → [《威联通设置阿里云动态解析进行外网 IPV6 访问家中 NAS》](https://65.chat/toss/72.html)

[ipv6](https://65.chat/tag/ipv6/)[公网](https://65.chat/tag/%E5%85%AC%E7%BD%91/)[openwrt](https://65.chat/tag/openwrt/)[光猫桥接](https://65.chat/tag/%E5%85%89%E7%8C%AB%E6%A1%A5%E6%8E%A5/)

[返回文章列表](https://65.chat/archives.html) [打赏]()

![本页链接的二维码](https://65.chat/toss/71.html)

![打赏二维码](https://65.chat/usr/uploads/2021/01/wx.jpg)

[下一篇:威联通设置阿里云动态域名解析进行外网 IPV6 访问家中 NAS](https://65.chat/toss/72.html "威联通设置阿里云动态域名解析进行外网 IPV6 访问家中 NAS")[上一篇:配置frps和frpc服务端以及客户端内网穿透进行远程访问](https://65.chat/toss/93.html "配置frps和frpc服务端以及客户端内网穿透进行远程访问")

添加新评论

[ ] [ ] [ ]

OωO

[ ]

**已有 10 条评论**

1. ![老王](https://secure.gravatar.com/avatar/638b0167e1a513fd5f0530beedc7cdf0?s=100&r=G&d=)老王
   [回复](https://65.chat/toss/71.html?replyTo=2#respond-post-71)
   [10 个月前](https://65.chat/toss/71.html#comment-2)
   好像还是不行哦

   1. ![和强君](https://thirdqq.qlogo.cn/g?b=sdk&k=eIibGmKyjYBhkicibvwFE8yHw&s=100&t=1655511865)[和强君](https://65.chat/)
      [回复](https://65.chat/toss/71.html?replyTo=3#respond-post-71)
      [9 个月前](https://65.chat/toss/71.html#comment-3)
      **@老王**推倒从来屡试不爽
2. ![小二哥](https://secure.gravatar.com/avatar/e4a0153a12a5c2f3ab0870cf01ae88d7?s=100&r=G&d=)小二哥
   [回复](https://65.chat/toss/71.html?replyTo=4#respond-post-71)
   [8 个月前](https://65.chat/toss/71.html#comment-4)
   不行 ![](https://65.chat/usr/plugins/Mirages/biaoqing/paopao/E9BB91E7BABF.png)
3. ![xhqpp](https://secure.gravatar.com/avatar/f26c95265b257b9aff0a07265daa2fef?s=100&r=G&d=)xhqpp
   [回复](https://65.chat/toss/71.html?replyTo=5#respond-post-71)
   [7 个月前](https://65.chat/toss/71.html#comment-5)
   能不能把 ipv6 的 80 端口映射成非 80 端口？80 被运营商封了

   1. ![VK](https://secure.gravatar.com/avatar/39cc87f49714da3c63e95bef73314306?s=100&r=G&d=)VK
      [回复](https://65.chat/toss/71.html?replyTo=6#respond-post-71)
      [5 个月前](https://65.chat/toss/71.html#comment-6)
      **@xhqpp**Socat Port Forword
4. ![VK](https://secure.gravatar.com/avatar/39cc87f49714da3c63e95bef73314306?s=100&r=G&d=)VK
   [回复](https://65.chat/toss/71.html?replyTo=7#respond-post-71)
   [5 个月前](https://65.chat/toss/71.html#comment-7)
   一直用的老思路主路由 ipv6 socat forword 到 Nas ipv4。
   看了自己试了下，还是直接透到公网更好，ipv6 真香。
5. ![没有字的回音](https://secure.gravatar.com/avatar/24f1e9f1aef349e6d4420b1ac682a7f6?s=100&r=G&d=)[没有字的回音](https://echo.moe/)
   [回复](https://65.chat/toss/71.html?replyTo=8#respond-post-71)
   [5 个月前](https://65.chat/toss/71.html#comment-8)
   作者你好，我的 OpenWRT 21.02.2 的防火墙里，可以直接在 advanced->Source MAC address 这里指定 MAC 地址，这样就不用操作 IPv6 地址了，你要不再看看？

   1. ![和强君](https://thirdqq.qlogo.cn/g?b=sdk&k=eIibGmKyjYBhkicibvwFE8yHw&s=100&t=1655511865)[和强君](https://65.chat/)
      [回复](https://65.chat/toss/71.html?replyTo=9#respond-post-71)
      [5 个月前](https://65.chat/toss/71.html#comment-9)
      **@没有字的回音**那也可以，只要达到穿透目的就可以了
   2. ![没有字的回音](https://secure.gravatar.com/avatar/24f1e9f1aef349e6d4420b1ac682a7f6?s=100&r=G&d=)[没有字的回音](https://echo.moe/)
      [回复](https://65.chat/toss/71.html?replyTo=10#respond-post-71)
      [5 个月前](https://65.chat/toss/71.html#comment-10)
      **@和强君**我发现这个规则并不可以，因为不是 destination MAC address，也不知道当初怎么缺心眼就以为可以了（捂脸
6. ![kiddytop](https://secure.gravatar.com/avatar/bb20d47ae48f3064de115456f08fdfec?s=100&r=G&d=)kiddytop
   [回复](https://65.chat/toss/71.html?replyTo=11#respond-post-71)
   [3 个月前](https://65.chat/toss/71.html#comment-11)
   博主：
   IPV6 如果只开放特定端口到设备，意思是有两步对吧，比如开放 5000 端口：
   1、开放 5000 端口到路由器，就是 INPUT 项；
   2、添加转发规则，5000 端口由 WAN 转发到设备，就是 forward 项

Copyright © 2022 [学长の生活志](https://65.chat/)

[滇ICP备2020009854号](http://beian.miit.gov.cn/) • Powered by [Typecho](http://typecho.org/) • Theme [Mirages](https://get233.com/archives/mirages-intro.html)
