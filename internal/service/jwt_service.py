#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/6/4 11:18
@Author : 751363075@qq.com
@File : jwt_service.py
"""
import os
from typing import Any

from injector import inject
from dataclasses import dataclass
import jwt


@inject
@dataclass
class JwtService:
    """jwt服务"""

    @classmethod
    def generate_token(cls, payload: dict[str, Any]) -> str:
        """根据传递的载荷信息生成token信息"""
        secret_key = os.getenv('JWT_SECRET_KEY')
        return jwt.encode(payload, secret_key, algorithm='HS256')

    @classmethod
    def parse_token(cls, token: str) -> dict[str, Any]:
        """解析传入的token信息，得到载荷"""
        secret_key = os.getenv('JWT_SECRET_KEY')
        try:
            return jwt.decode(token, secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise ValueError("授权认证凭证已过期，请重新登陆")
        except jwt.InvalidTokenError:
            raise ValueError("解析token出错，请重新登陆")
        except Exception as e:
            raise e
