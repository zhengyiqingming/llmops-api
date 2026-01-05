#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 9:54
@Author : 751363075@qq.com
@File : test7.py
"""


# 编写一个判断奇数的函数
def is_odd(x):
    return x % 2 == 1


for item in filter(is_odd, [1, 4, 6, 7, 9, 12, 17]):
    print(item)
