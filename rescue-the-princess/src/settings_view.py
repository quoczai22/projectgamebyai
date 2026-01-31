import arcade
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_PATH

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # --- 1. GIAO DIỆN (Giữ nguyên) ---
        self.ui_list = arcade.SpriteList()
        image_path = os.path.join(ASSETS_PATH, "images", "menu_view.png")
        if os.path.exists(image_path):
            try:
                bg_sprite = arcade.Sprite(image_path)
                bg_sprite.center_x = SCREEN_WIDTH / 2
                bg_sprite.center_y = SCREEN_HEIGHT / 2
                bg_sprite.width = SCREEN_WIDTH
                bg_sprite.height = SCREEN_HEIGHT
                self.ui_list.append(bg_sprite)
            except Exception as e:
                print(f"Lỗi ảnh nền: {e}")

        # --- 2. FONT (Giữ nguyên) ---
        font_path = os.path.join(ASSETS_PATH, "fonts", "PressStart2P-Regular.ttf")
        self.pixel_font = "Arial"
        if os.path.exists(font_path):
            arcade.load_font(font_path)
            self.pixel_font = "Press Start 2P"

        # --- QUAN TRỌNG: KHÔNG LOAD NHẠC Ở ĐÂY NỮA ---
        # Chúng ta sẽ dùng trực tiếp self.window.bg_player được tạo bên Menu

    def on_show_view(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)
        
        # Kiểm tra xem biến nhạc đã được khởi tạo bên Menu chưa (đề phòng lỗi)
        if not hasattr(self.window, "music_volume"):
            self.window.music_volume = 0.5
        if not hasattr(self.window, "is_muted"):
            self.window.is_muted = False

    def on_draw(self):
        self.clear()
        self.ui_list.draw()

        # Tiêu đề
        arcade.draw_text("SETTINGS",
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2+100,
                         arcade.color.GOLD, 30,
                         font_name=self.pixel_font,
                         anchor_x="center", bold=True)

        # --- HIỂN THỊ TRẠNG THÁI (Lấy từ self.window) ---
        # Lấy giá trị hiện tại từ cửa sổ game
        current_vol = self.window.music_volume
        is_muted = self.window.is_muted

        # Vẽ thanh Volume
        bar_count = int(current_vol * 10) # 0.5 -> 5 vạch
        bar_str = "|" * bar_count + "." * (10 - bar_count)
        
        if is_muted: 
            status_text = "MUTED"
            color = arcade.color.RED
            bar_display = "[MUTED]"
        else:
            status_text = f"VOL: {int(current_vol * 100)}%"
            color = arcade.color.WHITE
            bar_display = f"[{bar_str}]"

        arcade.draw_text(status_text,
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                         color, 16,
                         font_name=self.pixel_font,
                         anchor_x="center")
        
        arcade.draw_text(bar_display,
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40,
                         arcade.color.GREEN if not is_muted else arcade.color.RED,
                         16,
                         font_name=self.pixel_font,
                         anchor_x="center")

        # Hướng dẫn
        arcade.draw_text("UP/DOWN: Volume   M: Mute   ESC: Back",
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100,
                         arcade.color.LIGHT_GRAY, 10,
                         font_name=self.pixel_font,
                         anchor_x="center")

    def on_key_press(self, key, modifiers):
        # Lấy player nhạc đang chạy từ Window
        player = getattr(self.window, "bg_player", None)

        if key == arcade.key.M:
            # Đảo trạng thái Mute của Window
            self.window.is_muted = not self.window.is_muted
            
            # Cập nhật ngay lập tức cho player
            if player:
                player.volume = 0.0 if self.window.is_muted else self.window.music_volume

        elif key == arcade.key.UP:
            if not self.window.is_muted and self.window.music_volume < 1.0:
                self.window.music_volume = min(1.0, self.window.music_volume + 0.1)
                # Cập nhật volume thật
                if player:
                    player.volume = self.window.music_volume
                    
        elif key == arcade.key.DOWN:
            if not self.window.is_muted and self.window.music_volume > 0.0:
                self.window.music_volume = max(0.0, self.window.music_volume - 0.1)
                # Cập nhật volume thật
                if player:
                    player.volume = self.window.music_volume
                    
        elif key == arcade.key.ESCAPE:
            # Quay lại Menu (Menu sẽ tự nhận biết nhạc đang chạy nên không phát lại)
            from menu_view import MenuView 
            self.window.show_view(MenuView())