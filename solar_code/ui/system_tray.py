from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
from ui.assistant_window import AssistantWindow  # 导入AssistantWindow
from config import ICON_PATH # 导入图标路径
from tools import get_logger
import sysimport sys


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

        # ✅ 绑定托盘点击事件（左键）
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

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

    # def show_window(self):
    #     self.assistant_window.show()  # 确保有assistant_window实例

    # def exit_app(self):
    #     self.app.quit()
    def on_tray_icon_activated(self, reason: QSystemTrayIcon.ActivationReason):
        """处理托盘图标点击事件"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:  # 左键点击
            self.show_window()  # 调用显示窗口方法
    def show_window(self):
        """显示/隐藏主窗口"""
        if self.assistant_window.isHidden():
            self.assistant_window.show()
            self.assistant_window.activateWindow()  # 激活窗口到最前端
        else:
            self.assistant_window.hide()
    def exit_app(self):
        self.assistant_window.close()
        self.tray_icon.hide()
        self.app.quit()