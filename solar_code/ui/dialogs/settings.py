from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from config import ICON_PATH  # 直接导入根目录的 constants
from tools import get_logger
from PyQt6.QtGui import QIcon


logger = get_logger(__name__)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("初始化系统设置对话框")
        self.setWindowTitle("系统设置")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.init_ui()
        self.auto_set_geometry()
        logger.info("系统设置对话框初始化完成")

    def auto_set_geometry(self):
        logger.debug("设置系统设置对话框位置")
        screen = self.screen().availableGeometry()
        self.resize(300, 200)
        qr = self.frameGeometry()
        qr.moveCenter(screen.center())
        self.move(qr.topLeft())
        logger.debug(f"对话框位置设置为：{qr.x()},{qr.y()}")

    def init_ui(self):
        logger.debug("构建系统设置界面布局")
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("保存设置"))
        self.setLayout(layout)
        logger.debug("系统设置界面布局构建完成")
