#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/4 11:36
@Author : 751363075@qq.com
@File : 1.Multi-Query多查询策略.py
"""
import os

import dotenv
import weaviate
from langchain.retrievers import MultiQueryRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.构建向量数据库与检索器
db = WeaviateVectorStore(
    client=weaviate.connect_to_weaviate_cloud(
        cluster_url="https://3ds1l8qiqji2vxxgomgfmw.c0.asia-southeast1.gcp.weaviate.cloud",
        auth_credentials=AuthApiKey(
            "eE9yQ2FpaGV6UW04Y0Q1Ul9hL3BONXpGQW9hT1BMa1lrb3lsV2ZqZS9CZDNDRmU3WXdVcmdBMUsxbXhrPV92MjAw"),
    ),
    index_name="DatasetDemo",
    text_key="text",
    embedding=OpenAIEmbeddings(
        api_key=os.getenv("QIANFAN_API_KEY"),
        base_url=os.getenv("QIANFAN_BASE_URL"),
        model="qwen3-embedding-8b",
        check_embedding_ctx_length=False
    )
)

retriever = db.as_retriever(search_type="mmr")

# 2.创建多查询检索器
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=ChatOpenAI(
        model="deepseek-chat",
        temperature=0
    ),
    include_original=True,
    prompt=ChatPromptTemplate.from_template(
        "你是一个AI语言模型助手。你的任务是生成给定用户问题的3个不同版本，以从向量数据库中检索相关文档。"
        "通过提供用户问题的多个视角，你的目标是帮助用户克服基于距离的相似性搜索的一些限制。"
        "请用换行符分隔这些替代问题。"
        "原始问题：{question}"
    )
)

# 3.执行检索
docs = multi_query_retriever.invoke("关于LLMOps应用配置的文档有哪些")
print(docs)
print(len(docs))
