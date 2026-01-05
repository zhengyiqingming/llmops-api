#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 16:21
@Author : 751363075@qq.com
@File : test5.py
"""


class Animal:
    location = 'Asia'

    def __init__(self, name, age):
        self.name = name
        self.age = age


cat = Animal("cat", 1)
print(cat.location)
cat.location = 'Afica'
print(Animal.location)
print(cat.location)
