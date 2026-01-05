#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 16:46
@Author : 751363075@qq.com
@File : test7.py
"""


class Animal(object):

    def __init__(self, name, age, location):
        self.name = name
        self.age = age
        self.__location = location


dog = Animal('Dog', 1, 'GuangDong')
print(dog.name)
print(dog.age)
print(dog.__location)
