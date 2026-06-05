#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/29 11:49
@Author : 751363075@qq.com
@File : 3.分割中文场景示例.py
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1.创建加载器和文本分割器
loader = UnstructuredMarkdownLoader("./LLMOps API接口文档.md")
# 同时考虑中英文场景
separators = [
    "\n\n",
    "\n",
    "。|！|？",
    "\.\s|\!\s|\?\s",  # 英文文档标点符号后面通常加空格
    "；|;\s",
    "，|,\s",
    " ",
    ""
]

text_splitter = RecursiveCharacterTextSplitter(
    separators=separators,
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

# 2.加载文档与分割
documents = loader.load()
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"块大小：{len(chunk.page_content)}，元数据：{chunk.metadata}")

print(chunks[2].page_content)
