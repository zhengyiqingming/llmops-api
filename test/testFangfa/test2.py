#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 9:55
@Author : 751363075@qq.com
@File : test2.py
"""


class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    def __init__(self, name, gender, score):
        super().__init__(name, gender)
        self.score = score

    def __str__(self):
        return 'Student:{},{},{}'.format(self.name, self.gender, self.score)

    def __repr__(self):
        return 'Student:{},{},{}'.format(self.name, self.gender, self.score)


s = Student('bob', 'Male', 100)
print(s)
