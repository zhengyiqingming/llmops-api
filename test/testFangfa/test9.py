#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 15:36
@Author : 751363075@qq.com
@File : test9.py
"""


class Fib(object):
    def __init__(self):
        self.res = []

    def __call__(self, num):
        a = 0
        b = 1
        for x in range(num):
            self.res.append(a)
            a, b = b, a + b
        return self.res


f = Fib()
print(f(10))
