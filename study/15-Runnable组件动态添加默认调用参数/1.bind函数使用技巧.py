#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/15 16:36
@Author : 751363075@qq.com
@File : 1.bind函数使用技巧.py
"""
import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.构建组件
prompt = ChatPromptTemplate.from_messages([
    ("human", "{query}")
])
llm = ChatOpenAI(
    model="kimi-k2-instruct",
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
)

# 2.定义一个链
chain = prompt | llm.bind(model="deepseek-v3.1-250821") | StrOutputParser()

# 4.执行链并获取结果
content = chain.invoke({"query": "你是什么大模型呢?对应什么版本？"})

print(content)
