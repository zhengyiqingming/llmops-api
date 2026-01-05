#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/4 16:52
@Author : 751363075@qq.com
@File : 1.回调功能使用技巧.py
"""
import time
from typing import Any
from uuid import UUID

import dotenv
from langchain_core.messages import BaseMessage
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.callbacks import StdOutCallbackHandler, FileCallbackHandler, BaseCallbackHandler

dotenv.load_dotenv()


class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义LLMOPs回调处理器"""
    start_at: float = 0

    def on_chat_model_start(
            self,
            serialized: dict[str, Any],
            messages: list[list[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            tags: list[str] | None = None,
            metadata: dict[str, Any] | None = None,
            **kwargs: Any,
    ) -> Any:
        print("聊天模型开始执行了")
        print("serialized:", serialized)
        print("messages:", messages)
        self.start_at = time.time()

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            **kwargs: Any,
    ) -> Any:
        end_at: float = time.time()
        print("完成输出：", response)
        print("程序消耗：", end_at - self.start_at)


# 1.编排prompt
prompt = ChatPromptTemplate.from_template("{query}")

# 2.构建大语言模型
llm = ChatDeepSeek(model="deepseek-chat")

# 3.构建链
chain = {"query": RunnablePassthrough()} | prompt | llm | StrOutputParser()

# 4.调用链并执行
resp = chain.stream(
    "你好，你是？",
    config={"callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]})

for chunk in resp:
    pass
