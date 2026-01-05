#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 16:00
@Author : 751363075@qq.com
@File : test3.py
"""


class Animal:
    location = 'Asia'

    def __init__(self, name, age):
        self.name = name
        self.age = age


dog = Animal('Dog', 1)
cat = Animal('Cat', 2)
print(dog.location)
print(cat.location)
print(Animal.location)

Animal.location = 'Afica'
print(dog.location)
print(cat.location)
