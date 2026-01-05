#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/26 9:08
@Author : 751363075@qq.com
@File : test2.py
"""
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/corly')
def hello_corly():
    return '这个是我的第一个flask页面'


@app.route('/list/<int:aid>')
def article_list(aid):
    return '这是第{}篇文章'.format(aid)


@app.route('/list/<path:aid>')
def comment_list(aid):
    return '这是第{}个评论'.format(aid)


@app.route('/<any(notice,follow):url_path>/')
def message(url_path):
    return url_path


@app.route('/wd')
def baidu_search():
    return request.args.get('keyword')


if __name__ == '__main__':
    app.run(debug=True)
