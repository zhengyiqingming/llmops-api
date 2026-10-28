#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/7/25 10:27
@Author : 751363075@qq.com
@File : workflow.py
"""
from typing import Any, Optional, Iterator

from flask import current_app
from langchain_core.pydantic_v1 import PrivateAttr, BaseModel, Field, create_model
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import Input, Output
from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph, StateGraph

from internal.core.workflow.entities.node_entity import NodeType
from internal.core.workflow.entities.variable_entity import VARIABLE_TYPE_MAP
from internal.core.workflow.entities.workflow_entity import WorkflowConfig, WorkflowState
from internal.core.workflow.nodes import StartNode, EndNode, LLMNode, TemplateTransformNode, DatasetRetrievalNode, \
    CodeNode, ToolNode, HttpRequestNode
from internal.exception import ValidateErrorException

# 节点类映射
NodeClass = {
    NodeType.START: StartNode,
    NodeType.END: EndNode,
    NodeType.LLM: LLMNode,
    NodeType.TEMPLATE_TRANSFORM: TemplateTransformNode,
    NodeType.DATASET_RETRIEVAL: DatasetRetrievalNode,
    NodeType.CODE: CodeNode,
    NodeType.TOOL: ToolNode,
    NodeType.HTTP_REQUEST: HttpRequestNode,
}


class Workflow(BaseTool):
    """工作流Langchain工具类"""
    _workflow_config: WorkflowConfig = PrivateAttr(None)
    _workflow: CompiledStateGraph = PrivateAttr(None)

    def __init__(self, workflow_config: WorkflowConfig, **kwargs: Any):
        """构造函数，完成工作流函数的初始化"""
        # 1.调用父类构造喊出完成基础数据的初始化
        super().__init__(
            name=workflow_config.name,
            description=workflow_config.description,
            args_schema=self._build_args_schema(workflow_config),
            **kwargs
        )

        # 2.完善工作流配置与工作流图程序的初始化
        self._workflow_config = workflow_config
        self._workflow = self._build_workflow()

    @classmethod
    def _build_args_schema(cls, workflow_config: WorkflowConfig) -> type[BaseModel]:
        """构建输入参数结构体"""
        # 1.提取开始节点的输入参数信息
        fields = {}
        inputs = next(
            (node.inputs for node in workflow_config.nodes if node.node_type == NodeType.START.value),
            []
        )
        # 2.循环遍历所有输入信息并创建字段映射
        for input in inputs:
            field_name = input.name
            field_type = VARIABLE_TYPE_MAP.get(input.type, str)
            field_required = input.required
            field_description = input.description

            fields[field_name] = (
                field_type if field_required else Optional[field_type],
                Field(description=field_description),
            )

        # 3.调用create_model创建一个BaseModel类，并使用上述分析好的字段
        return create_model("DynamicModel", **fields)

    def _build_workflow(self) -> CompiledStateGraph:
        """构建编译后的工作流图程序"""
        # 1.构建graph图程序结构
        graph = StateGraph(WorkflowState)

        # 2.提取nodes和edges信息
        nodes = self._workflow_config.nodes
        edges = self._workflow_config.edges

        # 3.循环遍历nodes节点信息添加节点
        for node in nodes:
            node_flag = f"{node.node_type}_{node.id}"
            if node.node_type == NodeType.START.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.START](node_data=node),
                )
            elif node.node_type == NodeType.LLM.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.LLM](node_data=node),
                )
            elif node.node_type == NodeType.TEMPLATE_TRANSFORM.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.TEMPLATE_TRANSFORM](node_data=node),
                )
            elif node.node_type == NodeType.DATASET_RETRIEVAL.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.DATASET_RETRIEVAL](
                        flask_app=current_app._get_current_object(),
                        account_id=self._workflow_config.account_id,
                        node_data=node,
                    ),
                )
            elif node.node_type == NodeType.CODE.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.CODE](node_data=node),
                )
            elif node.node_type == NodeType.TOOL.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.TOOL](node_data=node),
                )
            elif node.node_type == NodeType.HTTP_REQUEST.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.HTTP_REQUEST](node_data=node),
                )
            elif node.node_type == NodeType.END.value:
                graph.add_node(
                    node_flag,
                    NodeClass[NodeType.END](node_data=node),
                )
            else:
                raise ValidateErrorException("工作流节点类型错误，请核实后重试")

        # 4.循环遍历edges信息添加边
        parallel_edges = {}  # 平行边 key:终点，value：起点列表
        start_node = ""
        end_node = ""

        for edge in edges:
            # 5.计算并获取并行边
            source_node = f"{edge.source_type.value}_{edge.source}"
            target_node = f"{edge.target_type.value}_{edge.target}"
            if target_node not in parallel_edges:
                parallel_edges[target_node] = [source_node]
            else:
                parallel_edges[target_node].append(source_node)

            # 6.检测特殊节点（开始节点、结束节点），需要写成两个if的形式，避免只有一条边的情况识别失败
            if edge.source_type.value == NodeType.START.value:
                start_node = f"{edge.source_type.value}_{edge.source}"
            if edge.target_type.value == NodeType.END.value:
                end_node = f"{edge.target_type.value}_{edge.target}"

        # 7.设置开始和终点
        graph.set_entry_point(start_node)
        graph.set_finish_point(end_node)

        # 8.循环遍历合并边
        for target_node, source_nodes in parallel_edges.items():
            graph.add_edge(source_nodes, target_node)

        # 7.构建图程序并编译
        return graph.compile()

    def invoke(self, input: Any, config: Optional[RunnableConfig] = None, **kwargs: Any) -> Any:
        """重写 invoke 方法，直接处理输入"""

        # 处理输入参数
        if isinstance(input, dict):
            input_dict = input
        elif isinstance(input, BaseModel):
            input_dict = input.dict()
        else:
            input_dict = {"input": input}

        # 如果 kwargs 有值，合并到 input_dict
        if kwargs:
            input_dict.update(kwargs)

        # 构建完整的 WorkflowState
        state = {
            "inputs": input_dict,
            "outputs": {},
            "node_results": []
        }

        return self._workflow.invoke(state, config=config)

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """工作流组件基础run方法,这个方法不会被调用，保留作为后备"""
        # 如果 args 有值，使用 args[0]（通常是传入的字典）
        if args:
            # 如果 args[0] 是字典，直接使用
            if isinstance(args[0], dict):
                input_dict = args[0]
            else:
                input_dict = {"input": args[0]}
        else:
            # 否则使用 kwargs
            input_dict = kwargs

        # 合并 kwargs 到 input_dict（如果 kwargs 有值）
        if kwargs:
            input_dict.update(kwargs)

        # 构建完整的 WorkflowState
        state = {
            "inputs": input_dict,
            "outputs": {},
            "node_results": []
        }

        return self._workflow.invoke(state)

    def stream(
            self,
            input: Input,
            config: Optional[RunnableConfig] = None,
            **kwargs: Optional[Any],
    ) -> Iterator[Output]:
        """工作流流式输出每个节点对应的结果"""
        return self._workflow.stream({"inputs": input})
