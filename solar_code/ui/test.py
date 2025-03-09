import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QDialog, QTabWidget, 
    QMenuBar, QGroupBox, QComboBox, QListWidget, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction

# ------------------------- 主窗口类 -------------------------
class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能助手")  # 设置窗口标题
        self.setWindowIcon(QIcon(r".\resources\icon.ico"))  # 设置窗口图标
        self.init_menu()               # 初始化菜单栏
        self.init_ui()                 # 初始化主界面布局
        self.init_plugins()            # 初始化插件系统
        self.auto_set_geometry()       # 自动设置窗口大小和位置

    def auto_set_geometry(self):
        """根据屏幕分辨率自动调整窗口位置和尺寸"""
        screen = QApplication.primaryScreen().availableGeometry()  # 获取主屏幕可用区域
        window_width = int(screen.width() * 0.6)  # 窗口宽度为屏幕的60%
        window_height = int(screen.height() * 0.7)  # 窗口高度为屏幕的70%
        x = (screen.width() - window_width) // 2    # 居中计算x坐标
        y = (screen.height() - window_height) // 2  # 居中计算y坐标
        self.setGeometry(x, y, window_width, window_height)  # 设置窗口位置和大小

    def showEvent(self, event):
        """窗口显示时重新计算位置（例如分辨率变化时）"""
        self.auto_set_geometry()
        super().showEvent(event)

    def init_menu(self):
        """初始化菜单栏"""
        menu_bar = self.menuBar()
        
        # 功能菜单
        func_menu = menu_bar.addMenu("功能")
        func_menu.addAction("聊天", self.show_chat)          # 聊天功能菜单项
        func_menu.addAction("音乐播放器", self.show_music_player)  # 音乐播放器菜单项
        func_menu.addAction("工具箱", self.show_tools)        # 工具箱菜单项
        func_menu.addAction("小游戏", self.show_games)        # 小游戏菜单项

        # 陪伴助手菜单
        companion_menu = menu_bar.addMenu("陪伴助手")
        companion_menu.addAction("二次元助手", self.show_live2d)  # 二次元助手菜单项

        # 设置菜单
        settings_menu = menu_bar.addMenu("设置")
        settings_menu.addAction("系统设置", self.show_settings)  # 系统设置菜单项

        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction("关于", self.show_about)          # 关于对话框菜单项

    def init_ui(self):
        """初始化主界面布局（标签页容器）"""
        self.tab_widget = QTabWidget()  # 创建标签页容器
        self.setCentralWidget(self.tab_widget)  # 设置为中心部件
        
        # 初始化各个功能标签页
        self.init_chat_tab()        # 聊天界面
        self.init_music_player()    # 音乐播放器界面
        self.init_tools()           # 工具箱界面
        self.init_games()           # 小游戏界面
        self.init_live2d()          # 二次元助手界面
        self.init_plugins_tab()     # 插件管理界面

    def init_plugins(self):
        """初始化插件系统"""
        self.plugins = {}  # 存储插件实例的字典
        self.load_plugin("天气插件", WeatherPlugin)  # 加载天气插件示例

    def load_plugin(self, name, plugin_class):
        """动态加载插件到标签页"""
        plugin = plugin_class(self)  # 创建插件实例
        self.tab_widget.addTab(plugin, name)  # 添加到标签页
        self.plugins[name] = plugin  # 记录插件引用

    def init_chat_tab(self):
        """初始化聊天功能标签页"""
        chat_container = QWidget()  # 创建容器部件
        layout = QVBoxLayout(chat_container)  # 垂直布局
        
        # 聊天记录显示区域
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)  # 设置为只读
        layout.addWidget(self.text_area)
        
        # 输入区域布局
        input_layout = QVBoxLayout()  
        self.input_field = QLineEdit(placeholderText="输入问题...")
        send_btn = QPushButton("发送", clicked=self.send_message)  # 绑定发送按钮
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)  # 将输入布局添加到主布局
        self.tab_widget.addTab(chat_container, "聊天")  # 添加到标签页

    # 其他标签页初始化方法（结构类似）
    def init_music_player(self):
        self.music_player = MusicPlayerWindow()
        self.tab_widget.addTab(self.music_player, "音乐播放器")

    def init_tools(self):
        self.tools_window = ToolsWindow()
        self.tab_widget.addTab(self.tools_window, "工具箱")

    def init_games(self):
        self.games_window = GamesWindow()
        self.tab_widget.addTab(self.games_window, "小游戏")

    def init_live2d(self):
        self.live2d = Live2DWindow()
        self.tab_widget.addTab(self.live2d, "二次元助手")

    def init_plugins_tab(self):
        """初始化插件管理标签页"""
        plugin_container = QWidget()
        layout = QVBoxLayout(plugin_container)
        layout.addWidget(QLabel("插件管理"))
        self.tab_widget.addTab(plugin_container, "插件")

    # 菜单栏动作响应方法
    def show_chat(self):    self.tab_widget.setCurrentIndex(0)
    def show_music_player(self): self.tab_widget.setCurrentIndex(1)
    def show_tools(self):       self.tab_widget.setCurrentIndex(2)
    def show_games(self):       self.tab_widget.setCurrentIndex(3)
    def show_live2d(self):      self.tab_widget.setCurrentIndex(4)

    def show_settings(self):
        """显示系统设置对话框"""
        SettingsDialog(self).exec()  # 显示模态对话框

    def show_about(self):
        """显示关于对话框"""
        AboutDialog(self).exec()

    def send_message(self):
        """处理用户发送消息"""
        text = self.input_field.text()
        if text:
            self.text_area.append(f"<font color='blue'>用户:</font> {text}")
            response = "助手：正在开发中"  # 临时响应
            self.text_area.append(f"<font color='green'>助手:</font> {response}")
            self.input_field.clear()

    def closeEvent(self, event):
        """重写关闭事件：隐藏窗口而非退出程序"""
        self.hide()
        event.ignore()

