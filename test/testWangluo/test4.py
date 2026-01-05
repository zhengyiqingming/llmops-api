#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/20 21:11
@Author : 751363075@qq.com
@File : test4.py
"""
import requests

response = requests.get("https://www.imooc.com")
content = str(response.content, encoding="utf-8")
print(content)
# 分行
content_list = content.split('\n')
print(len(content_list))

for line in content_list:
    if 'href' in line:
        print(line.strip())
