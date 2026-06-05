#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/28 9:45
@Author : 751363075@qq.com
@File : 1.Markdown文档加载器.py
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("./LLMOps API接口文档.md")
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
