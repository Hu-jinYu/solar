# ./config.py
# 作者：lxfight

import os
import json

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 配置文件路径
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'config.json')

# 配置文件
CONFIG = {}
with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  # 此时是根目录路径
RESOURCE_DIR = os.path.join(PROJECT_ROOT, "resources")
ICON_PATH = os.path.join(RESOURCE_DIR, "icon.ico")