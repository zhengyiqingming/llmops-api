#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/29 17:42
@Author : 751363075@qq.com
@File : module.py
"""
from redis import Redis

from internal.core.language_model import LanguageModelManager
from pkg.sqlalchemy import SQLAlchemy
from flask_weaviate import FlaskWeaviate
from injector import Module, Binder, Injector, singleton

from internal.extension.database_extension import db
from internal.extension.redis_extension import redis_client
from flask_migrate import Migrate
from internal.extension.migrate_extension import migrate
from flask_login import LoginManager
from internal.extension.login_extension import login_manager
from internal.extension.weaviate_extension import weaviate


class ExtensionModule(Module):
    """扩展模块的依赖注入"""

    def configure(self, binder: Binder) -> None:
        # 将类声明绑定到实例上
        binder.bind(SQLAlchemy, to=db)
        binder.bind(FlaskWeaviate, to=weaviate)
        binder.bind(Migrate, to=migrate)
        binder.bind(Redis, to=redis_client)
        binder.bind(LoginManager, to=login_manager)
        binder.bind(
            LanguageModelManager,
            to=lambda: LanguageModelManager(),  # 使用工厂函数
            scope=singleton
        )


injector = Injector([ExtensionModule])
