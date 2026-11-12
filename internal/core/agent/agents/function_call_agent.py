#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/5/8 10:34
@Author : 751363075@qq.com
@File : function_call_agent.py
"""
import json
import re
import time
import uuid
import logging
import tiktoken
from typing import Literal, Generator

from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage, ToolMessage, AIMessage
from langgraph.constants import END
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph

from internal.core.agent.entities.agent_entity import (
    AgentState,
    AGENT_SYSTEM_PROMPT_TEMPLATE,
    DATASET_RETRIEVAL_TOOL_NAME, MAX_ITERATION_RESPONSE
)
from internal.exception import FailException

from ..entities.queue_entity import AgentThought, QueueEvent
from .base_agent import BaseAgent
from langchain_core.messages import messages_to_dict

from ...language_model.entities.model_entity import ModelFeature


class FunctionCallAgent(BaseAgent):
    """基于函数/工具调用的智能体"""

    def _build_agent(self) -> CompiledStateGraph:
        """构建LangGraph图结构编译程序"""
        # 1.构建图
        graph = StateGraph(AgentState)

        # 2.添加节点
        graph.add_node("preset_operation", self._preset_operation_node)
        graph.add_node("long_term_memory_recall", self._long_term_memory_recall_node)
        graph.add_node("llm", self._llm_node)
        graph.add_node("tools", self._tools_node)

        # 3.添加边，并设置起点和终点
        graph.set_entry_point("preset_operation")
        graph.add_conditional_edges("preset_operation", self._preset_operation_condition)
        graph.add_edge("long_term_memory_recall", "llm")
        graph.add_conditional_edges("llm", self._tools_condition)
        graph.add_edge("tools", "llm")

        # 4.编译应用并返回
        agent = graph.compile()

        return agent

    def _preset_operation_node(self, state: AgentState) -> AgentState:
        """预设操作，涵盖：输入审核、数据预处理、条件边等"""
        # 1.获取审核配置与用户输入query
        review_config = self.agent_config.review_config
        query = state["messages"][-1].content

        # 2.检测是否开启审核配置
        if review_config["enable"] and review_config["inputs_config"]["enable"]:
            contains_keyword = any(
                keyword in query for keyword in review_config["keywords"])  # 只要query存在一个敏感词，any就会返回true
            # 3.如果包含敏感词，则执行后续步骤
            if contains_keyword:
                preset_response = review_config["inputs_config"]["preset_response"]
                self.agent_queue_manager.publish(state["task_id"], AgentThought(
                    id=uuid.uuid4(),
                    task_id=state["task_id"],
                    event=QueueEvent.AGENT_MESSAGE,
                    thought=preset_response,
                    message=messages_to_dict(state["messages"]),
                    answer=preset_response,
                    latency=0,
                ))
                self.agent_queue_manager.publish(state["task_id"], AgentThought(
                    id=uuid.uuid4(),
                    task_id=state["task_id"],
                    event=QueueEvent.AGENT_END,
                ))
                return {"messages": [AIMessage(preset_response)]}

        return {"messages": []}

    def _long_term_memory_recall_node(self, state: AgentState) -> AgentState:
        """长期记忆召回节点"""
        # 1.根据传递的智能体配置判断是否需要召回长期记忆
        long_term_memory = ""
        if self.agent_config.enable_long_term_memory:
            long_term_memory = state["long_term_memory"]
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=uuid.uuid4(),
                task_id=state["task_id"],
                event=QueueEvent.LONG_TERM_MEMORY_RECALL,
                observation=long_term_memory,
            ))
        # 新增：动态生成可用工具列表的提示词
        tools_prompt = ""
        if self.agent_config.tools:
            tools_prompt = "\n\n【重要：你当前拥有以下工具，请严格按照名字调用，不要编造不存在的工具】\n"
            for tool in self.agent_config.tools:
                tools_prompt += f"- 工具名: `{tool.name}`\n  描述: {tool.description}\n"
        # 2.构建预设消息列表，并将preset_prompt+long_term_memory填充到系统消息中
        preset_messages = [
            SystemMessage(AGENT_SYSTEM_PROMPT_TEMPLATE.format(
                preset_prompt=self.agent_config.preset_prompt,
                long_term_memory=long_term_memory,
            ) + tools_prompt)
        ]

        # 3.将短期历史消息添加到消息列表中
        history = state["history"]
        if isinstance(history, list) and len(history) > 0:
            # 4.校验历史消息是不是复数形式，也就是[人类消息，AI消息，人类消息，AI消息...]
            if len(history) % 2 != 0:
                self.agent_queue_manager.publish_error(state["task_id"], "智能体历史消息列表格式错误")
                logging.exception(
                    "智能体历史消息列表格式错误, len(history)=%(len_history)d, history=%(history)s",
                    {"len_history": len(history), "history": json.dumps(messages_to_dict(history))},
                )
                raise FailException("智能体历史消息列表格式错误")
            # 5，拼接历史消息
            preset_messages.extend(history)

        # 6.拼接当前用户的提问消息
        human_message = state["messages"][-1]
        preset_messages.append(HumanMessage(human_message.content))

        # 7.处理预设消息，将预设消息添加到用户消息前，先去删除用户的原始消息，然后补充一个新的代替
        return {
            "messages": [RemoveMessage(id=human_message.id), *preset_messages],
        }

    def _llm_node(self, state: AgentState) -> AgentState:
        """大语言模型节点"""
        # 1.检测当前Agent迭代次数是否符合需求
        if state["iteration_count"] > self.agent_config.max_iteration_count:
            self.agent_queue_manager.publish(
                state["task_id"],
                AgentThought(
                    id=uuid.uuid4(),
                    task_id=state["task_id"],
                    event=QueueEvent.AGENT_MESSAGE,
                    thought=MAX_ITERATION_RESPONSE,
                    message=messages_to_dict(state["messages"]),
                    answer=MAX_ITERATION_RESPONSE,
                    latency=0,
                ))
            self.agent_queue_manager.publish(
                state["task_id"],
                AgentThought(
                    id=uuid.uuid4(),
                    task_id=state["task_id"],
                    event=QueueEvent.AGENT_END,
                ))
            return {"messages": [AIMessage(MAX_ITERATION_RESPONSE)]}

        # 2.从智能体配置中提取大语言模型
        id = uuid.uuid4()
        # 当前时间
        start_at = time.perf_counter()
        llm = self.llm

        # 3.检测大语言模型实例是否有bind_tools方法，如果没有则不绑定，如果有还需要检测tools是否为空，不为空则绑定
        if (
                ModelFeature.TOOL_CALL in llm.features
                and hasattr(llm, "bind_tools")
                and callable(getattr(llm, "bind_tools"))
                and len(self.agent_config.tools) > 0
        ):
            llm = llm.bind_tools(self.agent_config.tools)

        # 4.流式调用LLM输出对应的内容
        gathered = None
        is_first_chunk = True
        generation_type = ""
        try:
            for chunk in llm.stream(state["messages"]):
                if is_first_chunk:
                    gathered = chunk
                    is_first_chunk = False
                else:
                    gathered += chunk

                # 5.检测生成类型是工具参数还是文本生成
                if not generation_type:
                    if chunk.tool_calls:
                        generation_type = "thought"
                    elif chunk.content:
                        generation_type = "message"

                # 6.如果生成的是消息，则提交智能体消息事件
                if generation_type == "message":
                    # 7.提取片段内容，并检测是否开启输出审核
                    review_config = self.agent_config.review_config
                    content = chunk.content
                    if review_config["enable"] and review_config["outputs_config"]["enable"]:
                        for keyword in review_config["keywords"]:
                            content = re.sub(re.escape(keyword), "**", content, flags=re.IGNORECASE)

                    self.agent_queue_manager.publish(state["task_id"], AgentThought(
                        id=id,
                        task_id=state["task_id"],
                        event=QueueEvent.AGENT_MESSAGE,
                        thought=content,
                        message=messages_to_dict(state["messages"]),
                        answer=content,
                        # 当前时间-开始时间
                        latency=(time.perf_counter() - start_at),
                    ))
        except Exception as e:
            logging.exception(
                "LLM节点发生错误, 错误信息: %(error)s",
                {"error": str(e) or "LLM出现未知错误"}
            )
            # 1. 发送错误事件
            self.agent_queue_manager.publish_error(state["task_id"], f"llm节点发生错误，错误信息：{str(e)}")
            # 2. 强制发送结束事件，确保 AgentQueueManager 能收到 None 并跳出 listen 循环
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=uuid.uuid4(),
                task_id=state["task_id"],
                event=QueueEvent.AGENT_END,
            ))
            raise e

        # 8.计算LLM的输入+输出token总数
        # input_token_count = self.llm.get_num_tokens_from_messages(state["messages"])
        # output_token_count = self.llm.get_num_tokens_from_messages([gathered])
        enc = tiktoken.get_encoding("cl100k_base")  # 适用于多数现代模型的近似估算
        input_token_count = sum(
            len(enc.encode(str(m.content))) for m in state["messages"]
        )
        # output 侧：兼容 content 为空、gathered 为 None、以及工具调用参数
        if gathered is None:
            output_text = ""
        elif getattr(gathered, "content", ""):
            output_text = str(gathered.content)
        else:
            # 纯工具调用场景：content 为空，但 tool_calls 的参数 JSON 是真实输出
            output_text = json.dumps(gathered.tool_calls, ensure_ascii=False)

        output_token_count = len(enc.encode(output_text))

        # 9.获取输入/输出价格和单位
        input_price, output_price, unit = self.llm.get_pricing()

        # 10.计算总token+总成本
        total_token_count = input_token_count + output_token_count
        total_price = (input_token_count * input_price + output_token_count * output_price) * unit

        # 11.如果generation_type的最后类型为thought，则添加智能体推理事件
        print("_llm_node:generation_type", generation_type)
        if generation_type == "thought":
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=id,
                task_id=state["task_id"],
                event=QueueEvent.AGENT_THOUGHT,
                thought=json.dumps(gathered.tool_calls),
                # 消息相关字段
                message=messages_to_dict(state["messages"]),
                message_token_count=input_token_count,
                message_unit_price=input_price,
                message_price_unit=unit,
                # 答案相关字段
                answer="",
                answer_token_count=output_token_count,
                answer_unit_price=output_price,
                answer_price_unit=unit,
                # Agent推理统计相关
                total_token_count=total_token_count,
                total_price=total_price,
                # 当前时间-开始时间
                latency=(time.perf_counter() - start_at),
            ))
        elif generation_type == "message":
            # 7.如果generation_type的最后类型为message，则表示已经拿到了最终答案，推送一条空内容用于计算总token+总成本，并停止监听
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=id,
                task_id=state["task_id"],
                event=QueueEvent.AGENT_MESSAGE,
                thought="",
                # 消息相关字段
                message=messages_to_dict(state["messages"]),
                message_token_count=input_token_count,
                message_unit_price=input_price,
                message_price_unit=unit,
                # 答案相关字段
                answer="",
                answer_token_count=output_token_count,
                answer_unit_price=output_price,
                answer_price_unit=unit,
                # Agent推理统计相关
                total_token_count=total_token_count,
                total_price=total_price,
                # 当前时间-开始时间
                latency=(time.perf_counter() - start_at),
            ))
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=uuid.uuid4(),
                task_id=state["task_id"],
                event=QueueEvent.AGENT_END,
            ))

        return {"messages": [gathered], "iteration_count": state["iteration_count"] + 1}

    def _tools_node(self, state: AgentState) -> AgentState:
        """工具执行节点"""
        # 1.将工具列表转换成字典，便于调用指定的工具
        tools_by_name = {tool.name: tool for tool in self.agent_config.tools}

        # 2.提取消息中的工具调用参数
        tool_calls = state["messages"][-1].tool_calls

        # 3.循环执行工具组装工具消息
        messages = []
        for tool_call in tool_calls:
            # 4.创建智能体动作事件id，并记录开始时间
            id = uuid.uuid4()
            start_at = time.perf_counter()  # 开始时间

            try:
                # 5.获取工具并调用工具
                if tool_call["name"] not in tools_by_name:
                    raise ValueError(f"未找到名为 {tool_call['name']} 的工具")
                tool = tools_by_name[tool_call["name"]]
                tool_result = tool.invoke(tool_call["args"])
                print("tool_result:", tool_result)

                # ================= 使用通用解析函数 =================
                content_str = self.format_tool_result(tool_result)
                print("format_tool_result--content_str:", content_str)
                # ====================================================

            except Exception as e:
                logging.error(f"工具 [{tool_call['name']}] 执行异常: {e}", exc_info=True)  # 👈 关键
                content_str = json.dumps({"error": f"工具执行出错，错误信息：{str(e)}"}, ensure_ascii=False)

            # 7.将工具消息添加到消息列表中
            messages.append(ToolMessage(
                tool_call_id=tool_call["id"],
                content=content_str,
                name=tool_call["name"],
            ))

            # 7.判断执行工具的名字、提交不同事件，涵盖智能体动作以及知识库检索
            event = (
                QueueEvent.AGENT_ACTION
                if tool_call["name"] != DATASET_RETRIEVAL_TOOL_NAME
                else QueueEvent.DATASET_RETRIEVAL
            )
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=id,
                task_id=state["task_id"],
                event=event,
                observation=content_str,
                tool=tool_call["name"],
                tool_input=tool_call["args"],
                latency=(time.perf_counter() - start_at),  # 当前时间-开始时间
            ))

        return {"messages": messages}

    @classmethod
    def _tools_condition(cls, state: AgentState) -> Literal["tools", "__end__"]:
        """检测下一个节点是执行tools节点，还是直接结束"""
        # 1.提取状态中的最后一条消息（AI消息）
        messages = state["messages"]
        ai_message = messages[-1]
        # 2.检测是否存在tools_call这个参数，如果存在则执行tools节点，否则结束
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"

        return END

    @classmethod
    def _preset_operation_condition(cls, state: AgentState) -> Literal["long_term_memory_recall", "__end__"]:
        """预设操作条件边，用于判断是否触发预设响应"""
        # 1.提取状态的最后一条消息
        messages = state["messages"][-1]

        # 2.判断消息的类型，如果是AI消息，则说明触发了审核机制，直接结束
        if messages.type == "ai":
            return END

        return "long_term_memory_recall"

    @classmethod
    def format_tool_result(cls, tool_result) -> str:
        """通用的工具结果解析器，将复杂嵌套结构转为大模型友好的 Markdown 纯文本"""
        if tool_result is None:
            return "无返回结果"

        # 1. 如果是纯字符串，直接返回
        if isinstance(tool_result, str):
            return tool_result

        # 2. 对象转字典
        if hasattr(tool_result, "model_dump"):
            tool_result = tool_result.model_dump()
        elif hasattr(tool_result, "__dict__") and not isinstance(tool_result, dict):
            tool_result = vars(tool_result)

        # 3. 精准提取内容
        if isinstance(tool_result, dict):
            # 优先提取 outputs 里的 llm_output（你最想要的最终回答）
            outputs = tool_result.get("outputs")
            if isinstance(outputs, dict) and outputs.get("llm_output"):
                return str(outputs["llm_output"])

            # 如果没有 outputs，看看有没有直接传 llm_output
            if tool_result.get("llm_output"):
                return str(tool_result["llm_output"])

            # 如果都没有，可能调用了其他工具，全量转成格式化的 JSON 兜底
            try:
                # 过滤掉 node_results，因为里面全是对象，不仅大模型看不懂还会引发序列化错误
                clean_result = {k: v for k, v in tool_result.items() if k != "node_results"}
                return json.dumps(clean_result, ensure_ascii=False, indent=2, default=str)
            except Exception:
                return str(tool_result)

        # 4. 兜底：如果是列表（比如 node_results），直接转字符串
        return str(tool_result)
