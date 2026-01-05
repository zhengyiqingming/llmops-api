#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/29 10:20
@Author : 751363075@qq.com
@File : test_app_handle.py
"""
import pytest
from pkg.response import HttpCode


class TestAppHandle:
    """app控制器的测试类"""

    @pytest.mark.parametrize("query", [None, "你好，你是谁？"])
    def test_completion(self, query, client):
        resp = client.post("/app/completion", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
