#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/26 16:13
@Author : 751363075@qq.com
@File : google_serper_tool.py
"""
import dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import GoogleSerperAPIWrapper

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


google_serper = GoogleSerperRun(
    name="google_serper",
    description=(
        "一个低成本的谷歌搜索API。"
        "当你需要回答有关时事的问题时，可以调用该工具。"
        "该工具传递的参数是搜索查询语句。"
    ),
    args_schema=GoogleSerperArgsSchema,
    api_wrapper=GoogleSerperAPIWrapper(),
)

print(google_serper.invoke("马拉松的世界纪录是多少？"))
