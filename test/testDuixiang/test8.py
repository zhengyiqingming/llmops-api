#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 16:51
@Author : 751363075@qq.com
@File : test8.py
"""


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.__age = age


cat = Animal('cat', 3)
print(cat.name)
print(cat.__age)
