import arcade
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_PATH
from sound_manager import SoundManager
from pixel_text import PixelText # Import class chữ mới

class SettingsView(arcade.View):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.sound_manager = sound_manager

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

        self.mode = 1 # 1: Music, 2: Effects

    def on_show_view(self):
        self.window.set_mouse_visible(True)
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        self.ui_list.draw()

        # Tiêu đề
        PixelText("SETTINGS", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120,
                  arcade.color.GOLD, size=30, anchor_x="center", bold=True).draw()

        # Mode
        mode_str = "< MODE: MUSIC >" if self.mode == 1 else "< MODE: EFFECTS >"
        color_mode = arcade.color.CYAN if self.mode == 1 else arcade.color.ORANGE
        PixelText(mode_str, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60,
                  color_mode, size=16, anchor_x="center").draw()

        # Lấy dữ liệu Volume
        if self.mode == 1:
            vol = self.sound_manager.music_volume
            muted = self.sound_manager.is_muted_music
        else:
            vol = self.sound_manager.effect_volume
            muted = self.sound_manager.is_muted_effect

        # Vẽ thanh Bar
        bar_count = int(vol * 10)
        bar_str = "|" * bar_count + "." * (10 - bar_count)
        
        if muted:
            PixelText("MUTED", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 
                      arcade.color.RED, size=16, anchor_x="center").draw()
            PixelText("[   MUTE   ]", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40, 
                      arcade.color.RED, size=16, anchor_x="center").draw()
        else:
            PixelText(f"VOL: {int(vol * 100)}%", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 
                      arcade.color.WHITE, size=16, anchor_x="center").draw()
            PixelText(f"[{bar_str}]", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40, 
                      arcade.color.GREEN, size=16, anchor_x="center").draw()

        # Hướng dẫn
        PixelText("1: Music   2: Effects", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100,
                  arcade.color.LIGHT_GRAY, size=10, anchor_x="center").draw()
        PixelText("UP/DOWN: Adjust   M: Mute   ESC: Back", SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 130,
                  arcade.color.LIGHT_GRAY, size=10, anchor_x="center").draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.NUM_1: self.mode = 1
        elif key == arcade.key.NUM_2: self.mode = 2
        elif key == arcade.key.M:
            if self.mode == 1: self.sound_manager.toggle_music_mute()
            else: self.sound_manager.toggle_effect_mute()
        
        elif key == arcade.key.UP:
            if self.mode == 1 and not self.sound_manager.is_muted_music:
                self.sound_manager.set_music_volume(self.sound_manager.music_volume + 0.1)
            elif self.mode == 2 and not self.sound_manager.is_muted_effect:
                self.sound_manager.set_effect_volume(self.sound_manager.effect_volume + 0.1)
                
        elif key == arcade.key.DOWN:
            if self.mode == 1 and not self.sound_manager.is_muted_music:
                self.sound_manager.set_music_volume(self.sound_manager.music_volume - 0.1)
            elif self.mode == 2 and not self.sound_manager.is_muted_effect:
                self.sound_manager.set_effect_volume(self.sound_manager.effect_volume - 0.1)

        elif key == arcade.key.ESCAPE:
            from menu_view import MenuView
            # Trả sound_manager về Menu để nó biết nhạc đã chỉnh thế nào
            menu = MenuView(self.sound_manager)
            self.window.show_view(menu)