#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/20 11:30
@Author : 751363075@qq.com
@File : 1.Hugging Face本地嵌入模型.py
"""
from langchain_huggingface import HuggingFaceEmbeddings

# 将模型下载到本地文件夹embeddings中
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="./embeddings/"
)

query_vector = embeddings.embed_query("你好，我是莫小可，我喜欢踢足球和游泳")

print(query_vector)
print(len(query_vector))
