#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/24 11:38
@Author : 751363075@qq.com
@File : 1.DuckDuckGo搜索.py
"""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.utils.function_calling import convert_to_openai_tool

serach = DuckDuckGoSearchRun(description="xxx")

print(convert_to_openai_tool(serach))
print("名字: ", serach.name)
print("描述: ", serach.description)
print("参数: ", serach.args)
print("是否直接返回: ", serach.return_direct)
print(serach.invoke("LangChain目前最新版本是什么?"))
