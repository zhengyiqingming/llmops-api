#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/4/14 16:19
@Author : 751363075@qq.com
@File : jieba_service.py
"""
from dataclasses import dataclass

import jieba.analyse
from injector import inject
from jieba.analyse import default_tfidf

from internal.entity.jieba_entity import STOPWORD_SET


@inject
@dataclass
class JiebaService:
    """结巴分词服务"""

    def __init__(self):
        """构造函数，扩展jieba的停用词"""
        default_tfidf.stop_words = STOPWORD_SET

    @classmethod
    def extract_keywords(cls, text: str, max_keyword_pre_chunk: int = 10) -> list[str]:
        """根据输入的文本，提取对应的文本关键词列表"""
        return jieba.analyse.extract_tags(
            sentence=text,
            topK=max_keyword_pre_chunk,
        )
