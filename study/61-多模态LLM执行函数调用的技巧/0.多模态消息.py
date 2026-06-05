#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/5 16:56
@Author : 751363075@qq.com
@File : 0.多模态消息.py
"""
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("human", [
        {"type": "text", "text": "{query}"},
        {"type": "image_url", "image_url": {"url": "{image_url}"}}
    ])
])

print(prompt.invoke({
    "query": "这张图片所在的地址的天气怎么样",
    "image_url": "https://img1.baidu.com/it/u=644490943,1781886584&fm=253&fmt=auto&app=138&f=JPEG"
}).to_messages())
