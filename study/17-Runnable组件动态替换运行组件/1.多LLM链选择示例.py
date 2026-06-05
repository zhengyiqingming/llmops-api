#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/16 9:26
@Author : 751363075@qq.com
@File : 1.多LLM链选择示例.py
"""
import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

dotenv.load_dotenv()
# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")

# 2.创建LLM大语言模型
# 月之暗面：model="kimi-k2-instruct"
kimi = ChatOpenAI(
    model="kimi-k2-instruct",
    api_key=os.environ.get("QIANFAN_API_KEY"),
    base_url=os.environ.get("QIANFAN_BASE_URL"),
)

# 文心一言：
wenxin = ChatOpenAI(
    model="ernie-4.5-0.3b",
    api_key=os.environ.get("QIANFAN_API_KEY"),
    base_url=os.environ.get("QIANFAN_BASE_URL"),
)

llm = ChatOpenAI(
    model="deepseek-chat",
).configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="deepseek-chat",
    wenxin=wenxin,
    kimi=kimi,
)

# 3.构建链调用
chain = prompt | llm | StrOutputParser()

# 4.调用链并传递配置信息，并切换到deepseek或者月之暗面大模型
content = chain.invoke(
    {"query": "你好，你是什么模型呢？"},
    config={"configurable": {"llm": "wenxin"}}
)
print(content)
