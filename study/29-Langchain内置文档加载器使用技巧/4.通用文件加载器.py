#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/28 11:29
@Author : 751363075@qq.com
@File : 4.通用文件加载器.py
"""
from langchain_community.document_loaders import UnstructuredFileLoader

loader = UnstructuredFileLoader("./LLMOps API接口文档.md")
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
