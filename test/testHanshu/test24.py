#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 12:08
@Author : 751363075@qq.com
@File : test24.py
"""
import functools

sorted_ignore_case = functools.partial(sorted, key=lambda item: item.lower())
list_ = sorted_ignore_case(['bob', 'about', 'Zoo', 'Credit'])
print(list_)
