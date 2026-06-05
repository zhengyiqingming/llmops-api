#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/14 11:08
@Author : 751363075@qq.com
@File : 3.flashrank重排序示例.py
"""
import os

import dotenv
import weaviate
from langchain_community.document_compressors import FlashrankRerank
from langchain_openai import OpenAIEmbeddings
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
        cluster_url="https://zmz2dlxsosx4tqcp5mm5g.c0.asia-southeast1.gcp.weaviate.cloud",
        auth_credentials=AuthApiKey(
            "elYrT2hQKzFrekw3N1hMbl9va0pCM1VKZWVNRCtSMCtSSUMvMFNyaVhXQktpMzJva0FQcDlvVCtPY2NBPV92MjAw"),
        skip_init_checks=True
    ),
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding,
)
rerank = FlashrankRerank()

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
