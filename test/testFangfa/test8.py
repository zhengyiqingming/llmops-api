#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 15:32
@Author : 751363075@qq.com
@File : test8.py
"""


class Person(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def __call__(self, friend):
        print('My name is {}...'.format(self.name))
        print('My friend is {}...'.format(friend))


p = Person('Bob', 'Male')
p('Alice')
