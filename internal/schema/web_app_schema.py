#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/10/30 17:11
@Author : 751363075@qq.com
@File : web_app_schema.py
"""
from flask_wtf import FlaskForm
from marshmallow import Schema, fields, pre_dump
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Optional, UUID

from internal.lib.helper import datetime_to_timestamp
from internal.model import App, Conversation


class GetWebAppResp(Schema):
    """获取WebApp基础信息响应结构"""
    id = fields.UUID(dump_default="")
    icon = fields.String(dump_default="")
    name = fields.String(dump_default="")
    description = fields.String(dump_default="")
    app_config = fields.Dict(dump_default={})

    @pre_dump
    def process_data(self, data: App, **kwargs):
        app_config = data.app_config
        return {
            "id": data.id,
            "icon": data.icon,
            "name": data.name,
            "description": data.description,
            "app_config": {
                "opening_statement": app_config.opening_statement,
                "opening_questions": app_config.opening_questions,
                "suggested_after_answer": app_config.suggested_after_answer,
            },
        }


class WebAppChatReq(FlaskForm):
    """WebApp对话请求结构体"""
    # 括号里的 "conversation_id"：这是给人看的。如果在自动生成 HTML 表单（传统 Web 开发）时，它会渲染成 <label>conversation_id</label>。如果你把它改成 "会话ID"，前端传的字段名依然要是左边的 conversation_id。
    conversation_id = StringField("conversation_id", default="", validators=[
        Optional(),
        UUID(message="会话id格式必须为uuid")
    ])
    query = StringField("query", default="", validators=[
        DataRequired(message="用户提问query不能为空"),
    ])


# FlaskForm 负责“收数据”（入参校验）
class GetConversationsReq(FlaskForm):
    """获取WebApp会话列表请求结构体"""
    is_pinned = BooleanField("is_pinned", default=False)


# Schema 负责“发数据”（出参序列化）
class GetConversationsResp(Schema):
    """获取WebApp会话列表响应结构体"""
    id = fields.UUID(dump_default="")
    name = fields.String(dump_default="")
    summary = fields.String(dump_default="")
    created_at = fields.Integer(dump_default=0)

    @pre_dump
    def process_data(self, data: Conversation, **kwargs):
        return {
            "id": data.id,
            "name": data.name,
            "summary": data.summary,
            "created_at": datetime_to_timestamp(data.created_at),
        }
