#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/10/12 11:25
@Author : 751363075@qq.com
@File : qwen_image_wrapper.py
"""
from dashscope import ImageSynthesis


class QwenImageWrapper:

    def __init__(
            self,
            api_key: str,
            model: str = "wanx-v1"
    ):
        self.api_key = api_key
        self.model = model

    def generate(
            self,
            prompt: str,
            size: str = "1024*1024"
    ):
        response = ImageSynthesis.call(
            api_key=self.api_key,
            model=self.model,
            prompt=prompt,
            size=size,
            n=1
        )

        if response.status_code != 200:
            raise Exception(
                f"图片生成失败:{response}"
            )

        return response.output.results[0].url
