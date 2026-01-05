#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:01
@Author : 751363075@qq.com
@File : test9.py
"""
import math


def is_sqrt(x):
    r = int(math.sqrt(x))
    return r * r == x


for item in filter(is_sqrt, range(1, 101)):
    print(item)
