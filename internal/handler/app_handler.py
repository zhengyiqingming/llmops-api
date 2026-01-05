#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 11:26
@Author : 751363075@qq.com
@File : app_handler.py
"""
import os
import uuid
from uuid import UUID
from dataclasses import dataclass

from injector import inject
from openai import OpenAI
from internal.schema.app_schema import CompletionReq
from pkg.response import sucess_json, validate_error_json, sucess_message
from internal.exception import FailedException
from internal.service import AppService
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return sucess_message(f"应用已成功创建，id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return sucess_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return sucess_message(f"应用已经成功修改，修改的名字是{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return sucess_message(f"应用已经成功删除，id为:{app.id}")

    def debug(self, app_id: UUID):
        """聊天接口"""
        # 1.提取从接口中获取的输入,POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.构建组件
        prompt = ChatPromptTemplate.from_template("{query}")
        llm = ChatDeepSeek(model="deepseek-chat")
        parser = StrOutputParser()

        # 3.构建链
        chain = prompt | llm | parser

        # 4.调用链得到结果
        content = chain.invoke({"query": req.query})

        return sucess_json({"content": content})

    def ping(self):
        raise FailedException("数据未找到")
        # return {"ping": "pong"}
