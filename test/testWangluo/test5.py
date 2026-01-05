#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/20 21:28
@Author : 751363075@qq.com
@File : test5.py
"""
import requests

response = requests.get("https://www.imooc.com")
# ==> 打印具体内容
content = str(response.content, encoding='utf-8')
print(content)
# 分行
content_list = content.split('\n')
print(len(content_list))
for line in content_list:
    if 'href' in line and 'www' in line:
        print(line.strip())
