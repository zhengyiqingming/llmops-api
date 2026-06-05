#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/28 11:16
@Author : 751363075@qq.com
@File : 3.URL网页加载器.py
"""
from langchain_community.document_loaders import WebBaseLoader

url_loader = WebBaseLoader("https://imooc.com/")
documents = url_loader.load()

print(documents)
print(len(documents))
print(documents[0].page_content)
