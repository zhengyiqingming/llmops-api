#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/14 19:12
@Author : 751363075@qq.com
@File : google_serper.py
"""
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field

from internal.core.tools.builtin_tools.providers.gaode.gaode_weather import GaodeWeatherArgsSchema
from internal.lib.helper import add_attribute


class GoogleSerperArgsSchema(BaseModel):
    """谷歌搜索API搜索参数描述"""
    query: str = Field(description="执行谷歌搜索的查询语句")


@add_attribute("args_schema", GoogleSerperArgsSchema)
def google_serper(**kwargs) -> BaseTool:
    """谷歌Serp搜索"""
    return GoogleSerperRun(
        name="google_serper",
        description="这是一个低成本的谷歌搜索API，当你需要搜索时事的问题时，可以调用该工具，该工具传递的参数是搜索查询语句",
        args_schema=GoogleSerperArgsSchema,
        api_wrapper=GoogleSerperAPIWrapper(),
    )
