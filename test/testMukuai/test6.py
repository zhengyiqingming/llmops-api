#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 16:50
@Author : 751363075@qq.com
@File : test6.py
"""
num = input('please input a number:')
num = int(num)
result = 1
for i in range(1, num):
    result = result * i

print(result)
