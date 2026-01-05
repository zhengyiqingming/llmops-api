#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/20 20:37
@Author : 751363075@qq.com
@File : test2.py
"""
import requests

response = requests.get("http://www.imooc.com")
# 打印状态码
print(response.status_code)
# 打印回应头
print(response.headers)
