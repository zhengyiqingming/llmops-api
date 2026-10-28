#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/9/14 16:10
@Author : 751363075@qq.com
@File : chat.py
"""
from internal.core.language_model.entities.model_entity import BaseLanguageModel

from langchain_openai import ChatOpenAI


class Chat(ChatOpenAI, BaseLanguageModel):
    """OpenAI聊天模型基类"""
    pass
