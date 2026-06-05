#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/12 9:23
@Author : 751363075@qq.com
@File : 1.对话消息历史组件基础.py
"""
from langchain_core.chat_history import InMemoryChatMessageHistory, BaseChatMessageHistory

chat_history = InMemoryChatMessageHistory()

chat_history.add_user_message("你好，我是慕小课，你是谁？")
chat_history.add_ai_message("你好，我是chatgpt,有什么可以帮到你的？")

print(chat_history.messages)
