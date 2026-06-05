#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/14 11:13
@Author : 751363075@qq.com
@File : 1.实体记忆组件示例.py
"""
import os
import dotenv
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

llm = ChatOpenAI(
    base_url=os.getenv("QIANFAN_BASE_URL"),
    api_key=os.getenv("QIANFAN_API_KEY"),
    model="deepseek-v3.1-think-250821",
    temperature=0,
)

chain = ConversationChain(
    llm=llm,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm),
)

print(chain.invoke({"input": "你好，我是莫小可，我最近正在学习langchain。"}))
print(chain.invoke({"input": "我最喜欢的编程语言是python。"}))
print(chain.invoke({"input": "我住在广州。"}))

# 查询实体中的对话
res = chain.memory.entity_store.store
print(res)
