#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 9:41
@Author : 751363075@qq.com
@File : test4.py
"""


def format_name(s):
    return s[0].upper() + s[1:].lower()


for item in map(format_name, ['alice', 'BOB', 'CanDY']):
    print(item)
