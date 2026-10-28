#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/7/24 10:27
@Author : 751363075@qq.com
@File : category_entity.py
"""
from pydantic import BaseModel, Field


class CategoryEntity(BaseModel):
    """内置工具分类实体"""
    category: str = Field(default="")  # 分类唯一标识
    name: str = Field(default="")  # 分类对应的名称
