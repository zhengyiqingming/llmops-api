#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/27 10:47
@Author : 751363075@qq.com
@File : 1.不支持函数调用的模型解决示例.py
"""
import json

import dotenv
import os
from typing import Any, Type, TypedDict, Dict, Optional

import requests
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool, render_text_description_and_args
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableConfig, RunnablePassthrough

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


class ToolCallRequest(TypedDict):
    name: str
    arguments: Dict[str, Any]


# 1.定义工具列表
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


def invoke_tool(
        tool_call_request: ToolCallRequest, config: Optional[RunnableConfig] = None,
) -> str:
    """
    我们可以使用的执行工具调用的函数。

    :param tool_call_request:一个包含名称和参数的字典，名称必须与现有的工具名称匹配，参数是该工具的参数。
    :param config: 这是Langchain中包含回调、元数据等信息的配置信息。
    :return: 工具执行的结果。
    """
    name = tool_call_request["name"]
    requested_tool = tool_dict.get(name)
    return requested_tool.invoke(tool_call_request.get("arguments"), config=config)


system_prompt = """你是一个由openAI开发的聊天机器人，可以访问以下工具。
以下是每个工具的名称和描述：

{rendered_tools}

根据用户输入，返回要使用的工具的名称和输入。
将您的响应作为具有`name`和`arguments`键的JSON块返回。
`arguments`应该是一个字典，其中键对应于参数名称，值对应于请求的值。"""
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{query}"),
]).partial(rendered_tools=render_text_description_and_args(tools))

print(prompt.invoke({"query": "马拉松的世界纪录是多少？"}).to_string())
print("===========================")

# 文心一言，不支持函数调用的大模型，调用出错，本来是查询：马拉松的世界纪录是多少？，结果选择成了gaode_weather工具
# 月之暗面，可以成功输出结果，但是改变了Human的原始提问。变成了：马拉松世界纪录 最新
llm = ChatOpenAI(
    model="kimi-k2-instruct",
    api_key=os.environ.get("QIANFAN_API_KEY"),
    base_url=os.environ.get("QIANFAN_BASE_URL"),
    temperature=0
)

chain1 = prompt | llm | JsonOutputParser()
print(chain1.invoke({"query": "马拉松的世界纪录是多少？"}))

chain = prompt | llm | JsonOutputParser() | RunnablePassthrough.assign(output=invoke_tool)

print(chain.invoke({"query": "马拉松的世界纪录是多少？"}))
