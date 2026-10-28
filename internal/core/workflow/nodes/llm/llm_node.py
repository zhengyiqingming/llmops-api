#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/8/5 16:57
@Author : 751363075@qq.com
@File : llm_node.py
"""
import time

from jinja2 import Template
from typing import Optional

from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from internal.core.workflow.entities.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entities.workflow_entity import WorkflowState

from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.llm.llm_entity import LLMNodeData
from internal.core.workflow.utils.helper import extract_variables_from_state


class LLMNode(BaseNode):
    """大语言模型节点"""
    node_data: LLMNodeData

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """大语言节点调用工具，根据输入字段+预设prompt生成对应的内容后输出"""
        # 1.提取节点输入变量字典映射
        start_at = time.perf_counter()
        inputs_dict = extract_variables_from_state(self.node_data.inputs, state)

        # 2.使用jinjia2格式模板
        template = Template(self.node_data.prompt)
        prompt_value = template.render(**inputs_dict)

        # 3.通过依赖管理器获取language_model_service并加载模型
        from app.http.module import injector
        from internal.service import LanguageModelService

        language_model_service = injector.get(LanguageModelService)
        llm = language_model_service.load_language_model(self.node_data.language_model_config)

        # 4.调用LLM并传递prompt后提取数据
        content = ""
        for chunk in llm.stream(prompt_value):
            content += chunk.content

        # 5.提取并构建输入数据结构
        outputs = {}
        if self.node_data.outputs:
            outputs[self.node_data.outputs[0].name] = content
        else:
            outputs["output"] = content

        # 6.构建响应状态并返回
        return {
            "node_results": [
                NodeResult(
                    node_data=self.node_data,
                    status=NodeStatus.SUCCEEDED,
                    inputs=inputs_dict,
                    outputs=outputs,
                    latency=(time.perf_counter() - start_at),
                )
            ]
        }
