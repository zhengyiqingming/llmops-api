#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/10 17:10
@Author : 751363075@qq.com
@File : 1.预构建ReACT智能体.py
"""
import dotenv
from langchain_community.tools import GoogleSerperRun
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


class DallEArgsSchema(BaseModel):
    query: str = Field(description="输入应该是生成图像的文本提示（prompt）")


# 1.定义工具与工具列表
google_serper = GoogleSerperRun(
    name="google_serper",
    description=(
        "一个低成本的谷歌搜索API。"
        "当你需要回答有关时事的问题时，可以调用该工具。"
        "该工具传递的参数是搜索查询语句。"
    ),
    args_schema=GoogleSerperArgsSchema,
    api_wrapper=GoogleSerperAPIWrapper(),
)
dalle = OpenAIDALLEImageGenerationTool(
    name="openai_dalle",
    api_wrapper=DallEAPIWrapper(model="dall-e-3"),
    args_schema=DallEArgsSchema,
)
tools = [google_serper, dalle]

# 2.创建大语言模型
model = ChatOpenAI(model="deepseek-chat", temperature=0)

# 3.使用预构建的函数创建ReACT智能体
agent = create_react_agent(model=model, tools=tools)

# 4.调用智能体并输出内容
inputs = {"messages": [("human", "请帮忙详细介绍下OpenClaw这个软件")]}

# 5.流式输出图结构内容
for chunk in agent.stream(inputs, stream_mode="updates"):
    print(chunk)
