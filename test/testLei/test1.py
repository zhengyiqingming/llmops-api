# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 17:42
@Author : 751363075@qq.com
@File : test1.py
"""


class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender


class Student(Person):
    def __init__(self, name, gender, score):
        Person.__init__(self, name, gender)
        self.score = score


class Teacher(Person):
    def __init__(self, name, gender, course):
        Person.__init__(self, name, gender)
        self.course = course


student = Student('Alice', 'girl', 100)
print(student.name)
print(student.gender)
print(student.score)

teacher = Teacher('Alice', 'Female', 'English')
print(teacher.name)
print(teacher.gender)
print(teacher.course)
