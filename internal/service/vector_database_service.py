#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/26 11:53
@Author : 751363075@qq.com
@File : vector_database_service.py
"""
import os
from dataclasses import dataclass

from flask_weaviate import FlaskWeaviate
from injector import inject
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
from weaviate.collections import Collection

from .embeddings_service import EmbeddingsService

# 向量数据库的集合名字
COLLECTION_NAME = "Dataset"


@inject
@dataclass
class VectorDataBaseService:
    """向量数据库服务"""
    weaviate: FlaskWeaviate  # 通过注入的方法获取Weaviate向量数据库，有利于自动关闭连接
    embeddings_service: EmbeddingsService

    @property
    def vector_store(self) -> WeaviateVectorStore:
        return WeaviateVectorStore(
            client=self.weaviate.client,
            index_name=COLLECTION_NAME,  # 向量数据库的集合名字
            text_key="text",  # 表示向量数据库中，文档内容存入哪一个metadata中
            embedding=self.embeddings_service.cache_backed_embeddings
        )

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()

    @property
    def collection(self) -> Collection:
        return self.weaviate.client.collections.get(COLLECTION_NAME)
