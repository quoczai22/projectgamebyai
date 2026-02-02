import arcade
import os
from settings import *
from night_level import NightView
from soldier import Soldier
from orc_bot import OrcBot

# --- CẤU HÌNH ---
GRAVITY = 1.0
PLAYER_JUMP_SPEED = 20
PLAYER_WALK_SPEED = 5
PLAYER_RUN_SPEED = 10

class HallwayDayNightView(arcade.View):
    def __init__(self, sound_manager=None):
        super().__init__()
        self.sound_manager = sound_manager
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

        # Cờ điều khiển di chuyển
        self.left_pressed = False
        self.right_pressed = False
        self.shift_pressed = False

        # Text hướng dẫn
        self.guide_text = arcade.Text(
            "ĐÊM TỐI",
            0, 0,
            arcade.color.RED,
            20,
            bold=True
        )

    def setup(self):
        map_path = os.path.join(ASSETS_PATH, "maps", "HallwayDayNight.tmx")
        try:
            self.tile_map = arcade.load_tilemap(
                map_path, scaling=TILE_SCALING,
                layer_options={"wall": {"use_spatial_hash": True},
                               "Ground": {"use_spatial_hash": True}}
            )
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.map_width_pixels = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
        except FileNotFoundError:
            print(f"!!! Lỗi không tìm thấy map: {map_path}")
            return
        
        # Soldier
        self.soldier = Soldier()
        self.soldier.center_x, self.soldier.center_y = 100, 200
        self.scene.add_sprite("Soldier", self.soldier)

        # Orc Bot
        self.orc_bot = OrcBot()
        self.orc_bot.center_x, self.orc_bot.center_y = 800, 200
        self.scene.add_sprite("OrcBot", self.orc_bot)

        # Physics
        walls_list = []
        if "wall" in self.scene: walls_list.append(self.scene["wall"])
        if "Ground" in self.scene: walls_list.append(self.scene["Ground"])
        self.soldier_engine = arcade.PhysicsEnginePlatformer(
            self.soldier, gravity_constant=GRAVITY, walls=walls_list
        )
        self.orc_engine = arcade.PhysicsEnginePlatformer(
            self.orc_bot, gravity_constant=GRAVITY, walls=walls_list
        )

        # Camera
        self.camera = arcade.Camera2D()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        if self.camera: self.camera.use()
        if self.scene: self.scene.draw()
        if self.soldier.center_x >= (self.map_width_pixels - 50):
            self.guide_text.x, self.guide_text.y = self.view_left + 300, 300
            self.guide_text.draw()
        if self.fade_alpha > 0:
            arcade.draw_rect_filled(
                arcade.LBWH(self.view_left, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
                (0, 0, 0, int(self.fade_alpha))
            )

    def on_update(self, delta_time):
        fade_speed = 5
        if self.fade_state == "FADE_IN":
            self.fade_alpha = max(0, self.fade_alpha - fade_speed)
            if self.fade_alpha == 0: self.fade_state = "PLAYING"

        elif self.fade_state == "PLAYING":
            # Di chuyển bằng cờ
            if not self.soldier.is_hurting:
                self.soldier.change_x = 0
                speed = PLAYER_RUN_SPEED if self.shift_pressed else PLAYER_WALK_SPEED
                self.soldier.is_running = self.shift_pressed
                if self.left_pressed and not self.right_pressed:
                    self.soldier.change_x = -speed
                elif self.right_pressed and not self.left_pressed:
                    self.soldier.change_x = speed

            # Physics & animation
            self.soldier_engine.update()
            self.orc_engine.update()
            self.scene.update_animation(delta_time, ["Soldier", "OrcBot"])

            # AI Bot
            if self.orc_bot in self.scene["OrcBot"]:
                self.orc_bot.update_ai(self.soldier, self.tile_map, self.orc_engine)

            # Combat
            KNOCK_X, KNOCK_Y = 8, 5
            if self.orc_bot in self.scene["OrcBot"]:
                if self.soldier.is_attacking and arcade.check_for_collision(self.soldier, self.orc_bot):
                    direction = 1 if self.soldier.center_x < self.orc_bot.center_x else -1
                    self.orc_bot.take_damage(KNOCK_X * direction, KNOCK_Y)
                if self.orc_bot.is_attacking and arcade.check_for_collision(self.orc_bot, self.soldier):
                    direction = 1 if self.orc_bot.center_x < self.soldier.center_x else -1
                    self.soldier.take_damage(KNOCK_X * direction, KNOCK_Y)

            # Camera & limits
            target_x = max(0, min(self.soldier.center_x - SCREEN_WIDTH/2,
                                  self.map_width_pixels - SCREEN_WIDTH))
            self.view_left = arcade.math.lerp(self.view_left, target_x, 0.1)
            if self.soldier.left < 0: self.soldier.left = 0
            if self.soldier.right > self.map_width_pixels: self.soldier.right = self.map_width_pixels
            if self.soldier.center_y < -100:
                self.soldier.center_x, self.soldier.center_y, self.soldier.change_y = 100, 200, 0
            if self.orc_bot in self.scene["OrcBot"]:
                if self.orc_bot.left < 0: self.orc_bot.left = 0
                if self.orc_bot.right > self.map_width_pixels: self.orc_bot.right = self.map_width_pixels
                if self.orc_bot.center_y < -100: self.orc_bot.kill()

            if self.soldier.center_x >= (self.map_width_pixels - 50):
                self.fade_state = "FADE_OUT"

        elif self.fade_state == "FADE_OUT":
            self.fade_alpha = min(255, self.fade_alpha + fade_speed)
            if self.fade_alpha == 255: self.switch_to_next_level()

        self.camera.position = (int(self.view_left + SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))

    def switch_to_next_level(self):
        next_view = NightView(self.sound_manager)
        next_view.setup()
        self.window.show_view(next_view)

    def on_key_press(self, key, modifiers):
        if self.fade_state != "PLAYING" or self.soldier.is_hurting: return
        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.shift_pressed = True
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.soldier_engine.can_jump():
                self.soldier.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.F:
            self.soldier.attack()
            if self.sound_manager: self.sound_manager.play_effect("sword")
        elif key == arcade.key.ENTER and self.soldier.center_x >= (self.map_width_pixels - 50):
            self.fade_state = "FADE_OUT"

    def on_key_release(self, key, modifiers):
        if self.soldier.is_hurting: return
        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.shift_pressed = False
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
