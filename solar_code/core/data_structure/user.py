from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class birthday:
    """生日信息"""
    year: int
    month: int
    day: int

@dataclass
class User:
    """用户信息"""
    user_name: str
    gender: str
    birthday: birthday

