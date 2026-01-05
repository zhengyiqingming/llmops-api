#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/4 11:06
@Author : 751363075@qq.com
@File : 2.LCEL表达式简化版本.py
"""
from typing import Any

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatDeepSeek(model="deepseek-chat")
parser = StrOutputParser()

# 2.创建链
chain = prompt | llm | parser

# 3.调用链得到结果
print(chain.invoke({"query": "请讲一个程序员的冷笑话"}))
