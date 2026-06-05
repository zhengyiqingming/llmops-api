#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/9 17:04
@Author : 751363075@qq.com
@File : 1.函数回调规范化输出.py
"""
from typing import Literal

import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field

dotenv.load_dotenv()


class RouteQuery(BaseModel):
    """将用户查询映射到对应的数据源上"""
    datasource: Literal["python_docs", "js_docs", "golang_docs"] = Field(
        description="根据用户的问题，选择哪个数据源最相关以回答用户的问题"
    )


# 1/创建绑定结构化输出的大语言模型
llm = ChatOpenAI(model="deepseek-chat", temperature=0)
structured_llm = llm.with_structured_output(RouteQuery)

# 2.构建一个问题
question = """为什么下面的代码不工作了，请帮我检查下：

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(["human", "speak in {language}"])
prompt.invoke("中文")"""
res: RouteQuery = structured_llm.invoke(question)

print(res)
print(type(res))
print(res.datasource)
