#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 9:50
@Author : 751363075@qq.com
@File : test6.py
"""
from functools import reduce


def f(x, y):
    return x * y


print(reduce(f, [1, 3, 5, 7, 9]))
