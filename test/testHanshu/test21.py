#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 11:26
@Author : 751363075@qq.com
@File : test21.py
"""


def log(prefix):
    def log_decorator(f):
        def wrapper(*args, **kwargs):
            print('[{}]{}()...'.format(prefix, f.__name__))
            return f(*args, **kwargs)

        return wrapper

    return log_decorator


@log('DEBUG')
def test():
    pass


test()
