#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/28 16:35
@Author : 751363075@qq.com
@File : 2.FileSystemBlobLoader示例.py
"""
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader

# 加载当前目录数据
loader = FileSystemBlobLoader(".", show_progress=True)

for blob in loader.yield_blobs():
    print(blob.as_string())
