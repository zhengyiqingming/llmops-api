#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 9:15
@Author : 751363075@qq.com
@File : test5.py
"""


class Person:
    pass


class Student(Person):
    pass


class Teacher(Person):
    pass


class SkillMixin:
    pass


class BasketballMixin(SkillMixin):
    def skill(self):
        return 'Basketball'


class FootballMixin(SkillMixin):
    def skill(self):
        return 'Football'


class Bstudent(BasketballMixin, Student):
    pass


class FTeacher(FootballMixin, Teacher):
    pass


s = Bstudent()
print(s.skill())

t = FTeacher()
print(t.skill())
