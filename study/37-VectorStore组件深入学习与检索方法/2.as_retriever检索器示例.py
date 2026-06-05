#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/3 15:33
@Author : 751363075@qq.com
@File : 2.as_retriever检索器示例.py
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
loader = UnstructuredMarkdownLoader("./LLMOps API接口文档.md")
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
        cluster_url="https://zmz2dlxsosx4tqcp5mm5g.c0.asia-southeast1.gcp.weaviate.cloud",
        auth_credentials=AuthApiKey(
            "elYrT2hQKzFrekw3N1hMbl9va0pCM1VKZWVNRCtSMCtSSUMvMFNyaVhXQktpMzJva0FQcDlvVCtPY2NBPV92MjAw"),
    ),
    index_name="LLMOps",
    text_key="text",
    embedding=OpenAIEmbeddings(
        api_key=os.getenv("QIANFAN_API_KEY"),
        base_url=os.getenv("QIANFAN_BASE_URL"),
        model="qwen3-embedding-8b",
        check_embedding_ctx_length=False
    )
)
db.add_documents(chunks)

# 4.转换检索器（带阈值的相似性搜索，数据为10条，得分阈值为0.5）
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 10, "score_threshold": 0.5},
)

# 5.检索结果
documents = retriever.invoke("能介绍下什么是LLMOps么？")

# 提取从开头到第50个元素（不包含第50个元素）的所有内容。
print(list(document.page_content[:50] for document in documents))
print(len(documents))
