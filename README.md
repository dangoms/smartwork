# smartwork
Smartwork is a helpful tool designed to deal with daily work automatically. Welcome to contribute your codes to complete it.


# 如何快速开发一个推送消息的机器人
准备一台windows系统的PC，Linux更好。本指导主要向面使用Windows系统的办公用户。对于有开发基础的用户，可以DIY自己的开发环境，不做要求。


## 安装开发语言Python3
https://www.python.org/downloads/

## 安装代码版本管控工具Git
https://git-scm.com/

## 环境变量检查以及配置
在command line中测试Git和Python是否正常工作，期望看到以下输出：
```
C:\Users\T440P>git
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           [--super-prefix=<path>] [--config-env=<name>=<envvar>]
           <command> [<args>]
...
C:\Users\T440P>python
Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## 拉基础代码：
代码主页：https://github.com/dangoms/smartwork
在command line中：
```
git clone git@github.com:dangoms/smartwork.git
```

以上命令会提示无权限问题。本来期望更简单的环境配置，不需要ssh key都可以随意拉此repo的代码，但因为github的安全限制，拉代码必须要向服务器添加ssh key。所以需要以下步骤：
### 生成本地ssh key
对于本地没有生成过ssh key的用户，在Git bash中生成ssh key：
```
$ ssh-keygen -t ed25519 -C "your_email@example.com"
```
或者
```
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
任选其中一条，生成过程中一直按回车，直接退出到command line提示符。

### 添加ssh key到Github：
使用记事本打开.ssh下面的.pub文件，发送我添加ssh key，再拉代码。
```
C:\Users\T440P>type .ssh\id_rsa.pub
```

如果你不打算贡献和协同开发，可以不用Git拉代码，基础代码比较少，直接复制到本地搭建你的机器人环境。