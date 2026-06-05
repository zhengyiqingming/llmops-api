#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/13 11:41
@Author : 751363075@qq.com
@File : 1.RAPTOR递归文档树优化策略.py
"""
import os

import dotenv
import weaviate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()

# 1.定义随机数种子、文本嵌入模型、大语言模型、向量数据库
RANDOM_SEED = 224
embd = HuggingFaceEmbeddings(
    model_name="thenlper/gte-small",
    cache_folder="./embeddings/",
    encode_kwargs={"normalize_embeddings": True},
)

model = ChatOpenAI(model="deepseek-chat", temperature=0)
db = WeaviateVectorStore(
    client=weaviate.connect_to_wcs(
        cluster_url="https://8th0hosnrngestnzlqjwg.c0.asia-southeast1.gcp.weaviate.cloud",
        auth_credentials=AuthApiKey(
            "dm9DemVWaEhPaFo3VUloZl9GUDhkQUZqK2ZpRmU3QmYxMWZBcnB6dm1Cc3RjK1Y0QmN0cTFUVWRZem5vPV92MjAw"),
    ),
    index_name="RaptorRAG",
    text_key="text",
    embedding=embd
)
