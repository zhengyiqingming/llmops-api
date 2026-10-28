#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/6/29 17:09
@Author : 751363075@qq.com
@File : ai_service.py
"""
import json
from typing import Generator
from uuid import UUID

from injector import inject
from dataclasses import dataclass

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .conversation_service import ConversationService
from .base_service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from internal.exception import ForbiddenException
from internal.model import Account, Message
from ..entity.ai_entity import OPTIMIZE_PROMPT_TEMPLATE


@inject
@dataclass
class AIService(BaseService):
    """AI服务"""
    db: SQLAlchemy
    conversation_service: ConversationService

    def generate_suggested_questions_from_message_id(self, message_id: UUID, account: Account) -> list[str]:
        """根据传递的消息id+账号生成建议问题列表"""
        # 1.查询消息并校验权限信息
        message = self.get(Message, message_id)
        if not message or message.created_by != account.id:
            raise ForbiddenException("该条消息不存在或无权限")

        # 2.构建对话历史列表
        histories = f"Human:{message.query}\nAI:{message.answer}"

        # 3.调用服务生成建议问题
        return self.conversation_service.genarate_suggested_questions(histories)

    @classmethod
    def optimize_prompt(cls, prompt: str) -> Generator[str, None, None]:
        """根据传递的prompt进行优化生成"""
        # 1.构建优化prompt的提示词模板
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", OPTIMIZE_PROMPT_TEMPLATE),
            ("human", "{prompt}")
        ])

        # 2.构建LLM
        llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)

        # 3.组装优化列
        optimize_chain = prompt_template | llm | StrOutputParser()

        # 4.调用链并流式事件返回
        for optimize_prompt in optimize_chain.stream({"prompt": prompt}):
            # 5.组装响应数据
            data = {"optimize_prompt": optimize_prompt}
            yield f"event:optimize_prompt\ndata:{json.dumps(data)}\n\n"
