import arcade
import os
from settings import *
from day_level import DayView 
from soldier import Soldier
from king import King
from sound_manager import SoundManager

class CastleView(arcade.View):
    def __init__(self, sound_manager=None):
        super().__init__()
        self.sound_manager = sound_manager 
        
        self.tile_map = None
        self.scene = None
        self.camera = None
        
        self.soldier = None
        self.soldier_engine = None
        self.king = None
        
        self.view_left = 0
        self.map_width_pixels = 0 
        
        self.fade_alpha = 255
        self.fade_state = "FADE_IN"
        self.step_timer = 0 
        self.current_step_player = None

        # Text hướng dẫn
        self.guide_text = arcade.Text(
            "NHẤN ENTER ĐỂ MỞ CỔNG",
            0, 0,
            arcade.color.WHITE,
            20,
            bold=True
        )

    def setup(self):
        # 1. LOAD MAP
        map_path = os.path.join(ASSETS_PATH, "maps", "Castle_of_king.tmx")
        try:
            self.tile_map = arcade.load_tilemap(
                map_path,
                scaling=TILE_SCALING,
                layer_options={"wall_stand": {"use_spatial_hash": False}}
            )
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.map_width_pixels = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
            print("-> Map Castle load thành công!")
        except FileNotFoundError:
            print(f"!!! LỖI KHÔNG TÌM THẤY MAP: {map_path}")
            return

        # 2. TẠO NHÂN VẬT
        self.soldier = Soldier()
        self.soldier.center_x, self.soldier.center_y = 400, 200
        self.scene.add_sprite("Soldier", self.soldier)

        self.king = King()
        self.king.center_x, self.king.center_y = 210, 230
        self.scene.add_sprite("King", self.king)

        # 3. PHYSICS & CAMERA
        walls_list = [self.scene["wall_stand"]] if "wall_stand" in self.scene else []
        self.soldier_engine = arcade.PhysicsEnginePlatformer(
            self.soldier,
            gravity_constant=GRAVITY,
            walls=walls_list
        )

        self.camera = arcade.Camera2D()
        self.view_left = 0
        self.camera.position = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        arcade.set_background_color(self.tile_map.background_color or arcade.color.BLACK)

        # 4. PHÁT NHẠC NỀN
        if self.sound_manager:
            self.sound_manager.play_music("castle_music.wav")

    def on_draw(self):
        self.clear()
        if self.camera: self.camera.use()
        if self.scene: self.scene.draw()

        if self.king:
            self.king.draw_dialog()
            self.king.draw_interaction_hint(self.soldier)

        if self.soldier and self.soldier.center_x >= (self.map_width_pixels - 300):
            self.guide_text.x, self.guide_text.y = self.view_left + 300, 300
            self.guide_text.draw()

        if self.fade_alpha > 0:
            arcade.draw_rect_filled(
                arcade.LBWH(self.view_left, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
                (0, 0, 0, int(self.fade_alpha))
            )

    def handle_step_sound(self, delta_time):
        """Quản lý âm thanh bước chân"""
        if self.soldier.change_x and self.soldier_engine.can_jump() and self.soldier.is_running:
            self.step_timer += delta_time
            if self.step_timer > 0.25:
                if self.current_step_player:
                    self.current_step_player.pause()
                    self.current_step_player.delete()
                if self.sound_manager:
                    self.current_step_player = self.sound_manager.play_effect("step", volume_override=0.5)
                self.step_timer = 0
        else:
            self.step_timer = 0.3
            if self.current_step_player:
                self.current_step_player.pause()
                self.current_step_player.delete()
                self.current_step_player = None

    def on_update(self, delta_time):
        fade_speed = 5
        if self.fade_state == "FADE_IN":
            self.fade_alpha = max(0, self.fade_alpha - fade_speed)
            if self.fade_alpha == 0: self.fade_state = "PLAYING"

        elif self.fade_state == "PLAYING":
            self.soldier_engine.update()
            self.scene.update_animation(delta_time, ["Soldier", "King"])
            self.handle_step_sound(delta_time)

            # Camera logic
            target_x = max(0, min(self.soldier.center_x - SCREEN_WIDTH/2,
                                  self.map_width_pixels - SCREEN_WIDTH))
            self.view_left = arcade.math.lerp(self.view_left, target_x, 0.1)

            # Giới hạn map
            self.soldier.left = max(0, self.soldier.left)
            self.soldier.right = min(self.map_width_pixels, self.soldier.right)
            if self.soldier.center_y < -100:
                self.soldier.center_x, self.soldier.center_y, self.soldier.change_y = 400, 200, 0

        elif self.fade_state == "FADE_OUT":
            self.fade_alpha = min(255, self.fade_alpha + fade_speed)
            if self.fade_alpha == 255: self.switch_to_next_level()

        self.camera.position = (int(self.view_left + SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2))

    def switch_to_next_level(self):
        if self.sound_manager: self.sound_manager.stop_music()
        next_view = DayView(self.sound_manager)
        next_view.setup()
        self.window.show_view(next_view)

    def on_key_press(self, key, modifiers):
        if self.fade_state != "PLAYING" or not self.soldier: return

        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.soldier.is_running = True
            if self.soldier.change_x:
                self.soldier.change_x = PLAYER_RUN_SPEED if self.soldier.change_x > 0 else -PLAYER_RUN_SPEED

        elif key in (arcade.key.UP, arcade.key.SPACE, arcade.key.W):
            if self.soldier_engine.can_jump():
                self.soldier.change_y = PLAYER_JUMP_SPEED

        elif key in (arcade.key.LEFT, arcade.key.A):
            self.soldier.change_x = - (PLAYER_RUN_SPEED if self.soldier.is_running else PLAYER_WALK_SPEED)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.soldier.change_x = (PLAYER_RUN_SPEED if self.soldier.is_running else PLAYER_WALK_SPEED)

        elif key == arcade.key.F:
            self.soldier.attack()
            if self.sound_manager: self.sound_manager.play_effect("sword")

        elif key == arcade.key.ENTER and self.soldier.center_x >= (self.map_width_pixels - 300):
            if self.sound_manager: self.sound_manager.play_effect("door")
            self.fade_state = "FADE_OUT"

        if self.king: self.king.on_key_press(key, self.soldier)

    def on_key_release(self, key, modifiers):
        if not self.soldier: return
        if key in (arcade.key.LSHIFT, arcade.key.RSHIFT):
            self.soldier.is_running = False
            if self.soldier.change_x:
                self.soldier.change_x = PLAYER_WALK_SPEED if self.soldier.change_x > 0 else -PLAYER_WALK_SPEED
        elif key in (arcade.key.LEFT, arcade.key.A) and self.soldier.change_x < 0:
            self.soldier.change_x = 0
        elif key in (arcade.key.RIGHT, arcade.key.D) and self.soldier.change_x > 0:
            self.soldier.change_x = 0
