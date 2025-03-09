from ui.test import QApplication, QSystemTrayIcon, SystemTrayApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("系统托盘不可用")
        sys.exit(1)

    tray_app = SystemTrayApp(app)
    tray_app.assistant_window.show()  # 显示主窗口
    
    sys.exit(app.exec())