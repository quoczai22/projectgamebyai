import arcade
import os
from settings import *
from hallway_day_night import HallwayDayNightView 

class DayView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera = None; self.tile_map = None; self.scene = None
        self.camera_speed = 10; self.view_left = 0
        self.left_pressed = False; self.right_pressed = False
        self.map_width_pixels = 0
        
        # Biến Fade
        self.fade_alpha = 255
        self.fade_state = "FADE_IN"

    def setup(self):
        map_path = os.path.join(ASSETS_PATH, "maps", "Day.tmx")
        layer_options = {"wall": {"use_spatial_hash": True}, "Ground": {"use_spatial_hash": True}}
        try:
            self.tile_map = arcade.load_tilemap(map_path, scaling=TILE_SCALING, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.camera = arcade.Camera2D()
            self.map_width_pixels = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
        except: print(f"Lỗi map: {map_path}")
        
        if self.tile_map.background_color: arcade.set_background_color(self.tile_map.background_color)
        else: arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        self.clear()
        if self.camera: self.camera.use()
        if self.scene: self.scene.draw()
        
        if self.view_left >= (self.map_width_pixels - SCREEN_WIDTH - 50):
            arcade.draw_text("ENTER -> TIEP TUC", self.view_left + 300, 300, arcade.color.WHITE, 20, bold=True)

        # Vẽ màn đen fade
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

        elif self.fade_state == "FADE_OUT":
            self.fade_alpha += fade_speed
            if self.fade_alpha >= 255: self.fade_alpha = 255; self.switch_to_next_level()

        if self.camera: self.camera.position = (self.view_left + SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    def switch_to_next_level(self):
        next_view = HallwayDayNightView()
        next_view.setup()
        self.window.show_view(next_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A: self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D: self.right_pressed = True
        elif key == arcade.key.ENTER:
            if self.view_left >= (self.map_width_pixels - SCREEN_WIDTH - 50) and self.fade_state == "PLAYING":
                self.fade_state = "FADE_OUT"

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A: self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D: self.right_pressed = False