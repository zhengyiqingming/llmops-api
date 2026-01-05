#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 16:13
@Author : 751363075@qq.com
@File : test4.py
"""


class Animal:
    location = 'Asia'

    def __init__(self, name, age, location):
        self.name = name
        self.age = age
        self.location = location


dog = Animal('Dog', 1, 'GuangDong')
cat = Animal('Cat', 2, 'ChongQing')
print(dog.location)
print(cat.location)
print(Animal.location)
