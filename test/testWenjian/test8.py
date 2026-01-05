#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:20
@Author : 751363075@qq.com
@File : test8.py
"""
f = open('test.txt', 'a+')
f.seek(0)
content = f.readlines()
f.seek(2)
for line in content:
    f.write(line)
f.close()
