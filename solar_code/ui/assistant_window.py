from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QMenuBar, QLabel
from PyQt6.QtGui import QIcon, QAction
from constants import ICON_PATH  # 直接导入根目录的 constants
from ui.dialogs.settings import SettingsDialog
from ui.dialogs.about import AboutDialog
from tools import get_logger

logger = get_logger(__name__)

class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("初始化主窗口")
        
        self.setWindowTitle("智能助手")
        self.setWindowIcon(QIcon(ICON_PATH))
        
        self.init_menu()
        self.init_ui()
        self.auto_set_geometry()
        logger.info("主窗口初始化完成")

    def auto_set_geometry(self):
        logger.debug("正在设置窗口位置和尺寸")
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.2)
        window_height = int(screen.height() * 0.6)
        x = screen.width() // 5 * 4
        y = screen.height() // 5 * 2
        self.setGeometry(x, y, window_width, window_height)
        logger.debug(f"窗口位置设置为：{x},{y} 尺寸：{window_width}x{window_height}")

    # 定义所有功能方法
    def show_chat(self):
        """显示聊天界面"""
        self.stacked_widget.setCurrentWidget(self.chat_container)
        logger.info("切换到聊天界面")

    def show_music_player(self):
        """显示音乐播放器（占位）"""
        print("音乐播放器功能被触发！")
        # 这里可以添加音乐播放器界面的逻辑

    def show_tools(self):
        """显示工具箱（占位）"""
        print("工具箱功能被触发！")
        # 这里可以添加工具箱界面的逻辑

    def show_games(self):
        """显示小游戏（占位）"""
        print("小游戏功能被触发！")
        # 这里可以添加小游戏界面的逻辑

    def show_live2d(self):
        """显示二次元助手（占位）"""
        print("二次元助手功能被触发！")
        # 这里可以添加二次元助手界面的逻辑

    def show_settings(self):
        """显示系统设置对话框"""
        dialog = SettingsDialog(self)
        dialog.exec()

    def show_about(self):
        """显示关于对话框"""
        dialog = AboutDialog(self)
        dialog.exec()

    def init_menu(self):
        logger.info("初始化菜单栏")
        menu_bar = self.menuBar()
        
        # 功能菜单
        func_menu = menu_bar.addMenu("功能")
        func_menu.addAction("聊天", self.show_chat)
        func_menu.addAction("音乐播放器", self.show_music_player)
        func_menu.addAction("工具箱", self.show_tools)
        func_menu.addAction("小游戏", self.show_games)
        func_menu.addAction("二次元助手", self.show_live2d)

        # 设置菜单
        settings_menu = menu_bar.addMenu("设置")
        settings_menu.addAction("系统设置", self.show_settings)

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction("关于", self.show_about)
        logger.info("菜单栏初始化完成")

    def init_ui(self):
        logger.info("初始化UI组件")
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # 初始化各个功能模块
        self.init_chat()
        # self.init_music_player()  # 暂时注释，待实现
        # self.init_tools()        # 暂时注释，待实现
        # self.init_games()        # 暂时注释，待实现
        # self.init_live2d()       # 暂时注释，待实现
        
        # 初始显示聊天界面
        self.show_chat()
        logger.info("UI组件初始化完成")

    def init_chat(self):
        logger.debug("初始化聊天模块")
        chat_container = QWidget()
        layout = QVBoxLayout(chat_container)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
        
        input_layout = QVBoxLayout()
        self.input_field = QLineEdit(placeholderText="输入问题...")
        send_btn = QPushButton("发送", clicked=self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)
        
        self.stacked_widget.addWidget(chat_container)
        self.chat_container = chat_container  # 保存引用以便切换
        logger.debug("聊天模块初始化完成")

    def send_message(self):
        text = self.input_field.text()
        if text:
            logger.info(f"用户发送消息: {text}")
            self.text_area.append(f"<font color='blue'>用户:</font> {text}")
            self.text_area.append(f"<font color='green'>助手:</font> 正在开发中")
            self.input_field.clear()
            logger.info("消息处理完成")

    def closeEvent(self, event):
        logger.warning("检测到关闭事件，应用将最小化到系统托盘")
        self.hide()
        event.ignore()
