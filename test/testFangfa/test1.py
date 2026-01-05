#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 9:43
@Author : 751363075@qq.com
@File : test1.py
"""
num = 12
print(str(num))
d = {1: 1, 2: 2}
print(d)
l = [1, 2, 3, 4, 5]
print(str(l))
print(dir(l))


class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def __str__(self):
        return 'name:{},gender:{}'.format(self.name, self.gender)


bob = Person('bob', 'Male')
print(str(bob))
print(bob)