# ------------------------- 基础功能窗口 -------------------------
class BaseFunctionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()  # 创建基础布局
        self.setLayout(self.layout)  # 设置布局
        self.init_ui()  # 初始化基础内容

    def init_ui(self):
        """添加默认的"功能正在开发中"提示"""
        self.layout.addWidget(QLabel("功能正在开发中"))

# ------------------------- 音乐播放器 -------------------------
class MusicPlayerWindow(BaseFunctionWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_music_ui()

    def init_music_ui(self):
        """初始化音乐播放器界面"""
        self.playlist = QListWidget()  # 歌曲列表
        play_btn = QPushButton("播放", clicked=self.play_music)  # 播放按钮
        
        # 直接使用基类的布局添加部件
        self.layout.addWidget(QLabel("音乐播放器"))
        self.layout.addWidget(self.playlist)
        self.layout.addWidget(play_btn)

    def play_music(self):
        """播放音乐（待实现）"""
        print("播放音乐未实现")

# ------------------------- 工具箱 -------------------------
class ToolsWindow(BaseFunctionWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_tools()

    def init_tools(self):
        """初始化工具箱界面"""
        weather_box = QGroupBox("天气查询")  # 分组框
        
        # 天气查询布局
        weather_layout = QVBoxLayout()
        self.city_input = QLineEdit(placeholderText="城市名")
        get_weather_btn = QPushButton("查询", clicked=self.get_weather)
        
        weather_layout.addWidget(self.city_input)
        weather_layout.addWidget(get_weather_btn)
        weather_box.setLayout(weather_layout)
        
        # 添加到基类布局
        self.layout.addWidget(weather_box)
        self.layout.addWidget(QLabel("工具功能正在开发中"))

    def get_weather(self):
        """获取天气（待集成接口）"""
        print(f"获取{self.city_input.text()}天气")

# ------------------------- 小游戏 -------------------------
class GamesWindow(BaseFunctionWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_games()

    def init_games(self):
        """初始化小游戏界面"""
        self.game_choice = QComboBox()
        self.game_choice.addItems(["猜数字", "井字棋", "文字冒险"])
        start_btn = QPushButton("开始游戏", clicked=self.start_game)
        
        # 添加到基类布局
        self.layout.addWidget(self.game_choice)
        self.layout.addWidget(start_btn)

    def start_game(self):
        """开始游戏（待实现）"""
        game = self.game_choice.currentText()
        print(f"开始游戏: {game}")

# ------------------------- 二次元助手 -------------------------
class Live2DWindow(BaseFunctionWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_live2d()

    def init_live2d(self):
        """初始化二次元助手界面"""
        self.layout.addWidget(QLabel("Live2D模型加载中..."))

# ------------------------- 插件系统 -------------------------
class BasePlugin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_plugin_ui()

    def init_plugin_ui(self):
        """默认插件界面"""
        self.layout.addWidget(QLabel("插件功能正在开发中"))

class WeatherPlugin(BasePlugin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_weather_ui()

    def init_weather_ui(self):
        """初始化天气插件界面"""
        self.city_input = QLineEdit(placeholderText="输入城市")
        get_weather_btn = QPushButton("获取天气", clicked=self.fetch_weather)
        
        # 添加到布局
        self.layout.addWidget(self.city_input)
        self.layout.addWidget(get_weather_btn)

    def fetch_weather(self):
        """获取天气数据（待集成接口）"""
        city = self.city_input.text()
        print(f"获取{city}天气数据...")

# ------------------------- 系统设置对话框 -------------------------
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(r".\resources\icon.ico"))
        self.init_ui()
        self.auto_set_geometry()

    def auto_set_geometry(self):
        """自动设置对话框位置和大小"""
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.4)
        window_height = int(screen.height() * 0.5)
        x = (screen.width() - window_width) // 2
        y = (screen.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

    def showEvent(self, event):
        self.auto_set_geometry()
        super().showEvent(event)

    def init_ui(self):
        """初始化设置界面布局"""
        layout = QVBoxLayout()
        
        # API设置分组
        api_group = QGroupBox("API设置")
        api_layout = QVBoxLayout()
        self.weather_api_key = QLineEdit(placeholderText="天气API密钥")
        
        api_layout.addWidget(QLabel("天气API密钥"))
        api_layout.addWidget(self.weather_api_key)
        api_group.setLayout(api_layout)
        
        layout.addWidget(api_group)
        layout.addWidget(QPushButton("保存设置"))
        self.setLayout(layout)

# ------------------------- 关于对话框 -------------------------
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setWindowIcon(QIcon(r".\resources\icon.ico"))
        self.init_ui()
        self.auto_set_geometry()

    def auto_set_geometry(self):
        """自动设置关于对话框大小并居中"""
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(300, 200)
        self.center()

    def center(self):
        """窗口居中显示"""
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showEvent(self, event):
        self.center()
        super().showEvent(event)

    def init_ui(self):
        """初始化关于界面布局"""
        layout = QVBoxLayout()
        layout.addWidget(QLabel("智能助手 v1.0"))
        layout.addWidget(QLabel("基于PyQt6和LLM驱动"))
        self.setLayout(layout)

# ------------------------- 系统托盘管理 -------------------------
class SystemTrayApp:
    def __init__(self, app):
        self.app = app
        icon_path = r".\resources\icon.ico"  # 确保路径正确
        self.icon = QIcon(icon_path)
        if self.icon.isNull():
            print(f"图标路径无效: {icon_path}")
            sys.exit(1)
        self.tray_icon = QSystemTrayIcon(self.icon, parent=app)
        
        # 新增：连接托盘图标的单击事件到显示窗口
        self.tray_icon.activated.connect(self.show_window)  # 处理单击托盘图标
        
        self.create_menu()
        self.assistant_window = AssistantWindow()
        self.tray_icon.show()
    def create_menu(self):
        menu = QMenu()
        menu.addAction("显示助手", self.show_window)  # 右键菜单显示
        menu.addAction("退出程序", self.exit_app)
        self.tray_icon.setContextMenu(menu)
    def show_window(self, reason=QSystemTrayIcon.ActivationReason.Trigger):  # 新增参数默认值
        """显示主窗口并激活"""
        self.assistant_window.showNormal()  # 确保窗口正常显示（非最小化）
        self.assistant_window.activateWindow()  # 让窗口获得焦点
        self.assistant_window.raise_()  # 确保窗口在最上层
    def exit_app(self):
        self.app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("系统托盘不可用")
        sys.exit(1)

    tray_app = SystemTrayApp(app)
    tray_app.assistant_window.show()  # 显示主窗口
    
    sys.exit(app.exec())
