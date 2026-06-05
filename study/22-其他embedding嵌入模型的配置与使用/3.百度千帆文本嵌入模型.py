#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/20 17:21
@Author : 751363075@qq.com
@File : 3.百度千帆文本嵌入模型.py
"""
import os

import dotenv
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
    model="qwen3-embedding-8b",
    check_embedding_ctx_length=False
)

query_vector = embeddings.embed_query("我叫莫小可，我喜欢踢足球游泳")

print(query_vector)
print(len(query_vector))
