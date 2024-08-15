本文测试环境为`ubuntu 20.04 LTS`

# 安装zsh

查看系统自带shell

```shell
cat /etc/shells
```

如果没有zsh的话，安装zsh并设置为默认shell，然后重启终端

```shell
sudo apt install zsh
chsh -s /bin/zsh
```

# 安装oh-my-zsh

```shell
 sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

安装插件

```shell
cd ~/.oh-my-zsh/custom/plugins/
git clone https://github.com/zsh-users/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git

git clone https://github.com/spaceship-prompt/spaceship-prompt.git "$ZSH_CUSTOM/themes/spaceship-prompt" --depth=1
ln -s "$ZSH_CUSTOM/themes/spaceship-prompt/spaceship.zsh-theme" "$ZSH_CUSTOM/themes/spaceship.zsh-theme"

# 配置文件
vi ~/.zshrc
# 修改主题

ZSH_THEME="spaceship"
# 添加插件
plugins=(
	z
	git
	zsh-autosuggestions
	zsh-syntax-highlighting
	extract
)
# 在最后添加
source ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
# 激活配置文件

```

PS：如果你有一些神秘服务需要设置，可以再添加

```shell
export http_proxy="http://127.0.0.1:10809"
export https_proxy="http://127.0.0.1:10809"
export ALL_PROXY="socks5://127.0.0.1:10808"
```

似乎http走socks5的话，wget命令会报错，干脆走http吧

## 中文乱码

```shell
vim ~/.zshrc
# 在文件末尾添加
export LC_ALL=en_US.UTF-8  
export LANG=en_US.UTF-8
source ~/.zshrc
```

## 一些按键不能用

```shell
vim ~/.zshr
# 在文件末尾添加
# key bindings
bindkey "\e[1~" beginning-of-line
bindkey "\e[4~" end-of-line
bindkey "\e[5~" beginning-of-history
bindkey "\e[6~" end-of-history

# for rxvt
bindkey "\e[8~" end-of-line
bindkey "\e[7~" beginning-of-line
# for non RH/Debian xterm, can't hurt for RH/DEbian xterm
bindkey "\eOH" beginning-of-line
bindkey "\eOF" end-of-line
# for freebsd console
bindkey "\e[H" beginning-of-line
bindkey "\e[F" end-of-line
# completion in the middle of a line
bindkey '^i' expand-or-complete-prefix

# Fix numeric keypad  
# 0 . Enter  
bindkey -s "^[Op" "0"
bindkey -s "^[On" "."
bindkey -s "^[OM" "^M"
# 1 2 3  
bindkey -s "^[Oq" "1"
bindkey -s "^[Or" "2"
bindkey -s "^[Os" "3"
# 4 5 6  
bindkey -s "^[Ot" "4"
bindkey -s "^[Ou" "5"
bindkey -s "^[Ov" "6"
# 7 8 9  
bindkey -s "^[Ow" "7"
bindkey -s "^[Ox" "8"
bindkey -s "^[Oy" "9"
# + - * /  
bindkey -s "^[Ol" "+"
bindkey -s "^[Om" "-"
bindkey -s "^[Oj" "*"
bindkey -s "^[Oo" "/"


source ~/.zshrc
```

