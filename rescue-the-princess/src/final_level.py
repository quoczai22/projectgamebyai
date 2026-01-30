import arcade
import os
from settings import *

class FinalView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera = None; self.tile_map = None; self.scene = None
        self.camera_speed = 10; self.view_left = 0
        self.left_pressed = False; self.right_pressed = False
        self.map_width_pixels = 0
        self.fade_alpha = 255; self.fade_state = "FADE_IN"

    def setup(self):
        map_path = os.path.join(ASSETS_PATH, "maps", "finalsence.tmx")
        layer_options = {"wall": {"use_spatial_hash": True}, "Ground": {"use_spatial_hash": True}}
        try:
            self.tile_map = arcade.load_tilemap(map_path, scaling=TILE_SCALING, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.camera = arcade.Camera2D()
            self.map_width_pixels = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
        except: print(f"Lỗi map: {map_path}")
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        if self.camera: self.camera.use()
        if self.scene: self.scene.draw()
        
        if self.view_left >= (self.map_width_pixels - SCREEN_WIDTH - 50):
            arcade.draw_text("WINNER!", self.view_left + 400, 350, arcade.color.GOLD, 50, bold=True)
            arcade.draw_text("ESC to Quit", self.view_left + 400, 300, arcade.color.WHITE, 15)

        if self.fade_alpha > 0:
            rect = arcade.LBWH(self.view_left, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            arcade.draw_rect_filled(rect, (0, 0, 0, int(self.fade_alpha)))

    def on_update(self, delta_time):
        fade_speed = 5
        if self.fade_state == "FADE_IN":
            self.fade_alpha -= fade_speed
            if self.fade_alpha <= 0: self.fade_alpha = 0; self.fade_state = "PLAYING"
        
        elif self.fade_state == "PLAYING":
            if self.left_pressed: self.view_left -= self.camera_speed
            if self.right_pressed: self.view_left += self.camera_speed
            if self.view_left < 0: self.view_left = 0
            if self.view_left > (self.map_width_pixels - SCREEN_WIDTH): self.view_left = self.map_width_pixels - SCREEN_WIDTH

        if self.camera: self.camera.position = (self.view_left + SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A: self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D: self.right_pressed = True
        elif key == arcade.key.ESCAPE: arcade.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A: self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D: self.right_pressed = False