#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/31 12:01
@Author : 751363075@qq.com
@File : 3.Model流式输出.py
"""
from datetime import datetime

import dotenv
from langchain_core.prompts import ChatPromptTemplate

from langchain_deepseek import ChatDeepSeek

dotenv.load_dotenv()

# 1.编排prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是openAI开发的聊天机器人，请回答用户的问题，现在的时间是{now}"),
    ("human", "{query}"),
]).partial(now=datetime.now())

# 2.创建大语言模型
llm = ChatDeepSeek(model="deepseek-chat")

response = llm.stream(prompt.invoke({"query": "你能简单介绍下LLM和LLMops吗？"}))
for chunk in response:
    print(chunk.content, flush=True, end="")
