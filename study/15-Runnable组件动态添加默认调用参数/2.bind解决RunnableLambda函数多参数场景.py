#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/15 17:33
@Author : 751363075@qq.com
@File : 2.bind解决RunnableLambda函数多参数场景.py
"""
import random

from langchain_core.runnables import RunnableLambda


def get_weather(location: str, unit: str, name: str) -> str:
    """根据传入的位置信息+温度单位，获取对应的天气信息"""
    print("location:", location)
    print("unit:", unit)
    print("name:", name)
    return f"{location}天气为{random.randint(24, 40)}{unit}"


get_weather_runnable = RunnableLambda(get_weather).bind(unit="摄氏度", name="莫小可")
print(get_weather_runnable.kwargs)

resp = get_weather_runnable.invoke("广州")

print(resp)
