#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/20 20:43
@Author : 751363075@qq.com
@File : test3.py
"""
import requests

response = requests.get("http://127.0.0.1:9999")
print(response.status_code)
print(response.headers)
