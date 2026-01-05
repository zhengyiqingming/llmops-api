#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:12
@Author : 751363075@qq.com
@File : test5.py
"""
f = open('test.txt', 'r')
lines = f.readlines()
f1 = open('test.txt', 'w')
for line in lines:
    line = line[::-1]
    f1.write(line)

f1.close()
f.close()
