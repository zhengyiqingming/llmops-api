#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/19 17:25
@Author : 751363075@qq.com
@File : test10.py
"""
with open('test.txt', 'a+') as f:
    f.seek(0)
    content = f.readlines()
    f.seek(2)
    for line in content:
        f.write(line)
