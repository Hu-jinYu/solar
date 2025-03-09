# ./core/llm/llm_base.py
# 作者：lxfight

from openai import AsyncOpenAI
import json
from typing import List, Dict, Optional, AsyncGenerator
from abc import ABC, abstractmethod

class LLM_Base:
    # LLM_Base类是一个抽象基类，定义了一个接口，包含了chat_completion、chat_completion_with_function、stream_chat_completion三个方法。
    # LLM_Base类的子类需要实现这三个方法。
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """
        纯对话调用
        :param messages: 消息列表
        :param temperature: 温度系数
        :param max_tokens: 最大token数
        :return: 模型生成的文本内容
        """
        pass

    @abstractmethod
    async def chat_completion_with_function(
        self,
        messages: List[Dict],
        functions: List[Dict],
        function_call: Optional[str] = "auto",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> Dict:
        """
        支持函数回调的调用
        :param messages: 消息列表
        :param functions: 函数定义列表
        :param function_call: 函数调用模式（auto/function_name）
        :param temperature: 温度系数
        :param max_tokens: 最大token数
        :return: 包含内容和函数调用的字典
        """
        pass

    async def stream_chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    )-> AsyncGenerator[str, None]:
        """
        流式对话调用
        :param messages: 消息列表
        :param temperature: 温度系数
        :param max_tokens: 最大token数
        :return: 生成器，逐块返回内容
        """
        pass