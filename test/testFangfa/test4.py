#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 14:20
@Author : 751363075@qq.com
@File : test4.py
"""


class Fib:
    def __init__(self, num):
        self.res = []
        self.num = num
        a = 0
        b = 1
        """从0到num-1循环"""
        for x in range(num):
            self.res.append(a)
            a, b = b, a + b

    def __str__(self):
        return str(self.res)

    def __len__(self):
        return self.num


f = Fib(10)
print(f)
print(len(f))
