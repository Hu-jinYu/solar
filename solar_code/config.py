# ./config.py
# 作者：lxfight

import os
import json

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(BASE_DIR)

# 配置文件路径
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'config.json')
# print(CONFIG_PATH)

# 加载配置文件
CONFIG = {}
with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)

# print(CONFIG)