#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 9:35
@Author : 751363075@qq.com
@File : test7.py
"""


class Person:
    def __init__(self, name, gender, **kw):
        self.name = name
        self.gender = gender
        for k, v in kw.items():
            setattr(self, k, v)


p = Person('Bob', 'Male', age=18, course='Python')
print(p.age)
print(p.course)

list_ = [1, 2, 3, 4, 5]
print(list_)
print(p)
print(list_.__str__())
print(p.__str__())
