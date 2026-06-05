#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/30 11:03
@Author : 751363075@qq.com
@File : 1.语义文档分割器使用示例.py
"""
import os

import dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

# 1.构建加载器和文本分割器
loader = UnstructuredMarkdownLoader("./科幻短篇.txt")

text_splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(
        api_key=os.getenv("QIANFAN_API_KEY"),
        base_url=os.getenv("QIANFAN_BASE_URL"),
        model="qwen3-embedding-8b",
        check_embedding_ctx_length=False
    ),
    number_of_chunks=10,
    add_start_index=True,
    sentence_split_regex=r"(?<=[。？！.?!])",
)

# 2.加载文本与分割
documents = loader.load()
chunks = text_splitter.split_documents(documents)

# 3.循环打印
for chunk in chunks:
    print(f"块大小：{len(chunk.page_content)},元数据：{chunk.metadata}")
