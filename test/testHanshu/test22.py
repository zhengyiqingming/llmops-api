#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 11:55
@Author : 751363075@qq.com
@File : test22.py
"""
import time
from functools import reduce


def performance(unit):
    def pref_decorator(f):
        def wrapper(*args, **kwargs):
            t1 = time.time()
            r = f(*args, **kwargs)
            t2 = time.time()
            t = (t2 - t1) * 1000 if unit == 'ms' else (t2 - t1)
            print('call {}() in {}{}'.format(f.__name__, t, unit))
            return r

        return wrapper

    return pref_decorator


@performance('ms')
def factorial(n):
    return reduce(lambda x, y: x * y, range(1, n + 1))


print(factorial(10))
