#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:39
@Author : 751363075@qq.com
@File : test16.py
"""
from functools import reduce


def calc_prod(list_):
    def lazy_prod():
        def f(x, y):
            return x * y

        return reduce(f, list_, 1)

    return lazy_prod


f = calc_prod([1, 2, 3, 4])
print(f)
print(f())
