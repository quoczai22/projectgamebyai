import sys
import os

# --- 1. SỬA LỖI ĐƯỜNG DẪN (BẮT BUỘC) ---
# Đoạn này giúp Python tìm thấy các file khác trong thư mục src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# ---------------------------------------

import arcade
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

# --- 2. IMPORT CÁC LEVEL (MÀN CHƠI) ---
from castle_level import CastleView
from cave_level import CaveView
# from day_level import DayView          # (Mở dòng này khi bạn tạo file day_level.py)
# from day_night_level import DayNightView # (Mở dòng này khi bạn tạo file day_night_level.py)

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self):
        """ Khởi tạo game và chọn màn chơi đầu tiên """
        
        # --- 3. CHỌN MAP ĐỂ CHƠI THỬ ---
        # Bạn muốn chơi map nào thì BỎ DẤU # ở đầu dòng đó
        # Và THÊM DẤU # vào dòng map không chơi
        
        start_view = CastleView()   # <--- Map Lâu đài
        
        # -------------------------------

        # Cài đặt và hiển thị màn chơi
        print(f"Đang tải màn chơi: {type(start_view).__name__}")
        start_view.setup()
        self.show_view(start_view)

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()