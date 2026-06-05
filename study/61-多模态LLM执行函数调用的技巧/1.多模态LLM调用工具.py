#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/5 16:32
@Author : 751363075@qq.com
@File : 1.多模态LLM调用工具.py
"""
import json

import dotenv
import os
from typing import Any, Type

import requests
from langchain_core.output_parsers import StrOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

dotenv.load_dotenv()


class GaodeWeatherArgsSchema(BaseModel):
    city: str = Field(description="需要查询天气预报的目标城市，例如：广州")


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


# 1.构建prompt
prompt = ChatPromptTemplate.from_messages([
    ("human", "请获取如下上传图片所在城市的天气预报：<image_url>{image_url}</image_url>"
     )
])
weather_prompt = ChatPromptTemplate.from_template("""请整理下传递的城市的天气预报信息，并以用户友好的方式输出。

<weather>
{weather}
</weather>""")

# 2.构建LLM并绑定工具
llm = ChatOpenAI(
    model="glm-5",
    base_url=os.getenv("ZAI_BASE_URL"),
    api_key=os.getenv("ZAI_API_KEY"),
)
llm_with_tools = llm.bind_tools([GaodeWeatherTool()], tool_choice="gaode_weather")

chain0 = (
        {"image_url": RunnablePassthrough()}
        | prompt
        | llm_with_tools
)
print(chain0.invoke("https://img1.baidu.com/it/u=644490943,1781886584&fm=253&fmt=auto&app=138&f=JPEG"))

# 3.创建链应用并执行
chain = (
        {
            "weather": (
                    {"image_url": RunnablePassthrough()}
                    | prompt
                    | llm_with_tools
                    | (lambda msg: msg.tool_calls[0]["args"])
                    | GaodeWeatherTool()
            )
        }
        | weather_prompt | llm | StrOutputParser()
)

print(chain.invoke("https://img1.baidu.com/it/u=644490943,1781886584&fm=253&fmt=auto&app=138&f=JPEG"))
