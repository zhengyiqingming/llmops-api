#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/16 10:23
@Author : 751363075@qq.com
@File : 2.Runnable回退机制.py
"""
import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")

# 月之暗面：
kimi = ChatOpenAI(
    model="kimi-k2-instruct",
    api_key=os.environ.get("QIANFAN_API_KEY"),
    base_url=os.environ.get("QIANFAN_BASE_URL"),
)
llm = ChatOpenAI(
    model="deepseek-v4",
).with_fallbacks([kimi])

# 2.构建链应用
chain = prompt | llm | StrOutputParser()

# 3.调用链并输出结果
content = chain.invoke({"query": "你好，你是？"})
print(content)
