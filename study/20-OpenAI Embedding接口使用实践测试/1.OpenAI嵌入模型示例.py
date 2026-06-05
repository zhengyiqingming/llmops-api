#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/20 9:20
@Author : 751363075@qq.com
@File : 1.OpenAI嵌入模型示例.py
"""
import os
import numpy as np
from numpy.linalg import norm

import dotenv
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()


def cosin_similarity(vec1: list, vec2: list) -> float:
    """计算传入的两个向量的余弦相似度"""
    # 1.计算2个向量的点积
    doc_product = np.dot(vec1, vec2)

    # 2.计算向量的长度:norm函数就是inputs的一共N维的话对这N个数据求p范数,默认p=2，||x||_{p} = \sqrt[p]{x_{1}^{p} + x_{2}^{p} + \ldots + x_{N}^{p}}
    vec1_norm = norm(vec1)
    vec2_norm = norm(vec2)

    # 3.计算余弦相似度
    return doc_product / (vec1_norm * vec2_norm)


# 1.创建文本嵌入模型
openai_embeddings = OpenAIEmbeddings(
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
    model="embedding-v1",
    check_embedding_ctx_length=False
)

# 2.嵌入文本
query_vector = openai_embeddings.embed_query("你好，我是莫小可")

print(query_vector)
print(len(query_vector))
print("======================================")

# 3.嵌入文档列表/字符串列表
docments_vector = openai_embeddings.embed_documents(
    [
        "我叫莫小可，我喜欢踢足球",
        "这个踢足球的人叫莫小可",
        "求知若渴，虚心若愚"
    ]
)
# print(docments_vector)
print(len(docments_vector))

# 4.计算余弦相似度
print("向量1和向量2的相似度：", cosin_similarity(docments_vector[0], docments_vector[1]))
print("向量1和向量3的相似度：", cosin_similarity(docments_vector[0], docments_vector[2]))
