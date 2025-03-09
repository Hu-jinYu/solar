import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  # 此时是根目录路径
RESOURCE_DIR = os.path.join(PROJECT_ROOT, "resources")
ICON_PATH = os.path.join(RESOURCE_DIR, "icon.ico")

print(f"项目根目录：{PROJECT_ROOT}")
print(f"资源目录：{RESOURCE_DIR}")
print(f"图标路径：{ICON_PATH}")
