#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 14:54
@Author : 751363075@qq.com
@File : test7.py
"""


class Person:
    __slots__ = ('name', 'gender')

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    __slots__ = ('score',)

    def __init__(self, name, gender, score):
        self.name = name
        self.gender = gender
        self.score = score


s = Student('Bob', 'male', 59)
s.name = 'Tim'
s.score = 99
print(s.score)
print(s.name)
print(s.gender)
