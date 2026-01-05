#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 15:45
@Author : 751363075@qq.com
@File : test2.py
"""


class Person:
    def __init__(self, name, sex, age):
        self.name = name
        self.sex = sex
        self.age = age


xiaoming = Person('Xiao Ming', 'boy', 13)
xiaohong = Person('Xiao Hong', 'girl', 14)
print(xiaohong.name)
print(xiaohong.sex)
print(xiaohong.age)
