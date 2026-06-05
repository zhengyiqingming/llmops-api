#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/30 17:28
@Author : 751363075@qq.com
@File : 1.自定义分割器示例.py
"""
import jieba.analyse
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import TextSplitter


class CustomTextSplitter(TextSplitter):
    """自定义文本分割器"""

    def __init__(self, separator: str, top_k: int = 10, **kwargs):
        """构造函数，传递分割器还有需要提取的关键词数，默认为10"""
        super().__init__(**kwargs)
        self._separator = separator
        self.top_k = top_k

    def split_text(self, text: str) -> list[str]:
        """传递对应的文本执行分割并提取分割数据的关键词，组成文档列表返回"""
        # 1.根据传递的分隔符分割传入的文本
        split_texts = text.split(self._separator)
        # 2.提取分割出来的每一段文本的关键词，数量为self._top_k个
        text_keywords = []
        for split_text in split_texts:
            text_keywords.append(jieba.analyse.extract_tags(split_text, self.top_k))
        # 3.将关键词使用逗号进行拼接，组成字符串列表并返回
        return [",".join(keywords) for keywords in text_keywords]


# 1.创建加载器与分割器
loader = UnstructuredFileLoader("./科幻短篇.txt")
# 每个分割文本提取关键词不超过10个，文本直接用\n\n分割
text_splitter = CustomTextSplitter("\n\n", 10)

# 2.加载文档并分割
documents = loader.load()
chunks = text_splitter.split_documents(documents)

# 3.循环遍历文档信息
for chunk in chunks:
    print(chunk.page_content)
    print("====================")
