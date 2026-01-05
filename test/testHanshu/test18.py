#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:58
@Author : 751363075@qq.com
@File : test18.py

result = [item for item in map(lambda x: x * x, [1, 2, 3, 4, 5, 6, 7, 8, 9])]
print(result)

from functools import reduce

num = reduce(lambda x, y: x + y, [1, 3, 5, 7, 9])
print(num)
"""
list_ = ['bob', 'about', 'Zoo', 'Credit']
k = lambda item: item.lower()
print(sorted(list_, key=k))
