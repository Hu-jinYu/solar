# ./core/llm/llm_openai.py
# 作者：lxfight

from openai import OpenAI
import json
from typing import List, Dict, Optional
from core import LLM_Base
from config import CONFIG

class LLM_OpenAI(LLM_Base):
    def __init__(self, api_base:str, api_key:str, model: str):
        """
        初始化大模型调用类
        :param api_base: OpenAI API地址
        :param api_key: OpenAI API密钥
        :param model: 要使用的模型名称
        """
        self.model = model
        self.client = OpenAI(
                    base_url=api_base,
                    api_key=api_key
                )

    def chat_completion(
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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def chat_completion_with_function(
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
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            functions=functions,
            function_call=function_call,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        message = response.choices[0].message
        result = {
            "content": message.content,
            "function_call": None
        }
        if message.function_call:
            result["function_call"] = {
                "name": message.function_call.name,
                "arguments": json.loads(message.function_call.arguments)
            }
        return result
    
    def stream_chat_completion(
        self,
        messages: List[Dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ):
        """
        流式对话调用
        :param messages: 消息列表
        :param temperature: 温度系数
        :param max_tokens: 最大token数
        :return: 生成器，逐块返回内容
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    @staticmethod
    def get_available_models() -> List[str]:
        """获取所有可用模型列表"""
        models = []
        for llm_config in CONFIG["llm"]:
            models.extend(llm_config["model_name"])
        return list(set(models))
    
