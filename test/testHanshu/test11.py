#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:24
@Author : 751363075@qq.com
@File : test11.py
"""


def k(item):
    return item.lower()


name_list = ['bob', 'about', 'Zoo', 'Credit']

print(sorted(name_list, key=k))
