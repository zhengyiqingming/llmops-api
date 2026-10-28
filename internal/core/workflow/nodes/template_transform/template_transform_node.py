#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/8/6 15:58
@Author : 751363075@qq.com
@File : template_transform_node.py
"""
import time
from typing import Optional

from jinja2 import Template
from langchain_core.runnables import RunnableConfig

from internal.core.workflow.entities.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entities.workflow_entity import WorkflowState
from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.template_transform.template_transform_entity import TemplateTransformNodeData
from internal.core.workflow.utils.helper import extract_variables_from_state


class TemplateTransformNode(BaseNode):
    """模板转换节点，将多个变量信息合并成一个"""
    node_data: TemplateTransformNodeData

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """模板转换节点执行函数，将传递的多个变量合并成字符串后返回"""
        # 1.提取节点输入变量字典映射
        start_at = time.perf_counter()
        inputs_dict = extract_variables_from_state(self.node_data.inputs, state)

        # 5.使用jinjia2格式模板
        template = Template(self.node_data.template)
        template_value = template.render(**inputs_dict)

        # 6.提取并构建输入数据结构
        outputs = {
            "output": template_value
        }

        # 7.构建响应状态并返回
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
