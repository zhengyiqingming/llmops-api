#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/2/2 11:06
@Author : 751363075@qq.com
@File : 1.问答转换器示例.py
"""
import json
import os
import ssl
from typing import List, Dict

import dotenv
from doctran.doctran import DocumentTransformationBuilder
from langchain_core.documents import Document
from langchain_community.document_transformers import DoctranQATransformer

dotenv.load_dotenv()


def patch_doctran():
    """修补 Doctran 以禁用函数调用"""
    global original_interrogate

    from doctran import Document

    def new_interrogate(self, **kwargs) -> 'DocumentTransformationBuilder':
        """替代的 interrogate 方法，不使用函数调用"""
        # 构建提示词
        prompt = """请基于以下文档内容生成高质量的问答对。

文档内容: {document}

要求:
1. 生成10个问题，涵盖文档的主要知识点
2. 每个问题都要有对应的答案
3. 答案要准确、完整
4. 返回JSON格式

请返回如下JSON格式:
{{
  "questions_and_answers": [
    {{"question": "第一个问题是什么?", "answer": "第一个问题的答案..."}},
    {{"question": "第二个问题是什么?", "answer": "第二个问题的答案..."}}
  ]
}}"""
        # 使用 ChatOpenAI 直接调用
        from langchain.chat_models import ChatOpenAI

        llm = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE"),
            temperature=0.3
        )
        response = llm.invoke(prompt.format(document=self.raw_content))
        print(response)
        # 尝试解析 JSON
        response_text = response.content.strip()

        # 清理响应
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        print(response_text)
        data = json.loads(response_text)
        document = Document(
            uri=self.uri,
            id=self.id,
            content_type=self.content_type,
            config=self.config,
            raw_content=self.raw_content,
            transformed_content=response.content,
            extracted_properties=data
        )
        transformation_builder = DocumentTransformationBuilder(document)
        return transformation_builder

    # 保存原始方法
    original_interrogate = Document.interrogate

    # 替换方法
    Document.interrogate = new_interrogate


# 使用修补后的 Doctran
patch_doctran()

# 1.构建文档列表
page_content = """
机密文件 - 仅供内部使用
日期：2023年7月1日
主题：各种话题的更新和讨论
亲爱的团队，
希望这封邮件能找到你们一切安好。在这份文件中，我想向你们提供一些重要的更新，并讨论需要我们关注的各种话题。请将此处包含的信息视为高度机密。
安全和隐私措施
作为我们不断致力于确保客户数据安全和隐私的一部分，我们已在所有系统中实施了强有力的措施。我们要赞扬IT部门的John Doe（电子邮件：john.doe@example.com）在增强我们网络安全方面的勤奋工作。未来，我们提醒每个人严格遵守我们的数据保护政策和准则。此外，如果您发现任何潜在的安全风险或事件，请立即向我们专门的团队报告，联系邮箱为security@example.com。
人力资源更新和员工福利
最近，我们迎来了几位为各自部门做出重大贡献的新团队成员。我要表扬Jane Smith（社保号：049-45-5928）在客户服务方面的出色表现。Jane一直受到客户的积极反馈。此外，请记住我们的员工福利计划的开放报名期即将到来。如果您有任何问题或需要帮助，请联系我们的人力资源代表Michael Johnson（电话：418-492-3850，电子邮件：michael.johnson@example.com）。
营销倡议和活动
我们的营销团队一直在积极制定新策略，以提高品牌知名度并推动客户参与。我们要感谢Sarah Thompson（电话：415-555-1234）在管理我们的社交媒体平台方面的杰出努力。Sarah在过去一个月内成功将我们的关注者基数增加了20%。此外，请记住7月15日即将举行的产品发布活动。我们鼓励所有团队成员参加并支持我们公司的这一重要里程碑。
研发项目
在追求创新的过程中，我们的研发部门一直在为各种项目不懈努力。我要赞扬David Rodriguez（电子邮件：david.rodriguez@example.com）在项目负责人角色中的杰出工作。David对我们尖端技术的发展做出了重要贡献。此外，我们希望每个人在7月10日定期举行的研发头脑风暴会议上分享他们的想法和建议，以开展潜在的新项目。
请将此文档中的信息视为最机密，并确保不与未经授权的人员分享。如果您对讨论的话题有任何疑问或顾虑，请随时直接联系我。
感谢您的关注，让我们继续共同努力实现我们的目标。
此致，
Jason Fan
联合创始人兼首席执行官
Psychic
jason@psychic.dev
"""
documents = [Document(page_content=page_content)]

# 2.构建问答转换器并转换
qa_transformer = DoctranQATransformer(
    openai_api_model="deepseek-chat",
)
print("正在转换文档...")
transform_documents = qa_transformer.transform_documents(documents)
print("转换成功!")

# 3.输出内容
for qa in transform_documents[0].metadata.get("questions_and_answers"):
    print("问答数据:", qa)
