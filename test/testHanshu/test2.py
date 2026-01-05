#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 8:49
@Author : 751363075@qq.com
@File : test2.py
"""
import math


def add(x, y, f):
    return f(x) + f(y)


print(add(25, 9, math.sqrt))
