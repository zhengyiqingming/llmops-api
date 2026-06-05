#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/9 11:32
@Author : 751363075@qq.com
@File : 1.混合策略实现doc-doc对称检索.py
"""
import os
from typing import List

import dotenv
import weaviate
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()


class HyDERetriever(BaseRetriever):
    """HyDE混合策略检索器"""
    retriever: BaseRetriever
    llm: BaseLanguageModel

    def _get_relevant_documents(
            self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """传递检索query实现HyDE混合策略检索"""
        # 1.构建生成假设性文档的prompt
        prompt = ChatPromptTemplate.from_template(
            "请写一篇科学论文来回答这个问题。\n"
            "问题：{question}\n"
            "文章："
        )

        # 2.构建HyDE混合策略检索链
        chain = (
                {"question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
                | self.retriever
        )

        return chain.invoke(query)


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

# 2.创建HyDE检索器
hyde_retriever = HyDERetriever(
    retriever=retriever,
    llm=ChatOpenAI(model="deepseek-chat", temperature=0),
)

# 3.检索文档
documents = hyde_retriever.invoke("关于LLMOps应用配置的文档有哪些？")
print(documents)
print(len(documents))
