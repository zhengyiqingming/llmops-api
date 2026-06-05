#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/4 16:37
@Author : 751363075@qq.com
@File : 1.RAG多查询结果融合策略.py
"""
import os
from typing import List

import dotenv
import weaviate
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from langchain.load import dumps, loads
from langchain.retrievers import MultiQueryRetriever

dotenv.load_dotenv()


class RAGFusionRetriever(MultiQueryRetriever):
    """RAG多查询结果融合策略检索器"""
    k: int = 4

    # 重写检索文档策略，使其返回一个嵌入式的文档列表：List[List]
    def retrieve_documents(
            self, queries: List[str], run_manager: CallbackManagerForRetrieverRun
    ) -> List[List]:
        """重写检索文档函数，返回值变成一个嵌套列表"""
        documents = []
        for query in queries:
            docs = self.retriever.invoke(
                query, config={"callbacks": run_manager.get_child()}
            )
            documents.append(docs)
        return documents

    # 重写合并文档的方法，传入值改为嵌入式的文档列表：List[List]
    def unique_union(self, documents: List[List]) -> List[Document]:
        """使用rrf算法来去重合并对应的文档，参数为嵌套列表，返回值为文档列表"""
        # 1.定义一个变量，存储每个文档的得分信息
        fused_result = {}

        # 2.循环两层获取每一个文档信息
        for docs in documents:
            for rank, doc in enumerate(docs):
                # 3.使用dumps函数将类转换成字符串
                doc_str = dumps(doc)
                # 4.判断该文档是否已经计算过得分
                if doc_str not in fused_result:
                    fused_result[doc_str] = 0
                # 5.计算新得分
                fused_result[doc_str] += 1 / (rank + 60)
        # 6.执行排序操作，获取相应的数据，使用的是降序
        reranked_results = [
            # loads函数将doc字符串加载为一个Document类
            (loads(doc), score)
            for doc, score in sorted(fused_result.items(), key=lambda x: x[1], reverse=True)
        ]

        return [item[0] for item in reranked_results[:self.k]]


# 1.构建向量数据库与检索器
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
retriever = db.as_retriever(search_type="mmr")

rag_fusion_retriever = RAGFusionRetriever.from_llm(
    retriever=retriever,
    llm=ChatOpenAI(model="deepseek-chat", temperature=0)
)

# 3.执行检索
docs = rag_fusion_retriever.invoke("关于LLMOps应用配置的文档有哪些")
print(docs)
print(len(docs))
