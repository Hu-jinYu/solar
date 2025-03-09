import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QDialog, QStackedWidget, 
    QMenuBar, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction

# ------------------------- 主窗口类 -------------------------
class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("智能助手")
        self.setWindowIcon(QIcon(r".\resources\icon.ico"))
        self.init_menu()
        self.init_ui()
        self.auto_set_geometry()

    def auto_set_geometry(self):
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.2)
        window_height = int(screen.height() * 0.6)
        x = screen.width() // 5 * 4
        y = screen.height() // 5 * 2
        self.setGeometry(x, y, window_width, window_height)

    def showEvent(self, event):
        self.auto_set_geometry()
        super().showEvent(event)

    def init_menu(self):
        menu_bar = self.menuBar()
        
        # 功能菜单
        func_menu = menu_bar.addMenu("功能")
        func_menu.addAction("聊天", self.show_chat)
        func_menu.addAction("音乐播放器", self.show_music_player)
        func_menu.addAction("工具箱", self.show_tools)
        func_menu.addAction("小游戏", self.show_games)
        func_menu.addAction("二次元助手", self.show_live2d)

        # 陪伴助手菜单（已包含在功能菜单中）
        # companion_menu = menu_bar.addMenu("陪伴助手")  # 移除冗余菜单

        # 设置菜单
        settings_menu = menu_bar.addMenu("设置")
        settings_menu.addAction("系统设置", self.show_settings)

        # 常规帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction("关于", self.show_about)

    def init_ui(self):
        self.stacked_widget = QStackedWidget()  # 使用堆叠窗口管理内容
        self.setCentralWidget(self.stacked_widget)
        
        # 初始化所有功能组件并添加到堆栈
        self.init_chat()
        self.init_music_player()
        self.init_tools()
        self.init_games()
        self.init_live2d()

        # 默认显示聊天界面
        self.show_chat()

    # 各功能初始化方法
    def init_chat(self):
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
        
        self.stacked_widget.addWidget(chat_container)  # 添加到堆栈

    def init_music_player(self):
        music_player = QWidget()
        music_player.setLayout(QVBoxLayout())
        music_player.layout().addWidget(QLabel("音乐播放器功能正在开发中"))
        self.stacked_widget.addWidget(music_player)

    def init_tools(self):
        tools = QWidget()
        tools.setLayout(QVBoxLayout())
        tools.layout().addWidget(QLabel("工具箱功能正在开发中"))
        self.stacked_widget.addWidget(tools)

    def init_games(self):
        games = QWidget()
        games.setLayout(QVBoxLayout())
        games.layout().addWidget(QLabel("小游戏功能正在开发中"))
        self.stacked_widget.addWidget(games)

    def init_live2d(self):
        live2d = QWidget()
        live2d.setLayout(QVBoxLayout())
        live2d.layout().addWidget(QLabel("二次元助手功能正在开发中"))
        self.stacked_widget.addWidget(live2d)

    # 菜单栏动作响应方法
    def show_chat(self): 
        self.stacked_widget.setCurrentIndex(0)
    
    def show_music_player(self): 
        self.stacked_widget.setCurrentIndex(1)
    
    def show_tools(self): 
        self.stacked_widget.setCurrentIndex(2)
    
    def show_games(self): 
        self.stacked_widget.setCurrentIndex(3)
    
    def show_live2d(self): 
        self.stacked_widget.setCurrentIndex(4)

    def show_settings(self):
        SettingsDialog(self).exec()

    def show_about(self):
        AboutDialog(self).exec()

    def send_message(self):
        text = self.input_field.text()
        if text:
            self.text_area.append(f"<font color='blue'>用户:</font> {text}")
            self.text_area.append(f"<font color='green'>助手:</font> 正在开发中")
            self.input_field.clear()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

# ------------------------- 系统设置对话框 -------------------------
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setWindowIcon(QIcon(r".\resources\icon.ico"))
        self.init_ui()
        self.auto_set_geometry()

    def auto_set_geometry(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.resize(300, 200)
        qr = self.frameGeometry()
        cp = screen.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()
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
        self.resize(300, 200)
        qr = self.frameGeometry()
        cp = QApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("智能助手 v1.0"))
        layout.addWidget(QLabel("基于PyQt6和LLM驱动"))
        self.setLayout(layout)

# ------------------------- 系统托盘管理 -------------------------
class SystemTrayApp:
    def __init__(self, app):
        self.app = app
        icon_path = r".\resources\icon.ico"
        self.icon = QIcon(icon_path)
        if self.icon.isNull():
            print(f"图标路径无效: {icon_path}")
            sys.exit(1)
        self.tray_icon = QSystemTrayIcon(self.icon, parent=app)
        
        self.tray_icon.activated.connect(
            lambda reason: self.handle_tray_activation(reason)
        )
        
        self.create_menu()
        self.assistant_window = AssistantWindow()
        self.tray_icon.show()
        
    def handle_tray_activation(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_window()
        elif reason == QSystemTrayIcon.ActivationReason.Context:
            pass

    def create_menu(self):
        menu = QMenu()
        menu.addAction("显示助手", self.show_window)
        menu.addAction("退出程序", self.exit_app)
        self.tray_icon.setContextMenu(menu)

    def show_window(self):
        self.assistant_window.showNormal()
        self.assistant_window.activateWindow()
        self.assistant_window.raise_()

    def exit_app(self):
        self.app.quit()

