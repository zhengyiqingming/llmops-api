#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/13 17:58
@Author : 751363075@qq.com
@File : 2.使用百度千帆平台的重排序功能.py
"""
import requests
import json


def main():
    url = "https://qianfan.baidubce.com/v2/rerank"

    payload = json.dumps({
        "model": "bce-reranker-base",
        "query": "上海天气",
        "documents": [
            "上海气候",
            "北京美食"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer bce-v3/ALTAK-t4NTjh5x6DqFxu4Vr08OU/ff94699fd19cbd33eb067ef56a868a6771ebf701'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()
