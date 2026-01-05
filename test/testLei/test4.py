#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 9:06
@Author : 751363075@qq.com
@File : test4.py
"""


class A:
    def __init__(self, a):
        print('init A...')
        self.a = a


class B(A):
    def __init__(self, a):
        super(B, self).__init__(a)
        print('init B...')


class C(A):
    def __init__(self, a):
        super(C, self).__init__(a)
        print('init C...')


class D(B, C):
    def __init__(self, a):
        super(D, self).__init__(a)
        print('init D...')


d = D('d')
