#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:09
@Author : 751363075@qq.com
@File : test4.py

f = open('test.txt', 'w')
f.write('hello world\n')
f.close()
"""

lines = ['hello world\n', 'hello python\n', 'hello Imooc\n']
f = open('test.txt', 'w')
f.writelines(lines)
f.close()
