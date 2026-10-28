#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/20 18:06
@Author : 751363075@qq.com
@File : 1.faiss向量数据库使用示例.py
"""
import os

import dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
    model="qwen3-embedding-8b",
    check_embedding_ctx_length=False
)
texts: list = [
    "笨笨是一只很喜欢睡觉的猫咪",
    "我喜欢在夜晚听音乐，这让我感到放松。",
    "猫咪在窗台上打盹，看起来非常可爱。",
    "学习新技能是每个人都应该追求的目标。",
    "我最喜欢的食物是意大利面，尤其是番茄酱的那种。",
    "昨晚我做了一个奇怪的梦，梦见自己在太空飞行。",
    "我的手机突然关机了，让我有些焦虑。",
    "阅读是我每天都会做的事情，我觉得很充实。",
    "他们一起计划了一次周末的野餐，希望天气能好。",
    "我的狗喜欢追逐球，看起来非常开心。",
]
metadatas: list = [
    {"page": 1},
    {"page": 2},
    {"page": 3},
    {"page": 4},
    {"page": 5},
    {"page": 6},
    {"page": 7},
    {"page": 8},
    {"page": 9},
    {"page": 10},
]
db = FAISS.from_texts(
    texts,
    embeddings,
    metadatas,
    relevance_score_fn=lambda distance: 1.0 / (1.0 + distance),
)

ids = db.add_texts(["笨笨是一只已经七岁的猫了"])

print(ids)
print(db.index.ntotal)
print(db.index_to_docstore_id)
print(db.similarity_search_with_relevance_scores(
    "我养了一只猫，叫笨笨",
    filter={"page": 5})
)
print("删除前数量：", db.index.ntotal)
# 获取向量数据库的索引id列表信息
db.delete([db.index_to_docstore_id[0]])
print("删除后数量：", db.index.ntotal)
db.save_local("./vector-store/")

# 加载本地数据到向量数据库
db = FAISS.load_local("./vector-store", embeddings, allow_dangerous_deserialization=True)

print(db.similarity_search_with_score("我养了一只猫，叫笨笨"))
