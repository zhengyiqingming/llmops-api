#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 17:20
@Author : 751363075@qq.com
@File : test11.py
"""


class Animal:
    __location = 'Asia'
    __count = 0

    def __init__(self, name, age):
        self.__name = name
        self.__age = age
        Animal.__count += 1

    @classmethod
    def set_location(cls, location):
        cls.__location = location

    @classmethod
    def get_location(cls):
        return cls.__location

    @classmethod
    def get_count(cls):
        return cls.__count


dog = Animal('Dog', 1)
cat = Animal('Cat', 2)
pig = Animal('Pig', 3)

count = Animal.get_count()
print(count)

print(Animal.get_location())
Animal.set_location('Afica')
print(Animal.get_location())
