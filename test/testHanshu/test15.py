#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:36
@Author : 751363075@qq.com
@File : test15.py
"""


def calc_sum(list_):
    def lazy_sum():
        return sum(list_)

    return lazy_sum


f = calc_sum([1, 2, 3, 4])
print(f)
print(f())
