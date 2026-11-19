#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/4/14 11:21
@Author : 751363075@qq.com
@File : embeddings_service.py
"""
import os

from injector import inject
from dataclasses import dataclass

from langchain_community.storage import RedisStore
from langchain_core.embeddings import Embeddings
from langchain.embeddings import CacheBackedEmbeddings
from redis import Redis
from langchain_openai import OpenAIEmbeddings
import tiktoken


@inject
@dataclass
class EmbeddingsService:
    """文本嵌入模型服务"""
    _store: RedisStore
    _embeddings: Embeddings
    # 缓存客户端
    _cache_backed_embeddings: CacheBackedEmbeddings

    def __init__(self, redis: Redis):
        """构造函数，初始化文本嵌入模型客户端、存储器、缓存客户端"""
        self._store = RedisStore(client=redis)
        # self._embeddings = HuggingFaceEmbeddings(
        #     model_name="Alibaba-NLP/gte-multilingual-base",
        #     cache_folder=os.path.join(os.getcwd(), "internal", "core", "embeddings"),
        #     model_kwargs={
        #         "trust_remote_code": True,
        #     },
        # )
        self._embeddings = OpenAIEmbeddings(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model="text-embedding-v3",  # 阿里云目前主流且好用的向量化模型
            check_embedding_ctx_length=False
        )
        # self._embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self._cache_backed_embeddings = CacheBackedEmbeddings.from_bytes_store(
            self._embeddings,
            self._store,
            namespace="embeddings",
        )

    @classmethod
    def caculate_token_count(cls, query: str) -> int:
        """计算传入文本的token数"""
        encoding = tiktoken.encoding_for_model("gpt-3.5")
        return len(encoding.encode(query))

    @property
    def store(self) -> RedisStore:
        return self._store

    @property
    def embeddings(self) -> Embeddings:
        return self._embeddings

    @property
    def cache_backed_embeddings(self) -> CacheBackedEmbeddings:
        return self._cache_backed_embeddings
