#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 11:05
@Author : 751363075@qq.com
@File : test19.py
"""
from functools import reduce


def log(f):
    def fn(*args, **kwargs):
        print('call' + f.__name__ + '()...')
        return f(*args, **kwargs)

    return fn


@log
def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n + 1))


print(factorial(10))


@log
def add(a, b):
    return a + b


print(add(1, 2))
