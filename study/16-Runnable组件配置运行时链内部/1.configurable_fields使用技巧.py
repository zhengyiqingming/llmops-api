#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/15 17:57
@Author : 751363075@qq.com
@File : 1.configurable_fields使用技巧.py
"""
import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

dotenv.load_dotenv()

# 1.构建组件
prompt = ChatPromptTemplate.from_template("请生成一个小于{x}的随机整数")

# 2.创建LLM大语言模型，并配置temperature参数为可运行时配置，配置键位llm_temperature
llm = ChatOpenAI(
    model="deepseek-v3.1-250821",  # model="deepseek-v3.1-250821"
    api_key=os.getenv("QIANFAN_API_KEY"),
    base_url=os.getenv("QIANFAN_BASE_URL"),
).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="大语言模型的温度",
        description="温度越低，大语言模型生成的内容越确定，温度越高，生成的内容越随机"
    )
)

# 3.定义一个链
chain = prompt | llm | StrOutputParser()

# 4.执行链并获取结果
content = chain.invoke({"x": 1000})
print(content)

print("==============================")

# 5.将temperature修改为0调用内部
with_config_chain = chain.with_config(configurable={"llm_temperature": 0})
content = with_config_chain.invoke({"x": 1000})
# content = chain.invoke(
#     {"x": 1000},
#     config={"configurable": {"llm_temperature": 0}},
# )
print(content)
