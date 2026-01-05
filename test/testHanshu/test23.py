#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 12:04
@Author : 751363075@qq.com
@File : test23.py
"""
import functools

int2 = functools.partial(int, base=2)
print(int2('1000000'))
print(int2('1010101'))
