from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class memorandum:
    """备忘录"""
    title: str                  # 备忘标题
    content: str                # 备忘内容
    memo_type: str               # （单次/循环：每天、每周、每月、每年（生日等）、工作日）
    reminder_time: float        # 提醒时间
    state: str                  # （未完成/已完成/已过期）
    timestamp: float            # 时间戳

