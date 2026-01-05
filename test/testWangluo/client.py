#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:33
@Author : 751363075@qq.com
@File : client.py
"""
import socket

# 1. 新建socket
client = socket.socket()
# 2. 连接服务端（注意，IP和端口要和服务端一致）
client.connect(('127.0.0.1', 8999))
# 发送内容，注意发送的是字节字符串。
client.send(bytes('hello world,hello socket', encoding='utf-8'))
client.close()
