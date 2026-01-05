#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/4 11:49
@Author : 751363075@qq.com
@File : 2.RunnableParallel模拟检索.py
"""
import dotenv
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

dotenv.load_dotenv()


def retrieval(query: str) -> str:
    """一个模拟的检索器函数"""
    print("正在检索：", query)
    return "我是莫小可"


# 1.编排prompt
prompt = ChatPromptTemplate.from_template("""请根据用户的问题回答，可以参考对应的上下文进行生成

<context>
{context}
</context>

用户的提问是：{query}""")

# 2.构建大语言模型
llm = ChatDeepSeek(model="deepseek-chat")

# 3.构建输出解析器
parser = StrOutputParser()

# 4.构建链
chain = {
            "context": lambda x: retrieval(x["query"]),
            "query": itemgetter("query"),
        } | prompt | llm | parser

# 5.调用链
content = chain.invoke({"query": "你好，我是谁？"})
print(content)
