#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 8:52
@Author : 751363075@qq.com
@File : test3.py
"""


def f(x):
    return x * x


for item in map(f, [-1, 2, 3, 4, 5, 6, 7, 8.8, 9.9]):
    print(item)
