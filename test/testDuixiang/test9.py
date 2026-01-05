#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 17:07
@Author : 751363075@qq.com
@File : test9.py
"""


class Person:
    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name


p = Person('John')
print(p.getName())
