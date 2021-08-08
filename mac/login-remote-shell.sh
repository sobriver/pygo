#!/usr/bin/expect -f
# ssh登录用户名
user=root
# ssh登录密码
password=hlwi1991
# 服务器ip
host=10.0.0.239
# ssh端口
port=2222

# ssh 连接主机 用admin连接
spawn ssh -p $port $user@$host
expect "*assword:*"
send "$password\r"
interact
expect eof
