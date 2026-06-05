#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/3 16:49
@Author : 751363075@qq.com
@File : 1.向量数据库检索与Runnable使用技巧.py
"""
import os

import dotenv
import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from langchain_core.runnables import ConfigurableField

dotenv.load_dotenv()

# 1.构建向量数据库
db = WeaviateVectorStore(
    client=weaviate.connect_to_wcs(
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

# 2.转换检索器
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 10, "score_threshold": 0.5}
).configurable_fields(
    search_type=ConfigurableField(id="db_search_type"),
    search_kwargs=ConfigurableField(id="db_search_kwargs"),
)

# 3.修改运行时配置执行MMR搜索，并返回4条数据
mmr_documents = retriever.with_config(
    configurable={
        "db_search_type": "mmr",
        "db_search_kwargs": {
            "k": 4,
        }
    }
).invoke("关于应用配置的接口有哪些？")
print("相似性搜索:", mmr_documents)
print("内容长度：", len(mmr_documents))

print(mmr_documents[0].page_content[:20])
print(mmr_documents[1].page_content[:20])
