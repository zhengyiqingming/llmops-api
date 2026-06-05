#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2025/12/18 9:51
@Author : 751363075@qq.com
@File : __init__.py.py
"""

import warnings

# 忽略 Marshmallow 的弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="marshmallow.*")
# 忽略 Jieba 的资源警告
warnings.filterwarnings("ignore", category=ResourceWarning, module="jieba.*")
# 忽略 HuggingFace Transformers 的权重未使用警告
warnings.filterwarnings("ignore", message=".*weights of the model checkpoint.*were not used.*")
