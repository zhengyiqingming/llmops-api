#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:30
@Author : 751363075@qq.com
@File : server.py
"""
import socket

# 1. 新建socket
server = socket.socket()
# 2. 绑定IP和端口（其中127.0.0.1为本机回环IP）
server.bind(('127.0.0.1', 8999))
# 3. 监听连接
server.listen(5)
# 4. 接受连接
s, addr = server.accept()
print('connect addr:{}'.format(addr))
# 接受来自客户端的消息，并编码打印出来
content = s.recv(1024)
print(str(content, encoding='utf-8'))
s.close()
