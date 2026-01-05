#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 11:15
@Author : 751363075@qq.com
@File : test20.py
"""
import time
from functools import reduce


def performance(f):
    def fn(*args, **kw):
        t1 = time.time()
        r = f(*args, **kw)
        t2 = time.time()
        print('call %s() in %fs' % (f.__name__, (t2 - t1)))
        return r

    return fn


@performance
def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n + 1))


print(factorial(10))
