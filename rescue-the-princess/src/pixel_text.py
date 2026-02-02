import arcade
import os
from settings import ASSETS_PATH

# Tên font chuẩn trong file .ttf
FONT_NAME = "SVN-Determination Sans" 

# Load font
font_path = os.path.join(ASSETS_PATH, "fonts", "SVN-Determination Sans.ttf")
if os.path.exists(font_path):
    arcade.load_font(font_path)
else:
    FONT_NAME = "Arial" 

class PixelText(arcade.Text):
    """Class vẽ chữ Pixel tiện lợi"""
    def __init__(self, text, x, y, color=arcade.color.WHITE, size=12, anchor_x="left", anchor_y="baseline", bold=False, width=0, multiline=False):
        super().__init__(
            text=str(text),
            x=x,          # <--- SỬA: Đổi start_x thành x
            y=y,          # <--- SỬA: Đổi start_y thành y
            color=color,
            font_size=size,
            font_name=FONT_NAME,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            bold=bold,
            width=width,
            multiline=multiline
        )