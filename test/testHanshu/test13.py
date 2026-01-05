#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:31
@Author : 751363075@qq.com
@File : test13.py
"""


def f():
    print('call f()...')

    # 定义函数g:
    def g():
        print('call g()...')

    # 返回函数g:
    return g


x = f()
print(x)
x()
