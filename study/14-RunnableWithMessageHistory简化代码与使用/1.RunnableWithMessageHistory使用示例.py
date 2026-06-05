#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/14 17:48
@Author : 751363075@qq.com
@File : 1.RunnableWithMessageHistory使用示例.py
"""
import dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

dotenv.load_dotenv()

# 1.定义历史记忆存储
store = {}


# 2.工厂函数，用于获取指定会话的聊天历史
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = FileChatMessageHistory(f"./chat_history_{session_id}.txt")
    return store[session_id]


# 3.创建提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个强大的聊天机器人，请根据用户的需求回复问题。"),
    MessagesPlaceholder("history"),
    ("human", "{query}")
])

# 4.创建大语言模型
llm = ChatOpenAI(model="deepseek-reasoner")

# 5.构建链
chain = prompt | llm | StrOutputParser()

# 6.包装链
with_message_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="history",
)

# 7.死循环构建对话命令行
while True:
    # 8.获取用户输入：
    query = input("Human: ")

    if query == "q":
        exit(0)

    # 9.运行链并传递配置信息
    response = with_message_chain.stream(
        {"query": query},
        config={"configurable": {"session_id": "moxiaoke"}}
    )
    print("AI:", flush=True, end="")
    for chunk in response:
        print(chunk, flush=True, end="")
    print("")
