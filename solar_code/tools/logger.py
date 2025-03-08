# ./solar_code/tools/logger.py
# 作者：lxfight

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from config import BASE_DIR

def get_logger(name):
    """
    获取指定名称的logger实例
    """
    # 初始化配置（只执行一次）
    if not hasattr(get_logger, 'initialized'):
        # 创建日志目录
        log_dir = os.path.join(BASE_DIR, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "application.log")
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        # 创建文件处理器（每天滚动，保留7天）
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        # 配置根logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        get_logger.initialized = True
    return logging.getLogger(name)

# 使用示例
# from logger import get_logger
# logger = get_logger(__name__)
# def test():
#     logger.info("This is a log from module1")