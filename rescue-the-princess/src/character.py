import arcade
import os
from settings import *

RIGHT_FACING = 0
LEFT_FACING = 1

class Character(arcade.Sprite):
    def __init__(self, base_folder, prefix, idle_count=18, walk_count=24, run_count=12, jump_count=12, slash_count=12, air_slash_count=12, hurt_count=12):
        super().__init__(scale=CHARACTER_SCALING)

        self.base_path = os.path.join(ASSETS_PATH, "images", base_folder)

        self.character_face_direction = RIGHT_FACING
        self.cur_texture_index = 0
        self.time_counter = 0.0
        self.animation_speed = 0.05
        
        self.is_running = False
        self.is_attacking = False 
        self.is_hurting = False   # Trạng thái bị thương

        # --- LOAD TEXTURES ---
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
                    pass
            return textures

        # Load animations
        self.walk_textures = load_texture_sequence("Walking", f"{prefix}_Walking_", walk_count)
        self.idle_textures = load_texture_sequence("Idle", f"{prefix}_Idle_", idle_count)
        self.run_textures = load_texture_sequence("Running", f"{prefix}_Running_", run_count)
        self.jump_textures = load_texture_sequence("Jump Loop", f"{prefix}_Jump Loop_", jump_count)
        self.slash_textures = load_texture_sequence("Slashing", f"{prefix}_Slashing_", slash_count)
        self.air_slash_textures = load_texture_sequence("Slashing in The Air", f"{prefix}_Slashing in The Air_", air_slash_count)
        self.hurt_textures = load_texture_sequence("Hurt", f"{prefix}_Hurt_", hurt_count)

        # Fallback
        if not self.idle_textures and self.walk_textures: self.idle_textures = self.walk_textures
        if not self.slash_textures: self.slash_textures = self.idle_textures
        if not self.hurt_textures: self.hurt_textures = self.idle_textures

        # Set ảnh ban đầu
        if self.idle_textures:
            self.texture = self.idle_textures[0][RIGHT_FACING]

    def attack(self):
        """Gọi khi nhấn phím F"""
        if not self.is_attacking and not self.is_hurting:
            self.is_attacking = True
            self.cur_texture_index = 0
            self.time_counter = 0

    def take_damage(self, knockback_x=0, knockback_y=0):
        """
        knockback_x: Lực đẩy ngang (quan trọng)
        knockback_y: Lực nảy lên
        """
        if not self.is_hurting:
            self.is_hurting = True
            self.is_attacking = False # Ngắt chiêu
            self.cur_texture_index = 0
            self.time_counter = 0
            
            # --- ÁP DỤNG LỰC ĐẨY (PHYSICS) ---
            # Nhân vật sẽ bị trượt đi theo lực này
            self.change_x = knockback_x
            
            # Chỉ nảy lên một chút nếu đang đứng dưới đất
            if self.change_y == 0:
                self.change_y = knockback_y

    def update_animation(self, delta_time: float = 1/60):
        self.time_counter += delta_time

        # --- [QUAN TRỌNG NHẤT] LOGIC HƯỚNG MẶT ---
        # Chỉ cho phép đổi hướng mặt KHI KHÔNG BỊ ĐAU.
        # Nếu đang Hurt, giữ nguyên hướng mặt về phía kẻ thù, mặc dù body đang trượt lùi về sau.
        if not self.is_hurting:
            if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
                self.character_face_direction = LEFT_FACING
            elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
                self.character_face_direction = RIGHT_FACING

        # --- ƯU TIÊN 1: BỊ THƯƠNG (HURT) ---
        if self.is_hurting and self.hurt_textures:
            if self.time_counter > 0.05:
                self.time_counter = 0
                self.cur_texture_index += 1
                
                # Chạy hết animation Hurt thì trở lại bình thường
                if self.cur_texture_index >= len(self.hurt_textures):
                    self.is_hurting = False
                    self.cur_texture_index = 0
                    self.change_x = 0 # Dừng lực đẩy sau khi hết animation (tùy chọn)
                else:
                    self.texture = self.hurt_textures[self.cur_texture_index][self.character_face_direction]
            return # Chặn tất cả animation khác

        # --- ƯU TIÊN 2: TẤN CÔNG ---
        if self.is_attacking:
            if abs(self.change_y) > 1 and self.air_slash_textures:
                textures = self.air_slash_textures
            else:
                textures = self.slash_textures

            if self.time_counter > 0.03: 
                self.time_counter = 0
                self.cur_texture_index += 1
                if self.cur_texture_index >= len(textures):
                    self.is_attacking = False
                    self.cur_texture_index = 0
                else:
                    self.texture = textures[self.cur_texture_index][self.character_face_direction]
            return

        # --- ƯU TIÊN 3: NHẢY ---
        if self.change_y != 0 and self.jump_textures:
            if self.time_counter > self.animation_speed:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.jump_textures)
                self.texture = self.jump_textures[self.cur_texture_index][self.character_face_direction]
            return

        # --- ƯU TIÊN 4: DI CHUYỂN ---
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

        # --- ƯU TIÊN 5: ĐỨNG YÊN ---
        else:
            if self.idle_textures and self.time_counter > 0.05:
                self.time_counter = 0
                self.cur_texture_index = (self.cur_texture_index + 1) % len(self.idle_textures)
                self.texture = self.idle_textures[self.cur_texture_index][self.character_face_direction]

    def update(self):
        # Update vị trí theo vật lý
        self.center_x += self.change_x
        self.center_y += self.change_y