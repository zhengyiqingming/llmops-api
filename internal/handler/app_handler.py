#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 11:26
@Author : 751363075@qq.com
@File : app_handler.py
"""
import json
from queue import Queue
import uuid
from operator import itemgetter
from threading import Thread
from typing import Dict, Any, Literal, Generator
from uuid import UUID
from dataclasses import dataclass

from injector import inject
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers import Run
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langgraph.constants import END
from langgraph.graph import MessagesState, StateGraph
from langchain_core.messages import ToolMessage
from redis import Redis

from internal.entity.conversation_entity import InvokeFrom
from internal.schema.app_schema import CompletionReq
from internal.service import AppService, ApiToolService, EmbeddingsService, ConversationService
from internal.service.vector_database_service import VectorDataBaseService
from pkg.response import success_json, validate_error_json, success_message, compact_generate_response
from internal.task.demo_task import demo_task
from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from internal.core.agent.agents import FunctionCallAgent, AgentQueueManager
from internal.core.agent.entities.agent_entity import AgentConfig


@inject
@dataclass
class AppHandler:
    """注入应用控制器"""
    app_service: AppService
    vector_database_service: VectorDataBaseService
    api_tool_service: ApiToolService
    embeddings_service: EmbeddingsService
    builtin_provider_manager: BuiltinProviderManager
    conversation_service: ConversationService
    redis_client: Redis

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已成功创建，id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id为:{app.id}")

    @classmethod
    def _load_memory_variables(cls, input: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        """加载记忆变量信息"""
        # 1.从config中获取configurable的信息
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        """存储对应的上下文信息到记忆实体中"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: UUID):
        """应用会话调试聊天接口，该接口为流式事件输出"""
        # 1.提取从接口中获取的输入,POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.定义工具列表
        tools = [
            self.builtin_provider_manager.get_tool("google", "google_serper")(),
            self.builtin_provider_manager.get_tool("time", "current_time")(),
            self.builtin_provider_manager.get_tool("gaode", "gaode_weather")(),
        ]

        agent = FunctionCallAgent(
            AgentConfig(
                llm=ChatOpenAI(model="deepseek-chat"),
                enable_long_term_memory=True,
                tools=tools,
            ),
            AgentQueueManager(
                user_id=uuid.uuid4(),
                task_id=uuid.uuid4(),
                invoke_from=InvokeFrom.DEBUGGER,
                redis_client=self.redis_client,
            ),
        )

        def stream_event_response() -> Generator:
            """流式事件输出响应"""
            for agent_queue_event in agent.run(req.query.data, [], "用户介绍自己叫莫小可"):
                data = {
                    "id": str(agent_queue_event.id),
                    "task_id": str(agent_queue_event.task_id),
                    "event": agent_queue_event.event,
                    "thought": agent_queue_event.thought,
                    "observation": agent_queue_event.observation,
                    "tool": agent_queue_event.tool,
                    "tool_input": agent_queue_event.tool_input,
                    "answer": agent_queue_event.answer,
                    "latency": agent_queue_event.latency,
                }
                yield f"event:{agent_queue_event.event}\ndata:{json.dumps(data)}\n\n"

        return compact_generate_response(stream_event_response())

    def ping(self):
        from internal.core.agent.agents import FunctionCallAgent
        from internal.core.agent.entities.agent_entity import AgentConfig
        from langchain_openai import ChatOpenAI

        agent = FunctionCallAgent(AgentConfig(
            llm=ChatOpenAI(model="deepseek-reasoner"),
            preset_prompt="你是一个拥有20年经验的诗人，请根据用户提供的主题来写一首诗"
        ))
        state = agent.run("程序员", [], "")
        content = state["messages"][-1].content

        return success_json({"content": content})
