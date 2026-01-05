#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:46
@Author : 751363075@qq.com
@File : test17.py



def f():
    print('f()...')

    def g():
        print('g()...')

    return g


def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i * i

        fs.append(f)
    return fs


f1, f2, f3 = count()
print(f1())
print(f2())
print(f3())
"""


def count():
    fs = []
    for i in range(1, 4):
        def f(j):
            def g():
                return j * j

            return g

        r = f(i)
        fs.append(r)
    return fs


f1, f2, f3 = count()
print(f1(), f2(), f3())
