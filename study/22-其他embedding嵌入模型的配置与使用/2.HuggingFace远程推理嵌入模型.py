#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/20 17:11
@Author : 751363075@qq.com
@File : 2.HuggingFace远程推理嵌入模型.py
"""
import dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings

dotenv.load_dotenv()

embeddings = HuggingFaceEndpointEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

query_vector = embeddings.embed_query("你好，我是莫小可，我喜欢踢足球和游泳")

print(query_vector)
print(len(query_vector))
