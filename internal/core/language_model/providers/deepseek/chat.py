#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/9/14 16:10
@Author : 751363075@qq.com
@File : chat.py
"""
from typing import Tuple

import tiktoken
from langchain_openai import ChatOpenAI

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Chat(ChatOpenAI, BaseLanguageModel):
    """OpenAI聊天模型基类"""

    # 通过这种方式获取消息token数不会报错
    def _get_encoding_model(self) -> Tuple[str, tiktoken.Encoding]:
        """重写deepseek获取编码模型名字+模型函数，该类继承OpenAI，词表模型可以使用gpt-3.5-turbo防止出错"""
        # 1.将月之暗面的词表模型设置为gpt-3.5-turbo
        model = "gpt-3.5-turbo"

        # 2.返回模型名字+编码器
        return model, tiktoken.encoding_for_model(model)
