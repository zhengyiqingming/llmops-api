#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/12 10:38
@Author : 751363075@qq.com
@File : 2.文件对话消息历史组件实现记忆.py
"""
import os

import dotenv
from openai import OpenAI
from langchain_community.chat_message_histories import FileChatMessageHistory

dotenv.load_dotenv()

# 1.创建客户端&记忆
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url=os.environ.get('DEEPSEEK_BASE_URL'))
chat_history = FileChatMessageHistory("./memory.txt")

# 2.创建一个死循环用于人机对话
while True:
    # 3.获取人类的输入
    query = input('Human: ')

    # 4.判断下输入是否为q，如果是则退出
    if query == 'q':
        break

    # 5.发起聊天对话
    print("AI:", flush=True, end="")
    system_prompt = (
        "你是DeepSeek开发的Chat聊天机器人，可以根据相应的上下文回复用户信息，上下文存放的是人类与你对话的信息列表。\n\n"
        f"<context>{chat_history}</context>\n\n"
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {'role': "system", 'content': system_prompt},
            {'role': "user", 'content': query},
        ],
        stream=True,
    )
    ai_content = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is None:
            break
        ai_content += content
        print(content, flush=True, end='')
    chat_history.add_user_message(query)
    chat_history.add_ai_message(ai_content)
    print("")
