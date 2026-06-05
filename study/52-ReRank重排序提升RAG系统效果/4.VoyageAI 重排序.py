#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/14 11:25
@Author : 751363075@qq.com
@File : 4.VoyageAI 重排序.py
"""
import os

import dotenv
import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_voyageai import VoyageAIRerank
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from langchain.retrievers import ContextualCompressionRetriever

dotenv.load_dotenv()

# 1.创建向量数据库与重排组件
embedding = OpenAIEmbeddings(
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
    model="qwen3-embedding-8b",
    check_embedding_ctx_length=False
)
db = WeaviateVectorStore(
    client=weaviate.connect_to_weaviate_cloud(
        cluster_url="https://8th0hosnrngestnzlqjwg.c0.asia-southeast1.gcp.weaviate.cloud",
        auth_credentials=AuthApiKey(
            "dm9DemVWaEhPaFo3VUloZl9GUDhkQUZqK2ZpRmU3QmYxMWZBcnB6dm1Cc3RjK1Y0QmN0cTFUVWRZem5vPV92MjAw"),
        skip_init_checks=True
    ),
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding,
)
rerank = VoyageAIRerank(
    model="rerank-lite-1",
    voyage_api_key=os.getenv("VOYAGE_API_KEY"),
    top_k=3
)

# 2.构建上下文压缩检索器
retriever = ContextualCompressionRetriever(
    base_retriever=db.as_retriever(search_type="mmr"),
    base_compressor=rerank,
)
# retriever = db.as_retriever()

# 3.执行搜索并排序
api_key = os.getenv("COHERE_API_KEY")
print(f"API 秘钥：{api_key}")
search_docs = retriever.invoke("关于LLMOps应用配置的信息有哪些呢？")
print(search_docs)
print(len(search_docs))
