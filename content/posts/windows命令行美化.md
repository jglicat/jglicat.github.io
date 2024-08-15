---
title: windows命令行美化
date: 2021-12-09 15:22:39
tags: windows
---



`颜值即正义`

众所周知windows自带的cmd和powershell又丑又难用，所以需要改进一下

# 软件安装

## Windows Terminal

[Windows Terminal](https://docs.microsoft.com/zh-cn/windows/terminal/)是微软推出的命令行工具，还是很好用的，推荐用[Store](https://www.microsoft.com/zh-cn/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab)安装，比较省心。

## Powershell

win10/11自带的还是Powershell 5，略老，目前最新的版本是[7.2](https://docs.microsoft.com/zh-cn/powershell/scripting/overview?view=powershell-7.2)，下载安装即可，建议msi文件安装。安装完成后会自动整合进Windows Terminal。

# 美化配置

## 下载字体

首先得整点支持Nerd-fonts的字体，用来在终端下显示各种图标，比如[Fira Code Nerd Font](https://link.zhihu.com/?target=https%3A//github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/FiraCode.zip)。

## 安装Powershell插件

```powershell
# 1. 安装 PSReadline 包，该插件可以让命令行很好用，类似 zsh
Install-Module -Name PSReadLine  -Scope CurrentUser

# 2. 安装 posh-git 包，让你的 git 更好用
Install-Module posh-git  -Scope CurrentUser

# 如果之前安装过，需要先卸载
Uninstall-Module oh-my-posh -AllVersions
# 3. 安装 oh-my-posh 包，让你的命令行更酷炫、优雅
# Install-Module oh-my-posh -Scope CurrentUser
winget install oh-my-posh
```

## 配置 Windows Terminal

在json文件里更改

```json
{
    "acrylicOpacity": 0.5,
    "closeOnExit": "graceful",
    "colorScheme": "Homebrew",
    "commandline": "C:/Program Files/PowerShell/7/pwsh.exe -nologo",
    "cursorColor": "#FFFFFF",
    "cursorShape": "bar",
    "experimental.retroTerminalEffect": false,
    "font": 
    {
        "face": "FiraCode Nerd Font",
        "size": 11
    },
    "guid": "{574e775e-4f2a-5b96-ac1e-a2962a402336}",
    "hidden": false,
    "historySize": 9001,
    "icon": "ms-appx:///ProfileIcons/pwsh.png",
    "name": "PowerShell",
    "padding": "5, 5, 20, 25",
    "snapOnInput": true,
    "source": "Windows.Terminal.PowershellCore",
    "startingDirectory": "C:/File/OneDrive/code",
    "useAcrylic": false
}
```

然后添加配色

```
{
    "name": "Homebrew",
    "black": "#000000",
    "red": "#FC5275",
    "green": "#00a600",
    "yellow": "#999900",
    "blue": "#6666e9",
    "purple": "#b200b2",
    "cyan": "#00a6b2",
    "white": "#bfbfbf",
    "brightBlack": "#666666",
    "brightRed": "#e50000",
    "brightGreen": "#00d900",
    "brightYellow": "#e5e500",
    "brightBlue": "#0000ff",
    "brightPurple": "#e500e5",
    "brightCyan": "#00e5e5",
    "brightWhite": "#e5e5e5",
    "background": "#283033",
    "foreground": "#00ff00"
}
```

配色也可以从[这里](https://windowsterminalthemes.dev/)找

## 添加Powershell 启动参数

```powershell
notepad.exe $Profile
```

复制进去

```
# 初始化oh my posh，把%HOMEPATH%换成你的用户路径
oh-my-posh init pwsh  --config %HOMEPATH%\AppData\Local\Programs\oh-my-posh\themes\hunk.omp.json | Invoke-Expression

#------------------------------- Import Modules BEGIN -------------------------------
# 引入 posh-git
Import-Module posh-git

# 引入 oh-my-posh
# Import-Module oh-my-posh

# 引入 ps-read-line
Import-Module PSReadLine

# 设置 PowerShell 主题
# Set-PoshPrompt ys
# Set-PoshPrompt unicorn
#------------------------------- Import Modules END   -------------------------------





#-------------------------------  Set Hot-keys BEGIN  -------------------------------
# 设置预测文本来源为历史记录
Set-PSReadLineOption -PredictionSource History

# 每次回溯输入历史，光标定位于输入内容末尾
Set-PSReadLineOption -HistorySearchCursorMovesToEnd

# 设置 Tab 为菜单补全和 Intellisense
Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete

# 设置 Ctrl+d 为退出 PowerShell
Set-PSReadlineKeyHandler -Key "Ctrl+d" -Function ViExit

# 设置 Ctrl+z 为撤销
Set-PSReadLineKeyHandler -Key "Ctrl+z" -Function Undo

# 设置向上键为后向搜索历史记录
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward

# 设置向下键为前向搜索历史纪录
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
#-------------------------------  Set Hot-keys END    -------------------------------





#-------------------------------    Functions BEGIN   -------------------------------
# Python 直接执行
$env:PATHEXT += ";.py"

# 更新系统组件
function Update-Packages {
	# update pip
	Write-Host "Step 1: 更新 pip" -ForegroundColor Magenta -BackgroundColor Cyan
	$a = pip list --outdated
	$num_package = $a.Length - 2
	for ($i = 0; $i -lt $num_package; $i++) {
		$tmp = ($a[2 + $i].Split(" "))[0]
		pip install -U $tmp
	}

	# update TeX Live
	$CurrentYear = Get-Date -Format yyyy
	Write-Host "Step 2: 更新 TeX Live" $CurrentYear -ForegroundColor Magenta -BackgroundColor Cyan
	tlmgr update --self
	tlmgr update --all

	# update Chocolotey
	Write-Host "Step 3: 更新 Chocolatey" -ForegroundColor Magenta -BackgroundColor Cyan
	choco outdated
}
#-------------------------------    Functions END     -------------------------------





#-------------------------------   Set Alias BEGIN    -------------------------------
# 1. 编译函数 make
function MakeThings {
	nmake.exe $args -nologo
}
Set-Alias -Name make -Value MakeThings

# 2. 更新系统 os-update
Set-Alias -Name os-update -Value Update-Packages

# 3. 查看目录 ls & ll
function ListDirectory {
	(Get-ChildItem).Name
	Write-Host("")
}
Set-Alias -Name ls -Value ListDirectory
Set-Alias -Name ll -Value Get-ChildItem

# 4. 打开当前工作目录
function OpenCurrentFolder {
	param
	(
		# 输入要打开的路径
		# 用法示例：open C:\
		# 默认路径：当前工作文件夹
		$Path = '.'
	)
	Invoke-Item $Path
}
Set-Alias -Name open -Value OpenCurrentFolder
#-------------------------------    Set Alias END     -------------------------------





#-------------------------------   Set Network BEGIN    -------------------------------
# 1. 获取所有 Network Interface
function Get-AllNic {
	Get-NetAdapter | Sort-Object -Property MacAddress
}
Set-Alias -Name getnic -Value Get-AllNic

# 2. 获取 IPv4 关键路由
function Get-IPv4Routes {
	Get-NetRoute -AddressFamily IPv4 | Where-Object -FilterScript {$_.NextHop -ne '0.0.0.0'}
}
Set-Alias -Name getip -Value Get-IPv4Routes

# 3. 获取 IPv6 关键路由
function Get-IPv6Routes {
	Get-NetRoute -AddressFamily IPv6 | Where-Object -FilterScript {$_.NextHop -ne '::'}
}
Set-Alias -Name getip6 -Value Get-IPv6Routes
#-------------------------------    Set Network END     -------------------------------
```

然后重启终端，Get-PoshThemes查看主题，选择一个自己喜欢的替换Set-PoshPrompt的值，具体配置可以在

```powershell
%HOMEPATH% \Documents\PowerShell\Modules\oh-my-posh\themes
```

里设置

## 添加sudo

```shell
winget install gsudo
```



------

参考网址：

https://zhuanlan.zhihu.com/p/137595941

https://drrany.github.io/wt/#%E9%9A%90%E8%97%8F%E4%B8%BB%E6%9C%BA%E5%90%8D

https://blog.csdn.net/Y1575071736/article/details/120616233
