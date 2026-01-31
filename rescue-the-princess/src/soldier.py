import arcade
import os
from settings import *

# Hướng mặt
RIGHT_FACING = 0
LEFT_FACING = 1

class Soldier(arcade.Sprite):
    def __init__(self):
        # Scale: lấy từ settings.py (CHARACTER_SCALING)
        super().__init__(scale=CHARACTER_SCALING) 
        
        # Biến trạng thái chạy (Shift)
        self.is_running = False

        # --- 1. ĐƯỜNG DẪN GỐC (trỏ về thư mục Valkyrie_2) ---
        self.base_path = os.path.join(ASSETS_PATH, "images", "Valkyrie_2", "PNG", "PNG Sequences")

        # --- 2. CẤU HÌNH ANIMATION ---
        self.character_face_direction = RIGHT_FACING
        self.cur_texture_index = 0
        self.time_counter = 0.0
        self.animation_speed = 0.05 

        # --- 3. HÀM LOAD ẢNH ---
        def load_texture_sequence(sub_folder, filename_prefix, count):
            textures = []
            for i in range(count):
                filename = f"{filename_prefix}{i:03d}.png"
                file_path = os.path.join(self.base_path, sub_folder, filename)

                if os.path.exists(file_path):
                    tex_r = arcade.load_texture(file_path)
                    tex_l = tex_r.flip_left_right()
                    textures.append([tex_r, tex_l])
                else:
                    # Nếu thiếu file thì bỏ qua, tránh crash
                    pass
            return textures

        # --- 4. THỰC HIỆN LOAD ẢNH ---
        # Lưu ý: tên file phải khớp với bộ sprite bạn có trong assets
        self.walk_textures = load_texture_sequence("Walking", "0_Valkyrie_Walking_", 24)
        self.idle_textures = load_texture_sequence("Idle", "0_Valkyrie_Idle_", 18)
        self.run_textures = load_texture_sequence("Running", "0_Valkyrie_Running_", 12)
        self.jump_textures = load_texture_sequence("Jump Loop", "0_Valkyrie_Jump Loop_", 12)

        # --- XỬ LÝ DỰ PHÒNG ---
        if not self.idle_textures and self.walk_textures: self.idle_textures = self.walk_textures
        if not self.run_textures and self.walk_textures: self.run_textures = self.walk_textures
        if not self.jump_textures and self.idle_textures: self.jump_textures = self.idle_textures

        # Thiết lập ảnh ban đầu
        if self.idle_textures:
            self.texture = self.idle_textures[0][RIGHT_FACING]
        else:
            self.texture = arcade.make_soft_square_texture(50, arcade.color.RED, outer_alpha=255)

    def update_animation(self, delta_time: float = 1 / 60):
        # 1. Xác định hướng quay mặt
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        self.time_counter += delta_time

        # --- ƯU TIÊN 1: NHẢY ---
        if self.change_y != 0 and self.jump_textures:
            if self.time_counter > self.animation_speed:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.jump_textures)
                self.texture = self.jump_textures[self.cur_texture_index][self.character_face_direction]
            return

        # --- ƯU TIÊN 2: DI CHUYỂN ---
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

        # --- ƯU TIÊN 3: ĐỨNG YÊN ---
        else:
            if self.idle_textures and self.time_counter > 0.05:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.idle_textures)
                self.texture = self.idle_textures[self.cur_texture_index][self.character_face_direction]

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
