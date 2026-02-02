import arcade
import os
import traceback
from settings import *

RIGHT_FACING = 0
LEFT_FACING = 1


class CharacterChat(arcade.Sprite):
    def __init__(
        self,
        base_folder,
        idle_prefix,
        idle_start,
        idle_end,
        scale=CHARACTER_CHAT_SCALING
    ):
        super().__init__(scale=scale)

        # ===== Basic =====
        self.base_path = os.path.join(ASSETS_PATH, "images", base_folder)
        self.character_face_direction = RIGHT_FACING
        self.cur_texture_index = 0
        self.time_counter = 0.0
        self.animation_speed = 0.1

        # ===== Load idle =====
        self.idle_textures = self.load_idle(idle_prefix, idle_start, idle_end)

        if self.idle_textures:
            self.texture = self.idle_textures[0][RIGHT_FACING]
        else:
            self.texture = arcade.make_soft_square_texture(
                50, arcade.color.BLUE, outer_alpha=255
            )

        # ===== Dialog =====
        self.dialog_lines = []
        self.dialog_index = 0
        self.is_talking = False
        self.font_name = "Arial"

        # ===== Chat bubble (chỉ 1 ảnh) =====
        self.chat_sprite = None
        try:
            frame = arcade.load_texture(
                os.path.join(ASSETS_PATH, "images", "ui", "chat_1.png")
            )
            self.chat_sprite = arcade.Sprite()
            self.chat_sprite.texture = frame
            self.chat_sprite.scale = CHARACTER_CHAT_BUBBLE_SCALING
        except Exception:
            print("❌ LỖI LOAD CHAT BUBBLE:")
            traceback.print_exc()
            self.chat_sprite = None

    # --------------------------------------------------

    def load_idle(self, idle_prefix, idle_start, idle_end):
        textures = []
        for i in range(idle_start, idle_end + 1):
            filename = f"{idle_prefix}{i:03d}.png"
            file_path = os.path.join(self.base_path, filename)
            if os.path.exists(file_path):
                try:
                    tex_r = arcade.load_texture(file_path)
                    tex_l = tex_r.flip_left_right()
                    textures.append([tex_r, tex_l])
                except Exception:
                    print(f"❌ LỖI LOAD IDLE FRAME: {file_path}")
                    traceback.print_exc()
        return textures

    # --------------------------------------------------

    def update_animation(self, delta_time: float = 1 / 60):
        try:
            self.time_counter += delta_time

            # Idle animation
            if self.idle_textures and self.time_counter > self.animation_speed:
                self.time_counter = 0
                self.cur_texture_index = (
                    self.cur_texture_index + 1
                ) % len(self.idle_textures)

                self.texture = self.idle_textures[
                    self.cur_texture_index
                ][self.character_face_direction]

            # Không cần animation cho chat bubble vì chỉ có 1 ảnh
        except Exception:
            print("❌ LỖI update_animation()")
            traceback.print_exc()

    # --------------------------------------------------

    def check_interaction(self, soldier, distance=100):
        try:
            return arcade.get_distance_between_sprites(self, soldier) < distance
        except Exception:
            print("❌ LỖI check_interaction()")
            traceback.print_exc()
            return False

    # --------------------------------------------------

    def draw_dialog(self):
        try:
            if (
                not self.is_talking
                or self.dialog_index >= len(self.dialog_lines)
                or not self.chat_sprite
                or not self.chat_sprite.texture
            ):
                return

            # Position chat bubble
            self.chat_sprite.center_x = self.center_x + 100
            self.chat_sprite.center_y = self.center_y + 100

            # Vẽ bong bóng (Arcade 2.x dùng arcade.draw_sprite, Arcade 3.x dùng self.chat_sprite.draw)
            try:
                self.chat_sprite.draw()  # Arcade 3.x
            except AttributeError:
                arcade.draw_sprite(self.chat_sprite)  # Arcade 2.x fallback

            # Vẽ chữ đè lên bong bóng
            arcade.Text(
                self.dialog_lines[self.dialog_index],
                self.chat_sprite.center_x -  self.chat_sprite.width / 2 + 130,
                self.chat_sprite.center_y -  self.chat_sprite.height /2+ 70,
                arcade.color.BLACK,   # chọn màu tương phản với nền PNG
                12,
                width=240,
                multiline=True,
                anchor_x="center",
                anchor_y="center",
                font_name=self.font_name
            ).draw()

        except Exception:
            print("❌ LỖI draw_dialog()")
            traceback.print_exc()
