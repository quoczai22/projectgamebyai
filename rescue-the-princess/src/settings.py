import arcade
import os

# Cài đặt chung
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Rescue The Princess"
TILE_SCALING = 2.0

# Đường dẫn gốc (Tự động dò tìm thư mục assets)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
ASSETS_PATH = os.path.join(PROJECT_ROOT, "assets")