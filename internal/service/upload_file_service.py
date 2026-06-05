#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/4/9 11:54
@Author : 751363075@qq.com
@File : upload_file_service.py
"""
from injector import inject
from dataclasses import dataclass

from internal.model import UploadFile
from pkg.sqlalchemy import SQLAlchemy
from .base_service import BaseService


@inject
@dataclass
class UploadFileService(BaseService):
    """上传文件记录服务"""
    db: SQLAlchemy

    def create_upload_file(self, **kwargs) -> UploadFile:
        """创建文件上传记录"""
        return self.create(UploadFile, **kwargs)
