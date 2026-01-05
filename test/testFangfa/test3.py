#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 14:16
@Author : 751363075@qq.com
@File : test3.py
"""


class Class:
    def __init__(self, students):
        self.students = students

    """def __len__(self):
        return len(self.students)"""


students = ['Alice', 'Bob', 'Candy']
class_ = Class(students)
print(len(class_))
