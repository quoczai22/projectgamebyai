import arcade
import os
from settings import *

RIGHT_FACING = 0
LEFT_FACING = 1

class CharacterChat(arcade.Sprite):
    def __init__(self, base_folder, idle_prefix, idle_start, idle_end, scale=CHARACTER_CHAT_SCALING):

        super().__init__(scale=scale)

        self.base_path = os.path.join(ASSETS_PATH, "images", base_folder)
        self.character_face_direction = RIGHT_FACING
        self.cur_texture_index = 0
        self.time_counter = 0.0
        self.animation_speed = 0.1

        # Load tất cả frame Idle
        self.idle_textures = self.load_idle(idle_prefix, idle_start, idle_end)

        # Nếu có texture thì gán, nếu không thì tạo ô vuông xanh
        if self.idle_textures:
            self.texture = self.idle_textures[0][RIGHT_FACING]
        else:
            self.texture = arcade.make_soft_square_texture(50, arcade.color.BLUE, outer_alpha=255)

    def load_idle(self, idle_prefix, idle_start, idle_end):
        textures = []
        for i in range(idle_start, idle_end + 1):
            filename = f"{idle_prefix}{i:03d}.png"
            file_path = os.path.join(self.base_path, filename)
            if os.path.exists(file_path):
                tex_r = arcade.load_texture(file_path)
                tex_l = tex_r.flip_left_right()
                textures.append([tex_r, tex_l])
        return textures

    def update_animation(self, delta_time: float = 1 / 60):
        self.time_counter += delta_time
        if self.idle_textures and self.time_counter > self.animation_speed:
            self.time_counter = 0
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.idle_textures)
            self.texture = self.idle_textures[self.cur_texture_index][self.character_face_direction]

    def check_interaction(self, soldier, distance=100):
        return arcade.get_distance_between_sprites(self, soldier) < distance
