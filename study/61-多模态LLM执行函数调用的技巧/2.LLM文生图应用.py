#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/3/5 18:00
@Author : 751363075@qq.com
@File : 2.LLM文生图应用.py
"""
import dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.openai_dalle_image_generation import OpenAIDALLEImageGenerationTool
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

dotenv.load_dotenv()

dalle = OpenAIDALLEImageGenerationTool(api_wrapper=DallEAPIWrapper(model="dall-e-3"))

llm = ChatOpenAI(model="deepseek-chat")
llm_with_tools = llm.bind_tools([dalle], tool_choice="openai_dalle")

chain = llm_with_tools | (lambda msg: msg.tool_calls[0]["args"]) | dalle

print(chain.invoke("帮我绘制一张老爷爷爬山的图片"))
