#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/4/10 11:56
@Author : 751363075@qq.com
@File : demo_task.py
"""
import logging
import time
from uuid import UUID
from flask import current_app

from celery import shared_task


@shared_task
def demo_task(id: UUID) -> str:
    """测试异步任务"""
    logging.info("睡眠5秒")
    time.sleep(5)
    logging.info(f"id的值：{id}")
    logging.info(f"配置信息{current_app.config}")
    return "莫小可"
