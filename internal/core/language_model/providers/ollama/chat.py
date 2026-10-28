#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/9/24 11:08
@Author : 751363075@qq.com
@File : chat.py
"""
from internal.core.language_model.entities.model_entity import BaseLanguageModel

from langchain_ollama import ChatOllama


class Chat(ChatOllama, BaseLanguageModel):
    """Ollama聊天模型"""
    pass
