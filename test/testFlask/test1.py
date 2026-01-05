#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/26 8:50
@Author : 751363075@qq.com
@File : test1.py
"""
from flask import Flask

# 传入__name__初始化一个Flask实例
app = Flask(__name__)


# 装饰器，将当前路由映射到指定函数
@app.route('/')
def hello_world():
    result = 1 / 0
    return 'Hello World!'


app.config.update(
    DEBUG=True,
)

if __name__ == '__main__':
    app.run()
