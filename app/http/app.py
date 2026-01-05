#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/22 15:16
@Author : 751363075@qq.com
@File : http.py
"""
import dotenv
from flask_migrate import Migrate
from flask_migrate import Migrate

from pkg.sqlalchemy import SQLAlchemy
from injector import Injector, Binder, Module
from internal.server import Http
from internal.router import Router
from config import Config

from .module import ExtensionModule

# 将env加载到环境变量中
dotenv.load_dotenv()

conf = Config()

injector = Injector([ExtensionModule])

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),
    router=injector.get(Router),
)

if __name__ == '__main__':
    app.run(debug=True)
