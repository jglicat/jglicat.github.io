# Fiddler Everything破解

3.2版本测试有效

## 前言

Fiddler Everywhere 是一款跨平台的抓包软件。

它由 Electron + dotNet 编写而成。

于是破解需要修改 Electron 与 dotNet 两部分。

## 破解

### 修改 Electron 的js代码

进入`\resources\app\out\WebServer\ClientApp\dist`

打开 main.xxxx.js
搜索 `updateUserLicense` ，在函数内部开头加入：

```js
 xe.licenseInfo.currentLicense = "Pro"
 xe.licenseInfo.hasExpiredTrial = false
 xe.licenseInfo.isTrialAvailable = false
 xe.licenseInfo.hasValidLicense = true
```

###  修改dotNet的代码

进入`C:\Users\SwordSong\AppData\Local\Programs\Fiddler Everywhere\resources\app\out\WebServer`

1. 使用 ildasm 将 `FiddlerBackendSDK.dll`转成 il

2. 定位到 `FiddlerBackendSDK.User.UserClient::GetBestAccount`

   删除 IL_000d – IL_0020 对应 if 语句

   删除 IL_003f – IL_0040 对应 `return null;` 语句

3. 定位到 <>c__DisplayClass18_0′::’b\_\_0

   删除 IL_0000 – IL_0019 , 在 IL_001e 前插入 `ldc.i4.1`

### 代码对比

GetBestAccount：

```java
public AccountDTO GetBestAccount(UserWithBestAccountDTO user)
{
	UserClient.u003cu003ec__DisplayClass18_0 variable = null;
	if (!user.get_BestEverywhereAccountId().get_HasValue())
	{
		return null;
	}
	return Enumerable.FirstOrDefault<UserAccountDTO>(user.get_Accounts(), new Func<UserAccountDTO, bool>(variable, (UserAccountDTO x) => x.get_Id() == this.user.get_BestEverywhereAccountId().get_Value()));
}
 
public AccountDTO GetBestAccount(UserWithBestAccountDTO user)
{
	UserClient.u003cu003ec__DisplayClass18_0 variable = null;
	return Enumerable.FirstOrDefault<UserAccountDTO>(user.get_Accounts(), new Func<UserAccountDTO, bool>(variable, (UserAccountDTO x) => true));
}
```

### 最后

使用 ilasm 将 il 文件 转成 dll

## 参考链接

https://www.jysafe.cn/4785.air

