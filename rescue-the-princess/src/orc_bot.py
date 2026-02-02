from character import Character
from settings import *
from pathfinding import a_star_search
import math

RIGHT_FACING = 0
LEFT_FACING = 1

class Orc(Character):
    def __init__(self):
        super().__init__(
            base_folder="Orc/PNG/PNG Sequences", 
            prefix="0_Orc",
            idle_count=18,
            walk_count=24,
            run_count=12,
            jump_count=12,
            slash_count=12,      
            air_slash_count=12,
            hurt_count=12   
        )

class OrcBot(Orc):
    def __init__(self):
        super().__init__()
        self.path = []
        self.attack_range = 60 
        self.attack_cooldown = 0 
        self.vision_range = 400 
        
        # [MỚI] Biến này đánh dấu Bot đã bị chọc giận hay chưa
        self.is_provoked = False 

    def update_ai(self, target, tile_map, physics_engine):
        # 1. NẾU ĐANG BỊ ĐAU
        if self.is_hurting:
            # [QUAN TRỌNG] Bị đánh cái là ghim thù luôn!
            self.is_provoked = True 
            
            # Quay mặt về hướng kẻ thù
            if target.center_x > self.center_x:
                self.character_face_direction = RIGHT_FACING
            else:
                self.character_face_direction = LEFT_FACING
            return 

        # -------------------------------------------------
        # 2. XỬ LÝ AI
        # -------------------------------------------------
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        dist_x = abs(self.center_x - target.center_x)
        dist_y = abs(self.center_y - target.center_y)

        # --- TRƯỜNG HỢP A: TẤN CÔNG (Gần sát bên) ---
        if dist_x < self.attack_range and dist_y < 30:
            self.change_x = 0 
            if target.center_x > self.center_x:
                self.character_face_direction = RIGHT_FACING
            else:
                self.character_face_direction = LEFT_FACING
            
            if self.attack_cooldown <= 0:
                self.attack() 
                self.attack_cooldown = 60 
            return

        # --- TRƯỜNG HỢP B: ĐUỔI THEO ---
        # Đuổi theo nếu: (Trong tầm nhìn) HOẶC (Đã bị chọc giận - is_provoked)
        should_chase = (dist_x < self.vision_range) or self.is_provoked

        if should_chase:
            # Bước 1: Thử tìm đường A*
            start = (int(self.center_x // tile_map.tile_width),
                     int(self.center_y // tile_map.tile_height))
            goal = (int(target.center_x // tile_map.tile_width),
                    int(target.center_y // tile_map.tile_height))

            # Chỉ tìm đường A* nếu khoảng cách không quá xa (để đỡ lag game)
            # Nếu xa quá thì chạy thẳng luôn (logic fallback bên dưới)
            if dist_x < 1000: 
                self.path = a_star_search(start, goal, tile_map)
            else:
                self.path = []

            # --- LOGIC DI CHUYỂN ---
            moved = False 
            
            # Ưu tiên đi theo A* nếu có đường
            if self.path:
                next_step = self.path[0]
                next_y = next_step[1] * tile_map.tile_height
                if physics_engine.can_jump():
                    if next_y > self.center_y + 10:
                        self.change_y = PLAYER_JUMP_SPEED

            # [FALLBACK] CHẠY THẲNG TỚI MỤC TIÊU (Bất chấp A* có hay không)
            # Giúp Bot không bao giờ đứng im khi đã ghim thù
            speed = 2.5 # Tăng tốc xíu cho nó hung hăng (cũ là 2)
            
            if target.center_x > self.center_x + 10: 
                self.character_face_direction = RIGHT_FACING
                self.change_x = speed
                moved = True
            elif target.center_x < self.center_x - 10:
                self.character_face_direction = LEFT_FACING
                self.change_x = -speed
                moved = True
            else:
                self.change_x = 0 
            
            # Nhảy nếu thấy người chơi ở cao hơn
            if physics_engine.can_jump() and target.center_y > self.center_y + 50:
                self.change_y = PLAYER_JUMP_SPEED

            # Nhảy nếu bị kẹt tường
            if moved and self.change_x == 0 and physics_engine.can_jump():
                 self.change_y = PLAYER_JUMP_SPEED

        else:
            # Nếu chưa bị chọc giận và người chơi ở xa -> Đứng chơi
            self.change_x = 0