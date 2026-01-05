#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 9:23
@Author : 751363075@qq.com
@File : test6.py
"""
n = 1
s = 'this is a string'
print(type(n))
print(type(s))


class Person:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def who(self):
        return 'I am a Person, my name is {}'.format(self.name)


class Student(Person):
    def __init__(self, name, gender, score):
        super(Student, self).__init__(name, gender)
        self.score = score


p = Person('Alice', 'Female')
s = Student('Bob', 'Male', 100)
print(type(p))
print(type(s))

n = 1
print(dir(n))
s = 'this is a string'
print(dir(s))

p = Person('Alice', 'Female')
print(dir(p))

print(getattr(p, 'name'))
setattr(p, 'name', 'Adam')
print(getattr(p, 'name'))

print(getattr(p, 'age', 20))
