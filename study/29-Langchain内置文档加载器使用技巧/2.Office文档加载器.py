#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/28 10:10
@Author : 751363075@qq.com
@File : 2.Office文档加载器.py
"""
from langchain_community.document_loaders import (
    UnstructuredExcelLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader
)

# excelLoader = UnstructuredExcelLoader("./供应中心战场用户.xlsx", mode="elements")
# excel_documents = excelLoader.load()

# word_documents = UnstructuredWordDocumentLoader("./学习AI笔记.docx")
# documents = word_documents.load()

ppt_loader = UnstructuredPowerPointLoader("./25年数字化使能部运营总结与26年规划.pptx")
documents = ppt_loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
