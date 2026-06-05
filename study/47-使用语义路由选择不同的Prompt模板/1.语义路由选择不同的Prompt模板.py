#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/10 11:01
@Author : 751363075@qq.com
@File : 1.语义路由选择不同的Prompt模板.py
"""
import os

from langchain.utils.math import cosine_similarity
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

dotenv.load_dotenv()

# 1.定义两份不同的prompt模板（物理模板、数学模板）
physics_template = """你是一位非常聪明的物理教程。
你擅长以简洁易懂的方式回答物理问题。
当你不知道问题的答案时，你会坦率承认自己不知道。

这是一个问题：
{query}"""
math_template = """你是一位非常优秀的数学家。你擅长回答数学问题。
你之所以如此优秀，是因为你能将复杂的问题分解成多个小步骤。
并且回答这些小步骤，然后将它们整合在一起回来更广泛的问题。

这是一个问题：
{query}"""

# 2.创建文本嵌入模型，并执行嵌入
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
    model="qwen3-embedding-8b",
    check_embedding_ctx_length=False
)
prompt_templates = [physics_template, math_template]
# 将传入的2个prompt模板（物理模板、数学模板）转化为向量列表
prompt_embeddings = embeddings.embed_documents(prompt_templates)


def prompt_router(input) -> ChatPromptTemplate:
    """根据传入的query计算返回不同的提示模板"""
    # 1.计算传入query的嵌入向量
    query_embedding = embeddings.embed_query(input["query"])
    print(query_embedding)
    print("=========================")
    # 2.计算相似性
    similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
    print(similarity)
    print("=========================")
    print(similarity.argmax())
    most_similar = prompt_templates[similarity.argmax()]
    print("使用数学模板" if most_similar == math_template else "使用物理模板")

    # 3.构建提示模板
    return ChatPromptTemplate.from_template(most_similar)


chain = (
        {"query": RunnablePassthrough()}
        | RunnableLambda(prompt_router)
        | ChatOpenAI(model="deepseek-chat")
        | StrOutputParser()
)

print(chain.invoke("黑洞是什么？"))
print("=========================")
print(chain.invoke("圆周率最早是谁提出来的？"))
