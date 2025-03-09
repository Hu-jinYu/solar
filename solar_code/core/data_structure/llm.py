# ./core/data_structure/llm_message.py
# 作者：lxfight

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class DialogueMessage:
    """单条对话消息结构"""
    session_id: str      # 会话ID
    role: str            # 消息角色（user/assistant/system）
    content: str         # 消息内容

@dataclass
class Session_Title:
    """会话列表和标题名称"""
    session_id: str
    title: str

@dataclass
class dialogue_data:
    """对话数据结构"""
    dialogue_info: Session_Title
    dialogue_messages: List[DialogueMessage]


@dataclass
class personality:
    """AI对话人格"""
    name:str
    system_prompt:str