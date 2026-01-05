#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 8:48
@Author : 751363075@qq.com
@File : test1.py
"""


def add(x, y, f):
    return f(x) + f(y)


num = add(-5, 9, abs)
print(num)
