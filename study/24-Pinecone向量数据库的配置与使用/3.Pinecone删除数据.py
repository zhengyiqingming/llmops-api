#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/21 15:00
@Author : 751363075@qq.com
@File : 3.Pinecone删除数据.py
"""
import os

import dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

dotenv.load_dotenv()

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
    model="qwen3-embedding-8b",
    check_embedding_ctx_length=False
)
db = PineconeVectorStore(index_name="llmops", embedding=embeddings, namespace="dataset")

id = "5b8ed381-5f15-4e91-b067-49de798f8ba3"
db.delete([id], namespace="dataset")
# pinecone_index = db.get_pinecone_index("llmops")
# pinecone_index.update(id="xxx", values=[], set_metadata={}, namespace="dataset")
