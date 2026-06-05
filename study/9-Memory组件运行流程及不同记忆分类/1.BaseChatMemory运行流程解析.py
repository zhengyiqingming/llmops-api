#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/12 11:20
@Author : 751363075@qq.com
@File : 1.BaseChatMemory运行流程解析.py
"""
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory import ConversationBufferMemory

memory = BaseChatMemory(
    input_key="query",
    output_key="output",
    return_messages=True,
    # chat_history假设

)

memory.load
