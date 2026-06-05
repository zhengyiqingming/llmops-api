#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/26 11:46
@Author : 751363075@qq.com
@File : gaode_weather_tool.py
"""
import json

import dotenv
import os
from typing import Any, Type

import requests
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

dotenv.load_dotenv()


class GaodeIPlocateArgsSchema(BaseModel):
    ip: str = Field(description="需要查询位置的ip地址，例如：7.249.124.71")


class GaodeIPlocateTool(BaseTool):
    """根据传入的ip地址查询位置"""
    name = "gaode_iplocate"
    description = "当你根据ip查询位置时可以使用的工具"
    args_schema: Type[BaseModel] = GaodeIPlocateArgsSchema

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """根据传入的ip地址调用api获取ip对应的位置信息"""
        try:
            # 1.获取高德API秘钥，如果没有创建的话，则抛出错误，
            gaode_api_key = os.getenv("GAODE_API_KEY")
            if not gaode_api_key:
                return f"高德开放平台API未配置"
            # 2.从参数中获取ip
            ip = kwargs.get("ip", "")
            # ip_type默认为ipv4,只能查询中国ip
            api_domain = "https://restapi.amap.com/v3"
            session = requests.session()

            # 3.发起城市区域编码查询，根据ip获取位置信息
            iplocate_response = session.request(
                method="GET",
                url=f"{api_domain}/ip?key={gaode_api_key}&ip={ip}&output=json",
                headers={"Content-Type": "application/json;charset=UTF-8"},
            )
            iplocate_response.raise_for_status()
            iplocate_data = iplocate_response.json()
            if iplocate_data.get("info") == "OK":
                # 4.返回最后的结果字符串
                return json.dumps(iplocate_data)
            return f"获取{ip}位置信息失败"
        except Exception as e:
            print(e)
            return f"获取{kwargs.get('ip', '')}位置信息失败"


gaode_iplocate = GaodeIPlocateTool()

print(gaode_iplocate.invoke({"ip": "192.168.40.1"}))
