#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 14:50
@Author : 751363075@qq.com
@File : test6.py
"""


class Student(object):
    __slots__ = ('name', 'gender', 'score')

    def __init__(self, name, gender, score):
        self.name = name
        self.gender = gender
        self.score = score


student = Student('Bob', 'Male', 99)
student.age = 18
