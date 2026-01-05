#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/29 17:15
@Author : 751363075@qq.com
@File : default_config.py
"""
# 应用默认配置项
DEFAULT_CONFIG = {
    # wft配置
    "WTF_CSRF_ENABLED": "False",
    # SQLAlchemy数据库配置项
    "SQLALCHEMY_DATABASE_URI": "",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": "True"
}
