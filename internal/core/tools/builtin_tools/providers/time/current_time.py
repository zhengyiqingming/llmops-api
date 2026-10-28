#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/16 17:38
@Author : 751363075@qq.com
@File : current_time.py
"""
from datetime import datetime
from typing import Any, Type

from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel


class CurrentTimeTool(BaseTool):
    """一个用于获取当前时间的工具"""
    name = "current_time"
    description = "一个用于获取当前时间的工具"
    args_schema: Type[BaseModel] = BaseModel

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """获取当前系统的时间，并进行格式化后返回"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")


def current_time(**kwargs) -> BaseTool:
    """返回获取当前时间的langchain工具"""
    return CurrentTimeTool()
