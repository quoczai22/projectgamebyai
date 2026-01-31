import arcade
import os
from settings import *
from cave_level import CaveView
from soldier import Soldier
from orc_bot import OrcBot   # thêm bot

# --- CẤU HÌNH VẬT LÝ ---
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 20
PLAYER_WALK_SPEED = 5
PLAYER_RUN_SPEED = 10

class HallwayNightCaveView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.tile_map = None
        self.scene = None
        self.soldier = None
        self.orc_bot = None
        self.soldier_engine = None
        self.orc_engine = None

        self.view_left = 0
        self.map_width_pixels = 0
        self.fade_alpha = 255
        self.fade_state = "FADE_IN"

    def setup(self):
        map_path = os.path.join(ASSETS_PATH, "maps", "HallWayNightCave.tmx")
        layer_options = {
            "wall": {"use_spatial_hash": True},
            "Ground": {"use_spatial_hash": True}
        }
        try:
            self.tile_map = arcade.load_tilemap(map_path, scaling=TILE_SCALING, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.map_width_pixels = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
            print("-> Map HallwayNightCave load thành công!")
        except FileNotFoundError:
            print(f"!!! Lỗi không tìm thấy map: {map_path}")
            return
        
        # Soldier xuất hiện sát mép trái
        self.soldier = Soldier()
        self.soldier.center_x = 100
        self.soldier.center_y = 200
        self.soldier.is_running = False
        self.scene.add_sprite("Soldier", self.soldier)

        # OrcBot xuất hiện ngoài màn hình bên phải
        self.orc_bot = OrcBot()
        self.orc_bot.center_x = SCREEN_WIDTH + 200
        self.orc_bot.center_y = 200
        self.scene.add_sprite("OrcBot", self.orc_bot)

        # Physics
        walls_list = []
        if "wall" in self.scene: walls_list.append(self.scene["wall"])
        if "Ground" in self.scene: walls_list.append(self.scene["Ground"])

        self.soldier_engine = arcade.PhysicsEnginePlatformer(self.soldier, gravity_constant=GRAVITY, walls=walls_list)
        self.orc_engine = arcade.PhysicsEnginePlatformer(self.orc_bot, gravity_constant=GRAVITY, walls=walls_list)

        # Camera
        self.camera = arcade.Camera2D()
        arcade.set_background_color(arcade.color.MIDNIGHT_BLUE)

    def on_draw(self):
        self.clear()
        if self.camera: self.camera.use()
        if self.scene: self.scene.draw()
        
        if self.soldier.center_x >= (self.map_width_pixels - 50):
            arcade.draw_text("ENTER -> VÀO HANG", self.view_left + 300, 300, arcade.color.RED, 20, bold=True)
        
        if self.fade_alpha > 0:
            rect = arcade.LBWH(self.view_left, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            arcade.draw_rect_filled(rect, (0, 0, 0, int(self.fade_alpha)))

    def on_update(self, delta_time):
        fade_speed = 5
        if self.fade_state == "FADE_IN":
            self.fade_alpha -= fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_state = "PLAYING"

        elif self.fade_state == "PLAYING":
            self.soldier_engine.update()
            self.orc_engine.update()
            self.scene.update_animation(delta_time, ["Soldier", "OrcBot"])

            # Bot Orc tìm đường tới Soldier
            self.orc_bot.update_ai(self.soldier, self.tile_map, self.orc_engine)

            # Camera follow Soldier
            target_x = self.soldier.center_x - (SCREEN_WIDTH / 2)
            target_x = max(0, min(target_x, self.map_width_pixels - SCREEN_WIDTH))
            self.view_left = arcade.math.lerp(self.view_left, target_x, 0.1)
            
            # Giới hạn map
            if self.soldier.left < 0: self.soldier.left = 0
            if self.soldier.right > self.map_width_pixels: self.soldier.right = self.map_width_pixels

            # Reset nếu rơi khỏi map
            if self.soldier.center_y < -100:
                print("Rơi khỏi map! Reset vị trí.")
                self.soldier.center_x = 100
                self.soldier.center_y = 200
                self.soldier.change_y = 0
            
        elif self.fade_state == "FADE_OUT":
            self.fade_alpha += fade_speed
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.switch_to_next_level()

        if self.camera:
            self.camera.position = (int(self.view_left + SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))

    def switch_to_next_level(self):
        next_view = CaveView()
        next_view.setup()
        self.window.show_view(next_view)

    def on_key_press(self, key, modifiers):
        if self.fade_state != "PLAYING":
            return

        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.soldier.is_running = True
            if self.soldier.change_x > 0: self.soldier.change_x = PLAYER_RUN_SPEED
            elif self.soldier.change_x < 0: self.soldier.change_x = -PLAYER_RUN_SPEED

        elif key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.soldier_engine.can_jump():
                self.soldier.change_y = PLAYER_JUMP_SPEED

        elif key in (arcade.key.LEFT, arcade.key.A):
            speed = PLAYER_RUN_SPEED if self.soldier.is_running else PLAYER_WALK_SPEED
            self.soldier.change_x = -speed
        elif key in (arcade.key.RIGHT, arcade.key.D):
            speed = PLAYER_RUN_SPEED if self.soldier.is_running else PLAYER_WALK_SPEED
            self.soldier.change_x = speed

        elif key == arcade.key.ENTER:
            if self.soldier.center_x >= (self.map_width_pixels - 50):
                self.fade_state = "FADE_OUT"

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.soldier.is_running = False
            if self.soldier.change_x > 0: self.soldier.change_x = PLAYER_WALK_SPEED
            elif self.soldier.change_x < 0: self.soldier.change_x = -PLAYER_WALK_SPEED

        elif key in (arcade.key.LEFT, arcade.key.A):
            if self.soldier.change_x < 0: self.soldier.change_x = 0
        elif key in (arcade.key.RIGHT, arcade.key.D):
            if self.soldier.change_x > 0: self.soldier.change_x = 0
