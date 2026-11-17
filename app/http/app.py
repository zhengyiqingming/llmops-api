#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 15:16
@Author : 751363075@qq.com
@File : http.py
"""
import dotenv
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_weaviate import FlaskWeaviate

from internal.middleware import Middleware
from pkg.sqlalchemy import SQLAlchemy
from internal.server import Http
from internal.router import Router
from config import Config

from .module import injector

# 将env加载到环境变量中
dotenv.load_dotenv()

conf = Config()

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),  # 通过类声明获取实例
    weaviate=injector.get(FlaskWeaviate),
    migrate=injector.get(Migrate),  # 通过类声明获取实例
    login_manager=injector.get(LoginManager),  # 通过类声明获取实例
    middleware=injector.get(Middleware),
    router=injector.get(Router),  # 通过类声明获取实例
)

celery = app.extensions["celery"]

if __name__ == '__main__':
    app.run(debug=True)
