#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 17:12
@Author : 751363075@qq.com
@File : test10.py
"""


class Animal:
    def __init__(self, name, age, location):
        self.__name = name
        self.__age = age
        self.__location = location

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_age(self, age):
        self.__age = age

    def get_age(self):
        return self.__age

    def set_location(self, location):
        self.__location = location

    def get_location(self):
        return self.__location


dog = Animal('dog', 3, 'GuangGong')
print(dog.get_name())
print(dog.get_age())
print(dog.get_location())
