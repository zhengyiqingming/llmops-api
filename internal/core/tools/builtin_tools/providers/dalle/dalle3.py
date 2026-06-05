#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/17 10:26
@Author : 751363075@qq.com
@File : dalle3.py
"""
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field
from internal.lib.helper import add_attribute


class DallE3ArgsSchema(BaseModel):
    query: str = Field(description="输入应该是生成图像的文本提示（prompt）")


@add_attribute("args_schema", DallE3ArgsSchema)
def dalle3(**kwargs) -> BaseTool:
    """返回delle3绘图的langchain工具"""
    return OpenAIDALLEImageGenerationTool(
        api_wrapper=DallEAPIWrapper(model="dall-e-3", **kwargs),
        args_schema=DallE3ArgsSchema,
    )
