#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/26 16:57
@Author : 751363075@qq.com
@File : 1.GPT模型绑定函数.py
"""
import json

import dotenv
import os
from typing import Any, Type

import requests
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class GaodeWeatherArgsSchema(BaseModel):
    city: str = Field(description="需要查询天气预报的目标城市，例如：广州")


class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


class GaodeWeatherTool(BaseTool):
    """根据传入的城市名查询天气"""
    name = "gaode_weather"
    description = "当你想查询天气或者与天气相关的问题时可以使用的工具"
    args_schema: Type[BaseModel] = GaodeWeatherArgsSchema

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """根据传入的城市名称运行调用api获取城市对应的天气预报信息"""
        try:
            # 1.获取高德API秘钥，如果没有创建的话，则抛出错误
            gaode_api_key = os.getenv("GAODE_API_KEY")
            if not gaode_api_key:
                return f"高德开放平台API未配置"
            # 2.从参数中获取city城市名字
            city = kwargs.get("city", "")
            api_domain = "https://restapi.amap.com/v3"
            session = requests.session()

            # 3.发起城市区域编码查询，根据city获取ad_code
            city_response = session.request(
                method="GET",
                url=f"{api_domain}/config/district?key={gaode_api_key}&keywords={city}&subdistrict=0",
                headers={"Content-Type": "application/json;charset=UTF-8"},
            )
            city_response.raise_for_status()
            city_data = city_response.json()
            if city_data.get("info") == "OK":
                adcode = city_data["districts"][0]["adcode"]
                # 4.根据得到的ad_code调用天气预报api接口，获取天气信息
                weather_response = session.request(
                    method="GET",
                    url=f"{api_domain}/weather/weatherInfo?key={gaode_api_key}&city={adcode}&extensions=all",
                    headers={"Content-Type": "application/json;charset=UTF-8"},
                )
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                if weather_data.get("info") == "OK":
                    # 5.返回最后的结果字符串
                    return json.dumps(weather_data)
            return f"获取{city}天气预报信息失败"
        except Exception as e:
            return f"获取{kwargs.get('city', '')}天气预报信息失败"


gaode_weather = GaodeWeatherTool()
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
tool_dict = {
    gaode_weather.name: gaode_weather,
    google_serper.name: google_serper,
}

tools = [tool for tool in tool_dict.values()]

# 2.创建Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是由OpenAI开发的聊天机器人，可以帮助用户回答问题，必要时刻请调用工具帮助用户解答"),
    ("human", "{query}"),
])

# 3.创建大语言模型并绑定工具,llm会自动选择工具（默认值是auto）
llm = ChatOpenAI(model="deepseek-chat", temperature=0)
llm_with_tools = llm.bind_tools(tools=tools)

# 4.创建链应用
chain = {"query": RunnablePassthrough()} | prompt | llm_with_tools
query = "东莞最近的天气如何，需要穿什么样的衣服？"
resp = chain.invoke(query)
tool_calls = resp.tool_calls

# 6.判断是工具调用还是正常输出结果
if len(tool_calls) <= 0:
    print("生成内容：", resp.content)
else:
    # 7.将历史的系统消息、人类消息、AI消息组合
    messages = prompt.invoke(query).to_messages()
    messages.append(resp)

    # 8.循环遍历所有工具调用信息
    for tool_call in tool_calls:
        tool = tool_dict.get(tool_call.get("name"))  # 获取需要执行的工具
        print("正在执行的工具：", tool.name)
        content = tool.invoke(tool_call.get("args"))  # 工具执行的结果
        print("工具返回结果：", content)
        tool_call_id = tool_call.get("id")
        messages.append(ToolMessage(
            content=content,
            tool_call_id=tool_call_id,
        ))
    print("输出内容：", llm.invoke(messages).content)
