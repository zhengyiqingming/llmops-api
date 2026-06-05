#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/14 17:35
@Author : 751363075@qq.com
@File : 3.对话链.py
"""
import dotenv
from langchain.chains.conversation.base import ConversationChain
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

llm = ChatOpenAI(model="deepseek-reasoner")
chain = ConversationChain(llm=llm)

content = chain.invoke({"input": "你好，我是莫小可，我喜欢足球，你是谁？你喜欢什么？"})
print(content)

content = chain.invoke({"input": "请问我的爱好是什么"})
print(content)
