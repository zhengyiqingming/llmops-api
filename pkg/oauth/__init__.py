#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/6/5 16:27
@Author : 751363075@qq.com
@File : __init__.py.py
"""
from .oauth import OAuthUserInfo, OAuth
from .github_oauth import GithubOAuth

__all__ = ["OAuth", "OAuthUserInfo", "GithubOAuth"]
