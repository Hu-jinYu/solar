import sys
import os
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from ui.assistant_window import AssistantWindow
from ui.system_tray import SystemTrayApp
from tools import get_logger



if __name__ == "__main__":
    # 确保工作目录为根目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    sys.path.insert(0, current_dir)
    
    logger = get_logger(__name__)
    logger.info("应用初始化开始")
    
    app = QApplication(sys.argv)
    logger.info("QApplication实例创建成功")
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        logger.error("系统托盘不可用，应用将退出")
        sys.exit(1)

    tray_app = SystemTrayApp(app)
    logger.info("系统托盘应用初始化完成")
    
    tray_app.assistant_window.show()
    logger.info("主窗口已显示")
    
    sys.exit(app.exec())
    logger.info("应用正常退出")
