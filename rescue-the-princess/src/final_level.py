import arcade
import os
from settings import *
from soldier import Soldier   # dùng Soldier thay vì Orc

# --- CẤU HÌNH VẬT LÝ ---
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 20
PLAYER_WALK_SPEED = 5
PLAYER_RUN_SPEED = 10

class FinalView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.tile_map = None
        self.scene = None
        self.soldier = None
        self.physics_engine = None

        self.view_left = 0
        self.map_width_pixels = 0
        self.fade_alpha = 255
        self.fade_state = "FADE_IN"

    def setup(self):
        map_path = os.path.join(ASSETS_PATH, "maps", "finalsence.tmx")
        layer_options = {
            "wall": {"use_spatial_hash": True},
            "Ground": {"use_spatial_hash": True}
        }
        try:
            self.tile_map = arcade.load_tilemap(map_path, scaling=TILE_SCALING, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.map_width_pixels = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
            print("-> Map Final load thành công!")
        except FileNotFoundError:
            print(f"!!! Lỗi không tìm thấy map: {map_path}")
            return
        
        # --- Soldier ---
        self.soldier = Soldier()
        self.soldier.center_x = 100   # sát mép trái
        self.soldier.center_y = 200   # nâng cao hơn để tránh rơi ngay
        self.soldier.is_running = False
        self.scene.add_sprite("Soldier", self.soldier)

        # Physics
        walls_list = []
        if "wall" in self.scene:
            walls_list.append(self.scene["wall"])
        if "Ground" in self.scene:
            walls_list.append(self.scene["Ground"])

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.soldier,
            gravity_constant=GRAVITY,
            walls=walls_list
        )

        self.camera = arcade.Camera2D()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        if self.camera:
            self.camera.use()
        if self.scene:
            self.scene.draw()
        
        # WIN khi tới cuối map
        if self.soldier.center_x >= (self.map_width_pixels - 50):
            arcade.draw_text("WINNER!", self.view_left + 300, 400, arcade.color.GOLD, 50, bold=True)
            arcade.draw_text("ESC to Quit", self.view_left + 350, 300, arcade.color.WHITE, 20)
            # tự động fade out khi thắng
            self.fade_state = "FADE_OUT"

        # Fade
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
            self.physics_engine.update()
            self.scene.update_animation(delta_time, ["Soldier"])

            # Camera follow mượt
            target_x = self.soldier.center_x - (SCREEN_WIDTH / 2)
            if target_x < 0:
                target_x = 0
            max_x = self.map_width_pixels - SCREEN_WIDTH
            if target_x > max_x:
                target_x = max_x
            self.view_left = arcade.math.lerp(self.view_left, target_x, 0.1)

            # Giới hạn map
            if self.soldier.left < 0:
                self.soldier.left = 0
            if self.soldier.right > self.map_width_pixels:
                self.soldier.right = self.map_width_pixels
            if self.soldier.center_y < -200:
                print("Rơi khỏi map! Reset vị trí.")
                self.soldier.center_x = 100
                self.soldier.center_y = 200
                self.soldier.change_y = 0

        elif self.fade_state == "FADE_OUT":
            self.fade_alpha += fade_speed
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                arcade.exit()   # thoát game khi fade out xong

        if self.camera:
            self.camera.position = (int(self.view_left + SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))

    def on_key_press(self, key, modifiers):
        if self.fade_state != "PLAYING":
            return

        # --- ATTACK ---
        if key == arcade.key.F:
            self.soldier.attack()

        # SHIFT để chạy
        elif key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.soldier.is_running = True
            if self.soldier.change_x > 0: self.soldier.change_x = PLAYER_RUN_SPEED
            elif self.soldier.change_x < 0: self.soldier.change_x = -PLAYER_RUN_SPEED

        # Nhảy
        elif key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.physics_engine.can_jump():
                self.soldier.change_y = PLAYER_JUMP_SPEED

        # Di chuyển
        elif key in (arcade.key.LEFT, arcade.key.A):
            speed = PLAYER_RUN_SPEED if self.soldier.is_running else PLAYER_WALK_SPEED
            self.soldier.change_x = -speed
        elif key in (arcade.key.RIGHT, arcade.key.D):
            speed = PLAYER_RUN_SPEED if self.soldier.is_running else PLAYER_WALK_SPEED
            self.soldier.change_x = speed
        
        # Thoát game khi bấm ESC
        elif key == arcade.key.ESCAPE: 
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.soldier.is_running = False
            if self.soldier.change_x > 0: self.soldier.change_x = PLAYER_WALK_SPEED
            elif self.soldier.change_x < 0: self.soldier.change_x = -PLAYER_WALK_SPEED

        elif key in (arcade.key.LEFT, arcade.key.A):
            if self.soldier.change_x < 0: self.soldier.change_x = 0
        elif key in (arcade.key.RIGHT, arcade.key.D):
            if self.soldier.change_x > 0: self.soldier.change_x = 0
