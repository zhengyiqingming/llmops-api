# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/5 15:31
@Author : 751363075@qq.com
@File : 1.问题分解策略.py
"""
from operator import itemgetter
import os

import dotenv
import weaviate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()


def fomate_qa_pair(question: str, answer: str) -> str:
    """格式化传递的问题+答案为单个字符串"""
    return f"Question:{question}\nAnswer:{answer}\n\n".strip()


# 1.定义分解子问题的prompt
decomposition_prompt = ChatPromptTemplate.from_template(
    "你是一个乐于助人的AI助理，可以针对一个输入问题生成多个相关的子问题。\n"
    "目标是将输入问题分解成一组可以独立回答的子问题或者子任务。\n"
    "生成与以下问题相关的多个搜索查询：{question}\n"
    "并使用换行符进行分割，输出（3个子问题/子查询）："
)

# 2.构建分解问题链
decomposition_chain = (
        {"question": RunnablePassthrough()}
        | decomposition_prompt
        | ChatOpenAI(model="deepseek-chat", temperature=0)
        | StrOutputParser()
        | (lambda x: x.strip().split("\n"))
)

# 3.构建向量数据库与检索器
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

# 4.执行提问获取子问题
question = "关于LLMOPs应用配置的文档有哪些"
sub_questions = decomposition_chain.invoke(question)

# 5.构件迭代问答链：提示模板+链
prompt = ChatPromptTemplate.from_template("""这是你需要回答的问题：
---
{question}
---

这是所有可用的背景问题和答案对：
---
{qa_pairs}
---

这是与问题相关的额外背景信息：
---
{context}
---""")
chain = (
        {
            "question": itemgetter("question"),
            "qa_pairs": itemgetter("qa_pairs"),
            "context": itemgetter("question") | retriever
        }
        | prompt
        | ChatOpenAI(model="deepseek-chat", temperature=0)
        | StrOutputParser()
)

# 5.循环遍历所有子问题进行检索并获取答案
qa_pairs = ""
for sub_question in sub_questions:
    answer = chain.invoke({"question": sub_question, "qa_pairs": qa_pairs})
    qa_pair = fomate_qa_pair(sub_question, answer)
    qa_pairs += "\n----\n" + qa_pair
    print(f"问题：{sub_question}")
    print(f"答案：{answer}")
