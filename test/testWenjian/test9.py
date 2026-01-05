#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:23
@Author : 751363075@qq.com
@File : test9.py

f = open('test.txt', 'a+')
exit(-1)
f.close()
"""
with open('test.txt', 'r') as f:
    content = f.readlines()
    for line in content:
        print(line)
