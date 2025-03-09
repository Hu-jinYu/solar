# ./core/data_structure/llm_message.py
# 作者：lxfight

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class DialogueMessage:
    """单条对话消息结构"""
    session_id: str      # 会话ID
    role: str            # 消息角色（user/assistant/system）
    content: str         # 消息内容
    timestamp: float     # 时间戳

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "session_id": self.session_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }
    
