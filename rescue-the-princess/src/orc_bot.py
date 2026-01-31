from character import Character
from settings import *
from pathfinding import a_star_search

RIGHT_FACING = 0
LEFT_FACING = 1

class Orc(Character):
    def __init__(self):
        super().__init__(base_folder="Orc/PNG/PNG Sequences", prefix="0_Orc")
        # Orc cơ bản: có animation, di chuyển như Soldier nhưng không nhận input

class OrcBot(Orc):
    def __init__(self):
        super().__init__()
        self.path = []

    def update_ai(self, target, tile_map, physics_engine):
        """
        Bot Orc tự tìm đường tới Soldier bằng A*.
        target: Soldier (sprite người chơi)
        tile_map: bản đồ hiện tại (arcade.TileMap)
        physics_engine: engine vật lý của OrcBot (để kiểm tra can_jump)
        """

        # 1. Lấy vị trí tile hiện tại của Orc và Soldier
        start = (int(self.center_x // tile_map.tile_width),
                 int(self.center_y // tile_map.tile_height))
        goal = (int(target.center_x // tile_map.tile_width),
                int(target.center_y // tile_map.tile_height))

        # 2. Chạy thuật toán A* để tìm đường
        self.path = a_star_search(start, goal, tile_map)

        if self.path:
            next_step = self.path[0]
            next_x = next_step[0] * tile_map.tile_width
            next_y = next_step[1] * tile_map.tile_height

            # --- Cập nhật hướng mặt theo vị trí Soldier ---
            if target.center_x > self.center_x:
                self.character_face_direction = RIGHT_FACING
                self.change_x = 2
            elif target.center_x < self.center_x:
                self.character_face_direction = LEFT_FACING
                self.change_x = -2
            else:
                self.change_x = 0

            # --- Nhảy: theo Soldier hoặc theo path ---
            if physics_engine.can_jump():
                # Nếu Soldier đang nhảy, bot cũng nhảy
                if target.change_y > 0:
                    self.change_y = PLAYER_JUMP_SPEED
                # Hoặc nếu path yêu cầu đi lên
                elif next_y > self.center_y:
                    self.change_y = PLAYER_JUMP_SPEED
