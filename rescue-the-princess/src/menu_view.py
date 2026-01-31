import arcade
import os
import pyglet
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
        font_path = os.path.join(ASSETS_PATH, "fonts", "SVN-Determination Sans.ttf")
        self.pixel_font = "Arial"
        if os.path.exists(font_path):
            try:
                arcade.load_font(font_path)
                self.pixel_font = "Press Start 2P"
            except Exception as e:
                print(f"Lỗi load font: {e}")

        # --- 3. KHỞI TẠO NHẠC NỀN ---
        if not hasattr(self.window, "bg_player"):
            self.window.bg_player = None
            self.window.music_volume = 0.5
            self.window.is_muted = False

        music_path = os.path.join(ASSETS_PATH, "sounds", "menu_music.wav")
        if self.window.bg_player is None and os.path.exists(music_path):
            try:
                # Dùng pyglet để loop nhạc
                source = pyglet.media.load(music_path, streaming=False)
                player = pyglet.media.Player()
                player.queue(source)
                player.loop = True
                player.volume = self.window.music_volume
                player.play()
                self.window.bg_player = player
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
            "PRESS 'G' FOR SETTINGS",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 60,
            arcade.color.CYAN,
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
            # --- Tắt nhạc khi vào game ---
            if hasattr(self.window, "bg_player") and self.window.bg_player:
                self.window.bg_player.pause()
                self.window.bg_player.delete()
                self.window.bg_player = None

            next_view = StoryView()
            self.window.show_view(next_view)
            
        elif key == arcade.key.ESCAPE:
            arcade.exit()
            
        elif key == arcade.key.G:
            from settings_view import SettingsView 
            next_view = SettingsView()
            self.window.show_view(next_view)
