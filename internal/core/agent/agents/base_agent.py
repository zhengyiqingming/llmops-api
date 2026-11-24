#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/5/8 9:58
@Author : 751363075@qq.com
@File : base_agent.py
"""
import uuid
from threading import Thread
from typing import Optional, Any, Iterator
from abc import abstractmethod

from internal.core.language_model.entities.model_entity import BaseLanguageModel
from langgraph.graph.state import CompiledStateGraph

from internal.core.agent.entities.agent_entity import AgentConfig, AgentState
from internal.core.agent.entities.queue_entity import AgentThought, AgentResult, QueueEvent
from internal.exception import FailException
from .agent_queue_manager import AgentQueueManager
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.load import Serializable
from langchain_core.pydantic_v1 import PrivateAttr


class BaseAgent(Serializable, Runnable):
    """基于Runnable的基础智能体基类"""
    # 实现langchain的两大核心类：Serializable, Runnable组件，就变成Runnable可运行组件
    llm: BaseLanguageModel
    agent_config: AgentConfig
    _agent: CompiledStateGraph = PrivateAttr(None)  # 属性定义成PrivateAttr(None)，让子类也能使用这个属性
    _agent_queue_manager: AgentQueueManager = PrivateAttr(None)  # “_”表示私有变量

    class Config:
        # 允许传递私有属性，私有属性允许接收任意类型，且不需要校验私有属性
        arbitrary_types_allowed = True

    def __init__(
            self,
            llm: BaseLanguageModel,  # 显式位置参数
            agent_config: AgentConfig,  # 显式位置参数
            *args,  # 收集额外的位置参数，例如"gpt-4"，0.7, "sk-abc123"
            **kwargs,  # 收集额外的关键字参数，就是 key=value 的形式
    ):
        """构造函数，初始化智能体图结构程序"""
        super().__init__(*args, llm=llm, agent_config=agent_config, **kwargs)
        self._agent = self._build_agent()
        self._agent_queue_manager = AgentQueueManager(
            user_id=agent_config.user_id,
            invoke_from=agent_config.invoke_from,
        )

    @abstractmethod
    def _build_agent(self) -> CompiledStateGraph:
        """构建智能体函数，等待子类实现"""
        raise NotImplementedError("_build_agent()未实现")

    def invoke(self, input: AgentState, config: Optional[RunnableConfig] = None) -> AgentResult:
        """块内容响应，一次性生成完整内容后返回"""
        # 1.调用stream方法获取流式输出数据
        content = input["messages"][0].content
        query = ""
        image_urls = []
        if isinstance(content, str):
            query = content
        elif isinstance(content, list):
            query = content[0]["text"]
            image_urls = [chunk["image_url"]["url"] for chunk in content if chunk.get("type") == "image_url"]
        agent_result = AgentResult(query=query, image_urls=image_urls)
        agent_thoughts = {}
        for agent_thought in self.stream(input, config):
            # 2.提取事件id并转换成字符串
            event_id = str(agent_thought.id)

            # 3.除了ping事件，其他事件全部记录
            if agent_thought.event != QueueEvent.PING:
                # 4.单独处理agent_message事件，因为该事件为数据叠加
                if agent_thought.event == QueueEvent.AGENT_MESSAGE:
                    # 5.检测是否存储了事件
                    if event_id not in agent_thoughts:
                        agent_thoughts[event_id] = agent_thought
                    else:
                        # 7.叠加智能体消息事件
                        agent_thoughts[event_id] = agent_thoughts[event_id].model_copy(update={
                            "thought": agent_thoughts[event_id].thought + agent_thought.thought,
                            "answer": agent_thoughts[event_id].answer + agent_thought.answer,
                            "latency": agent_thought.latency,
                        })
                    # 8.更新智能体消息答案
                    agent_result.answer += agent_thought.answer
                else:
                    # 9.处理其他类型的智能体事件，类型均是覆盖
                    agent_thoughts[event_id] = agent_thought

                    # 10.单独判断是否为异常消息类型，如果是则修改状态并记录错误
                    if agent_thought.event in [QueueEvent.STOP, QueueEvent.ERROR, QueueEvent.TIMEOUT]:
                        agent_result.status = agent_thought.event
                        agent_result.error = agent_thought.observation if agent_thought.event == QueueEvent.ERROR else ""

        # 11.将推理字典装换为列表并存储
        agent_result.agent_thoughts = [agent_thought for agent_thought in agent_thoughts.values()]

        # 12.完善message,使用next生成器：从生成器中取第一个满足条件的元素,找不到就给一个空列表
        # 在所有智能体的思考记录中，找到第一个标记为 AGENT_MESSAGE 的事件，将其消息内容作为最终结果；如果没有这样的消息，则设为空列表。
        agent_result.message = next(
            (agent_thought.message for agent_thought in agent_thoughts.values()
             if agent_thought.event == QueueEvent.AGENT_MESSAGE),
            []
        )

        # 13.更新总耗时
        agent_result.latency = sum([agent_thought.latency for agent_thought in agent_thoughts.values()])

        return agent_result

    def stream(
            self,
            input: AgentState,
            config: Optional[RunnableConfig] = None,
            **kwargs: Optional[Any],
    ) -> Iterator[AgentThought]:
        """流式输出，每个Not节点，或者LLM每生成一个token时，则会返回相应内容"""
        # 1.检测子类是否已构建agent智能体，如果未构建则抛出错误
        if not self._agent:
            raise FailException("智能体未构建成功，请核实后尝试")

        # 2.构建对应的任务id及数据初始化
        input["task_id"] = input.get("task_id", uuid.uuid4())
        input["history"] = input.get("history", [])
        input["iteration_count"] = input.get("iteration_count", 0)

        # 3.创建子线程并执行
        thread = Thread(
            target=self._agent.invoke,
            args=(input,)  # 元组
        )
        thread.start()

        # 4.调用队列管理器监听数据，并返回迭代器
        yield from self._agent_queue_manager.listen(input["task_id"])

    @property
    def agent_queue_manager(self) -> AgentQueueManager:
        """只读属性，返回智能体队列管理器"""
        return self._agent_queue_manager
