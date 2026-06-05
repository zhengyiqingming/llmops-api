#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2026/1/13 9:53
@Author : 751363075@qq.com
@File : 1.缓冲窗口记忆示例.py
"""
from operator import itemgetter
import dotenv
import tiktoken
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationTokenBufferMemory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


# 需要创建一个新的类，实现自己的token计数逻辑，继承 ChatOpenAI，该类提供给deepseek模型使用
class CustomChatOpenAI(ChatOpenAI):
    def get_num_tokens_from_messages(self, messages):
        """
        为使用 cl100k_base 分词器的模型（如GPT, DeepSeek-chat）计算消息的token数量。
        参考OpenAI官方的计算规则：https://platform.openai.com/docs/guides/text-generation/managing-tokens
        """
        # 指定编码
        model = "cl100k_base"
        try:
            encoding = tiktoken.get_encoding(model)
        except KeyError:
            # 如果找不到指定编码，使用 cl100k_base 作为后备
            encoding = tiktoken.get_encoding("cl100k_base")

        # OpenAI格式消息的token计算规则
        tokens_per_message = 4  # 每条消息有4个token的开销
        tokens_per_name = -1  # 如果消息中有'name'字段，每个name减1个token（因为角色字段会被省略）
        num_tokens = 0

        for message in messages:
            num_tokens += tokens_per_message
            # 遍历消息的每个字段（如content, role, name等）
            for value in message.content:
                num_tokens += len(encoding.encode(value))

        # 添加模型回复时的开场token（例如 assistant: ）
        num_tokens += 3
        return num_tokens


# 1.创建提示模板&记忆
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是deepseek开发的聊天机器人，请根据对应的上下文回复用户问题"),
    MessagesPlaceholder("history"),  # 需要的history是一个列表
    ("human", "{query}"),
])
memory = ConversationTokenBufferMemory(
    return_messages=True,  # 返回消息列表信息
    input_key="query",
    llm=CustomChatOpenAI(model="deepseek-chat"),
)

# 2.创建大语言模型
llm = CustomChatOpenAI(model="deepseek-chat")

# 3.构建链应用
chain = RunnablePassthrough.assign(
    history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
) | prompt | llm | StrOutputParser()

# 4.死循环构建对话命令行
while True:
    query = input("Human: ")

    if query == "q":
        exit(0)

    chain_input = {"query": query, "language": "中文"}

    response = chain.stream(chain_input)
    print("AI:", flush=True, end="")
    output = ""
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end="")
    memory.save_context(chain_input, {"output": output})
    print("")
    print("history: ", memory.load_memory_variables({}))
