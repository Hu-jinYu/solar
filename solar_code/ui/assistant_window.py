from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QMenuBar, QLabel
from PyQt6.QtGui import QIcon, QAction
from config import ICON_PATH
from ui.dialogs.settings import SettingsDialog
from ui.dialogs.about import AboutDialog
from tools import get_logger

logger = get_logger(__name__)

class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._init_components()
        logger.info("主窗口初始化完成")

    def _setup_window(self) -> None:
        """设置窗口基本属性"""
        logger.info("设置窗口基本属性")
        self.setWindowTitle("智能助手")
        self.setWindowIcon(QIcon(ICON_PATH))
        self._auto_set_geometry()
    def _auto_set_geometry(self) -> None:
        """根据屏幕尺寸自动设置窗口位置和大小"""
        logger.debug("正在设置窗口位置和尺寸")
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.2)
        window_height = int(screen.height() * 0.6)
        x = screen.width() // 5 * 4
        y = screen.height() // 5 * 2
        self.setGeometry(x, y, window_width, window_height)
        logger.debug(f"窗口位置设置为：{x},{y} 尺寸：{window_width}x{window_height}")

    def _init_components(self) -> None:
        """初始化所有组件"""
        self._init_menu()
        self._init_ui()

    def _init_menu(self) -> None:
        """初始化菜单栏"""
        logger.info("初始化菜单栏")
        menu_bar = self.menuBar()
        
        # 功能菜单
        func_menu = menu_bar.addMenu("功能")
        self._add_menu_actions(func_menu, {
            "聊天": self.show_chat,
            "音乐播放器": self.show_music_player,
            "工具箱": self.show_tools,
            "小游戏": self.show_games,
            "二次元助手": self.show_live2d
        })
        # 设置菜单
        settings_menu = menu_bar.addMenu("设置")
        self._add_menu_actions(settings_menu, {
            "系统设置": self.show_settings
        })
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        self._add_menu_actions(help_menu, {
            "关于": self.show_about
        })
        logger.info("菜单栏初始化完成")

    def _add_menu_actions(self, menu: QMenuBar, actions: dict[str, callable]) -> None:
        """为菜单添加多个动作"""
        for text, callback in actions.items():
            menu.addAction(text, callback)
    
    def _init_ui(self) -> None:
        """初始化UI组件"""
        logger.info("初始化UI组件")
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # 初始化功能模块
        self._init_chat_module()
        # 其他模块初始化可以在这里添加
        
        # 初始显示聊天界面
        self.show_chat()
        logger.info("UI组件初始化完成")

    def _init_chat_module(self) -> None:
        """初始化聊天模块"""
        logger.debug("初始化聊天模块")
        self.chat_container = self._create_chat_widget()
        self.stacked_widget.addWidget(self.chat_container)
        logger.debug("聊天模块初始化完成")
    
    def _create_chat_widget(self) -> QWidget:
        """创建聊天界面组件"""
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # 消息显示区域
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
        
        # 输入区域
        input_layout = QVBoxLayout()
        self.input_field = QLineEdit(placeholderText="输入问题...")
        # 设置回车键发送消息
        self.input_field.returnPressed.connect(self._handle_message)
        
        send_btn = QPushButton("发送", clicked=self._handle_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        layout.addLayout(input_layout)
        
        return container

    def _handle_message(self) -> None:
        """处理用户发送的消息"""
        text = self.input_field.text().strip()
        if not text:
            return
            
        logger.info(f"用户发送消息: {text}")
        self._display_user_message(text)
        self._display_assistant_response("正在开发中")
        self.input_field.clear()
        logger.info("消息处理完成")
    def _display_user_message(self, text: str) -> None:
        """显示用户消息"""
        self.text_area.append(f"<font color='blue'>用户:</font> {text}")
    def _display_assistant_response(self, text: str) -> None:
        """显示助手回复"""
        self.text_area.append(f"<font color='green'>助手:</font> {text}")
    # 功能切换方法
    def show_chat(self) -> None:
        """显示聊天界面"""
        self.stacked_widget.setCurrentWidget(self.chat_container)
        logger.info("切换到聊天界面")
    def show_music_player(self) -> None:
        """显示音乐播放器（占位）"""
        logger.info("音乐播放器功能被触发")
        # 这里可以添加音乐播放器界面的逻辑
    def show_tools(self) -> None:
        """显示工具箱（占位）"""
        logger.info("工具箱功能被触发")
        # 这里可以添加工具箱界面的逻辑
    def show_games(self) -> None:
        """显示小游戏（占位）"""
        logger.info("小游戏功能被触发")
        # 这里可以添加小游戏界面的逻辑
    def show_live2d(self) -> None:
        """显示二次元助手（占位）"""
        logger.info("二次元助手功能被触发")
        # 这里可以添加二次元助手界面的逻辑
    def show_settings(self) -> None:
        """显示系统设置对话框"""
        logger.info("打开系统设置")
        SettingsDialog(self).exec()
    def show_about(self) -> None:
        """显示关于对话框"""
        logger.info("打开关于对话框")
        AboutDialog(self).exec()
    def closeEvent(self, event) -> None:
        """处理窗口关闭事件"""
        logger.warning("检测到关闭事件，应用将最小化到系统托盘")
        self.hide()
        event.ignore()
