#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/3 16:24
@Author : 751363075@qq.com
@File : 3.最大边际相关性示例.py
"""
import os

import dotenv
import weaviate
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()
# 1.构建加载器与分割器
loader = UnstructuredMarkdownLoader("./项目API文档.md")
# 同时考虑中英文场景
separators = [
    "\n\n",
    "\n",
    "。|！|？",
    "\.\s|\!\s|\?\s",  # 英文文档标点符号后面通常加空格
    "；|;\s",
    "，|,\s",
    " ",
    ""
]
text_splitter = RecursiveCharacterTextSplitter(
    separators=separators,
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

# 2.加载文档并分割
documents = loader.load()
print(documents)
chunks = text_splitter.split_documents(documents)

# 3.将数据存储到向量数据库
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
# db.add_documents(chunks)

# 4.执行最大边际相关性搜素
# documents = db.similarity_search("关于配置接口的信息有哪些?")
documents = db.max_marginal_relevance_search("关于配置接口的信息有哪些?")

# 提取从开头到第50个元素（不包含第50个元素）的所有内容。
# print(list(document.page_content[:100] for document in documents))
# print(len(documents))
for document in documents:
    print(document.page_content[:100])
    print("==========================")
