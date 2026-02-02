import arcade
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, ASSETS_PATH
from story_view import StoryView
from sound_manager import SoundManager
from pixel_text import PixelText  # Import class chữ mới

class MenuView(arcade.View):
    def __init__(self, sound_manager=None):
        super().__init__()
        # Khởi tạo hoặc dùng lại SoundManager
        self.sound_manager = sound_manager or SoundManager()

        # --- Ảnh nền ---
        self.ui_list = arcade.SpriteList()
        image_path = os.path.join(ASSETS_PATH, "images", "menu_view.png")
        if os.path.exists(image_path):
            bg_sprite = arcade.Sprite(image_path)
            bg_sprite.center_x = SCREEN_WIDTH / 2
            bg_sprite.center_y = SCREEN_HEIGHT / 2
            bg_sprite.width = SCREEN_WIDTH
            bg_sprite.height = SCREEN_HEIGHT
            self.ui_list.append(bg_sprite)

        # --- Text Objects (Dùng PixelText) ---
        self.title_text = PixelText(
            SCREEN_TITLE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
            arcade.color.GOLD, size=40, anchor_x="center", bold=True
        )
        self.start_text = PixelText(
            "PRESS ENTER TO START", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10,
            arcade.color.WHITE, size=20, anchor_x="center"
        )
        self.settings_text = PixelText(
            "PRESS 'G' FOR SETTINGS", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
            arcade.color.CYAN, size=15, anchor_x="center"
        )
        self.quit_text = PixelText(
            "ESC TO QUIT", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110,
            arcade.color.GRAY_BLUE, size=15, anchor_x="center"
        )

        self.setup()

    def setup(self):
        # Bật nhạc nền nếu chưa có
        if self.sound_manager.bg_player is None:
            self.sound_manager.play_music("menu_music.wav")

    def on_show_view(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        self.ui_list.draw()
        
        self.title_text.draw()
        self.start_text.draw()
        self.settings_text.draw()
        self.quit_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.sound_manager.stop_music() # Tắt nhạc nền để vào Story
            
            next_view = StoryView(self.sound_manager)
            self.window.show_view(next_view)
            
        elif key == arcade.key.ESCAPE:
            arcade.exit()
            
        elif key == arcade.key.G:
            from settings_view import SettingsView
            # Truyền sound_manager đi để chỉnh âm thanh
            next_view = SettingsView(self.sound_manager)
            self.window.show_view(next_view)