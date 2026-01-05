#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 10:21
@Author : 751363075@qq.com
@File : test10.py
"""
score = [('Alice', 72), ('Candy', 90), ('Bob', 62)]
print(sorted(score))


# ==> 按成绩排序，成绩是第二个字段
def k(item):
    return item[1]


print(sorted(score, key=k))

print(sorted(score, key=k, reverse=True))
