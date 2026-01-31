import arcade
import os
from settings import *

RIGHT_FACING = 0
LEFT_FACING = 1

class Character(arcade.Sprite):
    def __init__(self, base_folder, prefix, idle_count=18, walk_count=24, run_count=12, jump_count=12):
        super().__init__(scale=CHARACTER_SCALING)

        # Đường dẫn gốc (ví dụ Valkyrie_2 hoặc Orc)
        self.base_path = os.path.join(ASSETS_PATH, "images", base_folder)

        # Hướng mặt
        self.character_face_direction = RIGHT_FACING
        self.cur_texture_index = 0
        self.time_counter = 0.0
        self.animation_speed = 0.05
        self.is_running = False

        # Hàm load ảnh
        def load_texture_sequence(sub_folder, filename_prefix, count):
            textures = []
            for i in range(count):
                filename = f"{filename_prefix}{i:03d}.png"
                file_path = os.path.join(self.base_path, sub_folder, filename)
                if os.path.exists(file_path):
                    tex_r = arcade.load_texture(file_path)
                    tex_l = tex_r.flip_left_right()
                    textures.append([tex_r, tex_l])
            return textures

        # Load các bộ animation
        self.walk_textures = load_texture_sequence("Walking", f"{prefix}_Walking_", walk_count)
        self.idle_textures = load_texture_sequence("Idle", f"{prefix}_Idle_", idle_count)
        self.run_textures = load_texture_sequence("Running", f"{prefix}_Running_", run_count)
        self.jump_textures = load_texture_sequence("Jump Loop", f"{prefix}_Jump Loop_", jump_count)

        # Dự phòng
        if not self.idle_textures and self.walk_textures: self.idle_textures = self.walk_textures
        if not self.run_textures and self.walk_textures: self.run_textures = self.walk_textures
        if not self.jump_textures and self.idle_textures: self.jump_textures = self.idle_textures

        # Ảnh ban đầu
        if self.idle_textures:
            self.texture = self.idle_textures[0][RIGHT_FACING]
        else:
            self.texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)

    def update_animation(self, delta_time: float = 1/60):
        # Xác định hướng mặt
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        self.time_counter += delta_time

        # Ưu tiên 1: Nhảy
        if self.change_y != 0 and self.jump_textures:
            if self.time_counter > self.animation_speed:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.jump_textures)
                self.texture = self.jump_textures[self.cur_texture_index][self.character_face_direction]
            return

        # Ưu tiên 2: Di chuyển
        if abs(self.change_x) > 0.1:
            if self.is_running and self.run_textures:
                textures = self.run_textures
                speed = 0.03
            elif self.walk_textures:
                textures = self.walk_textures
                speed = 0.05
            else:
                textures = self.idle_textures
                speed = 0.05

            if self.time_counter > speed:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(textures)
                self.texture = textures[self.cur_texture_index][self.character_face_direction]

        # Ưu tiên 3: Đứng yên
        else:
            if self.idle_textures and self.time_counter > 0.05:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.idle_textures)
                self.texture = self.idle_textures[self.cur_texture_index][self.character_face_direction]

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
