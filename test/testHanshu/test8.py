#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 9:57
@Author : 751363075@qq.com
@File : test8.py
"""


def is_not_empty(s):
    return s and len(s.strip()) > 0


for item in filter(is_not_empty, ['test', None, '', 'str', ' ', 'END']):
    print(item)
