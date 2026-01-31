import arcade
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, ASSETS_PATH
from story_view import StoryView
# Lưu ý: KHÔNG import SettingsView ở đây để tránh lỗi vòng lặp (Circular Import)

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # --- 1. SETUP ẢNH NỀN ---
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

        # --- 2. LOAD FONT PIXEL ---
        font_path = os.path.join(ASSETS_PATH, "fonts", "PressStart2P-Regular.ttf")
        self.pixel_font = "Arial"
        if os.path.exists(font_path):
            try:
                arcade.load_font(font_path)
                self.pixel_font = "Press Start 2P"
            except Exception as e:
                print(f"Lỗi load font: {e}")

        # --- 3. KHỞI TẠO NHẠC NỀN (QUAN TRỌNG) ---
        # Chúng ta lưu player vào self.window để nó tồn tại xuyên suốt game
        
        # Kiểm tra nếu biến player chưa tồn tại trong window thì tạo mới
        if not hasattr(self.window, "bg_player"):
            self.window.bg_player = None
            self.window.music_volume = 0.5 # Mặc định 50%
            self.window.is_muted = False

        music_path = os.path.join(ASSETS_PATH, "sounds", "menu_music.wav")
        
        # Chỉ phát nhạc nếu chưa có nhạc nào đang chạy
        if self.window.bg_player is None and os.path.exists(music_path):
            try:
                bg_music = arcade.load_sound(music_path)
                # Lưu trình phát nhạc vào biến toàn cục của cửa sổ
                self.window.bg_player = bg_music.play(volume=self.window.music_volume, loop=True)
            except Exception as e:
                print(f"Lỗi phát nhạc: {e}")

    def on_show_view(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        self.ui_list.draw()

        # --- Tiêu đề ---
        arcade.draw_text(
            SCREEN_TITLE,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 80,
            arcade.color.GOLD,
            font_size=25,
            font_name=self.pixel_font,
            anchor_x="center",
            bold=True
        )

        # --- Start ---
        arcade.draw_text(
            "PRESS ENTER TO START",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 20,
            arcade.color.WHITE,
            font_size=12,
            font_name=self.pixel_font,
            anchor_x="center"
        )

        # --- Settings ---
        arcade.draw_text(
            "PRESS 'S' FOR SETTINGS",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 60,
            arcade.color.CYAN, # Đổi màu Cyan cho khác biệt
            font_size=10,
            font_name=self.pixel_font,
            anchor_x="center"
        )

        # --- Quit ---
        arcade.draw_text(
            "ESC TO QUIT",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100,
            arcade.color.GRAY_BLUE,
            font_size=10,
            font_name=self.pixel_font,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            next_view = StoryView()
            self.window.show_view(next_view)
            
        elif key == arcade.key.ESCAPE:
            arcade.exit()
            
        elif key == arcade.key.S:
            # Import bên trong hàm để tránh lỗi Circular Import
            from settings_view import SettingsView 
            next_view = SettingsView()
            self.window.show_view(next_view)