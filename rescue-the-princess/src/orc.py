import arcade
import os
from settings import *

# Hướng mặt
RIGHT_FACING = 0
LEFT_FACING = 1

class Orc(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=CHARACTER_SCALING) 
        self.is_running = False

        # Đường dẫn gốc tới thư mục sprite Orc
        self.base_path = os.path.join(ASSETS_PATH, "images", "Orc", "PNG", "PNG Sequences")

        # Cấu hình animation
        self.character_face_direction = RIGHT_FACING
        self.cur_texture_index = 0
        self.time_counter = 0.0
        self.animation_speed = 0.05 

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

        # Load ảnh
        self.walk_textures = load_texture_sequence("Walking", "0_Orc_Walking_", 23)
        self.idle_textures = load_texture_sequence("Idle", "0_Orc_Idle_", 17)
        self.run_textures = load_texture_sequence("Running", "0_Orc_Running_", 12) 
        self.jump_textures = load_texture_sequence("Jump Loop", "0_Orc_Jump Loop_", 6) 

        # Dự phòng
        if not self.idle_textures and self.walk_textures: self.idle_textures = self.walk_textures
        if not self.run_textures and self.walk_textures: self.run_textures = self.walk_textures
        if not self.jump_textures and self.idle_textures: self.jump_textures = self.idle_textures

        # Ảnh ban đầu
        if self.idle_textures:
            self.texture = self.idle_textures[0][RIGHT_FACING]
        else:
            self.texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)

    def update_animation(self, delta_time: float = 1 / 60):
        if self.change_x < 0: self.character_face_direction = LEFT_FACING
        elif self.change_x > 0: self.character_face_direction = RIGHT_FACING
        self.time_counter += delta_time

        # Jump
        if self.change_y != 0 and self.jump_textures:
            if self.time_counter > self.animation_speed:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.jump_textures)
                self.texture = self.jump_textures[self.cur_texture_index][self.character_face_direction]
            return

        # Walk / Run
        if abs(self.change_x) > 0.1:
            if self.is_running and self.run_textures:
                textures = self.run_textures; speed = 0.03
            elif self.walk_textures:
                textures = self.walk_textures; speed = 0.05
            else:
                textures = self.idle_textures; speed = 0.05

            if self.time_counter > speed:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(textures)
                self.texture = textures[self.cur_texture_index][self.character_face_direction]
        else:
            if self.idle_textures and self.time_counter > 0.05:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.idle_textures)
                self.texture = self.idle_textures[self.cur_texture_index][self.character_face_direction]

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
