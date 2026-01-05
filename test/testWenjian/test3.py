#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:03
@Author : 751363075@qq.com
@File : test3.py
"""
f = open('test.txt', 'r')
s = f.read(5)
print(s)
s = f.read(6)
print(s)
f.close()
f = open('test.txt', 'r')
s = f.readline(20)
print(s)
f.close()
f = open('test.txt', 'r')
s = f.readlines()
print(s)
f.close()
f = open('main.py')
content = f.readlines()
print(content)
