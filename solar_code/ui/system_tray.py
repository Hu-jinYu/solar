from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from ui.assistant_window import AssistantWindow  # 导入AssistantWindow
from config import ICON_PATH # 导入图标路径
from tools import get_logger
import sys
logger = get_logger(__name__)

class SystemTrayApp:
    def __init__(self, app):
        logger.info("初始化系统托盘应用")
        self.app = app
        self.assistant_window = AssistantWindow()

        # 加载图标
        try:
            self.icon = QIcon(ICON_PATH)
            if self.icon.isNull():
                raise FileNotFoundError(f"图标路径无效: {ICON_PATH}")
        except Exception as e:
            logger.error(f"图标加载失败: {e}")
            sys.exit(1)
        
        # 创建系统托盘图标实例
        self.tray_icon = QSystemTrayIcon(self.icon, self.app)  # 传递图标和应用实例
        self.tray_icon.show()  # 显示托盘图标
        
        # 创建右键菜单
        self.menu = QMenu()
        self.action_show = QAction("显示主窗口")
        self.action_exit = QAction("退出")
        self.menu.addAction(self.action_show)
        self.menu.addAction(self.action_exit)
        
        # 设置菜单到托盘图标
        self.tray_icon.setContextMenu(self.menu)
        
        # 连接信号
        self.action_show.triggered.connect(self.show_window)
        self.action_exit.triggered.connect(self.exit_app)

    def show_window(self):
        self.assistant_window.show()  # 确保有assistant_window实例

    def exit_app(self):
        self.app.quit()
