import pathlib
import os
import arcade

# Đường dẫn tới thư mục assets
FILE_PATH = pathlib.Path(__file__).parent.absolute()
ROOT_DIR = FILE_PATH.parent
ASSETS_PATH = os.path.join(ROOT_DIR, "assets")

# Cấu hình màn hình
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 630
SCREEN_TITLE = "Rescue The Princess"

# Tỷ lệ scale
TILE_SCALING = 2.0
CHARACTER_SCALING = 0.15
CHARACTER_CHAT_SCALING = 0.3
CHARACTER_CHAT_BUBBLE_SCALING = 0.7

# Vật lý
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 20
PLAYER_WALK_SPEED = 5
PLAYER_RUN_SPEED = 10

# Màu nền mặc định
BACKGROUND_COLOR = arcade.color.AMAZON
