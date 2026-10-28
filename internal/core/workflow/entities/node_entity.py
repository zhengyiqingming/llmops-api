#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/7/25 10:42
@Author : 751363075@qq.com
@File : node_entity.py
"""
from enum import Enum
from typing import Any
from uuid import UUID

from langchain_core.pydantic_v1 import BaseModel, Field


class NodeType(Enum):
    """节点类型枚举"""
    START = "start"
    LLM = "llm"
    TOOL = "tool"
    CODE = "code"
    DATASET_RETRIEVAL = "dataset_retrieval"
    HTTP_REQUEST = "http_request"
    TEMPLATE_TRANSFORM = "template_transform"
    END = "end"

    class Config:
        use_enum_values = True  # 自动将枚举转换为值


class BaseNodeData(BaseModel):
    """基础节点数据"""

    class Position(BaseModel):
        """节点坐标基础模型"""
        x: float = 0
        y: float = 0

    id: UUID  # 节点id，数值必须唯一
    node_type: NodeType  # 节点类型
    title: str = ""  # 节点标题，数值也必须唯一
    description: str = ""  # 节点描述信息
    position: Position = Field(default_factory=lambda: {"x": 0, "y": 0})  # 节点对应的坐标信息

    class Config:
        use_enum_values = True  # 自动将枚举转换为值
        allow_population_by_field_name = True  # 允许通过字段名进行赋值（这时字段名和别名都可以赋值了）


class NodeStatus(str, Enum):
    """节点状态"""
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class NodeResult(BaseModel):
    """节点运行结果"""
    node_data: BaseNodeData  # 节点基础数据
    status: NodeStatus = NodeStatus.RUNNING  # 节点运行状态
    inputs: dict[str, Any] = Field(default_factory=dict)  # 节点输入数据
    outputs: dict[str, Any] = Field(default_factory=dict)  # 节点输出数据
    latency: float = 0  # 节点响应耗时
    error: str = ""  # 节点运行错误信息

    class Config:
        use_enum_values = True  # 自动将枚举转换为值
        json_encoders = {
            NodeType: lambda v: v.value if hasattr(v, 'value') else str(v),
            NodeStatus: lambda v: v.value if hasattr(v, 'value') else str(v),
        }
