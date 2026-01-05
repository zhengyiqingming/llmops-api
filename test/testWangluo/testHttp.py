#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:51
@Author : 751363075@qq.com
@File : testHttp.py
"""
from urllib import request

# 向慕课网官网发送请求
response = request.urlopen("http://127.0.0.1:9999/")
print(response)
print(response.status)
for k, v in response.getheaders():
    print('{}:{}'.format(k, v))
