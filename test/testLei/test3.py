#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 8:54
@Author : 751363075@qq.com
@File : test3.py
"""


class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def who(self):
        return 'I am a person, my name is %s' % self.name


class Student(Person):
    def __init__(self, name, gender, score):
        super().__init__(name, gender)
        self.score = score

    def who(self):
        return 'I am a Student, my name is %s' % self.name


class Teacher(Person):
    def __init__(self, name, gender, course):
        super().__init__(name, gender)
        self.course = course

    def who(self):
        return 'I am a Teacher, my name is %s' % self.name


p = Person('Tim', 'Male')
s = Student('John', 'Male', 100)
t = Teacher('Alice', 'FeMale', 'English')
print(p.who())
print(s.who())
print(t.who())


class Boss(Person):
    def __init__(self, name, gender, company):
        super().__init__(name, gender)
        self.company = company


b = Boss('Bob', 'Male', 'Alibaba')
print(b.who())
