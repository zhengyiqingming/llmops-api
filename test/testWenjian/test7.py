#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:17
@Author : 751363075@qq.com
@File : test7.py
"""
f = open('test.txt', 'a+')
content = f.readlines()
print(content)
f.seek(0)
content = f.readlines()
print(content)
