#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/28 11:16
@Author : 751363075@qq.com
@File : 1.LLM结构化输出.py
"""
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

dotenv.load_dotenv()


class QAExtra(BaseModel):
    """这是一个问答键值对工具，传递对应的假设性问题和答案"""
    question: str = Field(description="假设性问题")
    answer: str = Field(description="假设性问题对应的答案")


llm = ChatOpenAI(model="deepseek-chat")
structured_llm = llm.with_structured_output(QAExtra, method="json_mode")

prompt = ChatPromptTemplate.from_messages([
    ("system", "请从用户传递的query中提取出假设性问题和答案,响应格式为json，并携带`question`和`answer`两个字段"),
    ("human", "{query}")
])

chain = {"query": RunnablePassthrough()} | prompt | structured_llm

print(chain.invoke("我叫莫小可，我喜欢踢足球、游泳"))
