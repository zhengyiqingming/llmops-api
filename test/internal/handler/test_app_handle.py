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

    @pytest.mark.parametrize(
        "app_id, query",
        [
            ("6fa459ea-ee8a-3ca4-894e-db77e160355e", None),
            ("6fa459ea-ee8a-3ca4-894e-db77e160355e", "请简单介绍一下LLMOps")
        ]
    )
    def test_completion(self, app_id, query, client):
        resp = client.post(f"/apps/{app_id}/debug", json={"query": query})
        assert resp.status_code == 200
        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
