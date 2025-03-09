from ui.test import QApplication, QSystemTrayIcon, SystemTrayApp
import sys
from config import CONFIG
from tools import get_logger

if __name__ == "__main__":
    logger = get_logger(__name__)
    app = QApplication(sys.argv)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        logger.error("系统托盘不可用")
        sys.exit(1)

    tray_app = SystemTrayApp(app)
    tray_app.assistant_window.show()  # 显示主窗口
    
    sys.exit(app.exec())