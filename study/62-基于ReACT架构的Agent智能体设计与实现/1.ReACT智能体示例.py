#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/6 9:59
@Author : 751363075@qq.com
@File : 1.ReACT智能体示例.py
"""
import dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_community.tools import GoogleSerperRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import render_text_description_and_args
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


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
tools = [google_serper]

# 2.定义智能体提示模板
# prompt = ChatPromptTemplate.from_template("")
prompt = hub.pull("hwchase17/react")

# 3.创建大语言模型与智能体
llm = ChatOpenAI(model="deepseek-chat", temperature=0)
agent = create_react_agent(
    llm=llm,
    prompt=prompt,
    tools=tools,
    tools_renderer=render_text_description_and_args,
)

# 4.创建智能体执行者 verbose=True表示打印结果
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# 5.执行智能体并检索
print(agent_executor.invoke({"input": "你好，你是？"}))
