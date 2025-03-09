from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton  # 新增 QPushButton 导入（如果需要关闭按钮）
from PyQt6.QtGui import QIcon  # 新增导入 QIcon
from PyQt6.QtCore import Qt  # 如果需要对齐等 Qt 属性，可导入
from config import ICON_PATH  # 直接导入根目录的 constants
from tools import get_logger

logger = get_logger(__name__)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("初始化关于对话框")
        self.setWindowTitle("关于")
        self.setWindowIcon(QIcon(ICON_PATH))  # 此处需要 QIcon
        self.init_ui()
        self.auto_set_geometry()
        logger.info("关于对话框初始化完成")

    def auto_set_geometry(self):
        logger.debug("设置关于对话框位置")
        self.resize(300, 200)
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        logger.debug(f"关于对话框位置设置为：{qr.x()},{qr.y()}")

    def init_ui(self):
        logger.debug("构建关于对话框布局")
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # 添加边距
        
        title_label = QLabel("智能助手 v1.0")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        version_label = QLabel("基于 PyQt6 和 LLM 驱动")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 文字居中
        layout.addWidget(version_label)
        
        # 可选：添加关闭按钮
        close_btn = QPushButton("关闭", clicked=self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        logger.debug("关于对话框布局构建完成")
