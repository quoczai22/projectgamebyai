import arcade
import os
from settings import *
from day_level import DayView 

class CastleView(arcade.View):
    def __init__(self):
        super().__init__()
        self.tile_map = None
        self.scene = None
        self.camera = None
        
        # --- BIẾN DI CHUYỂN ---
        self.camera_speed = 10
        self.view_left = 0
        self.view_bottom = 0 # Luôn bằng 0 để khóa trục Y
        self.left_pressed = False
        self.right_pressed = False
        self.map_width_pixels = 0 
        
        # --- BIẾN HIỆU ỨNG FADE ---
        self.fade_alpha = 255  # 255 = Đen thui (Bắt đầu vào game là đen)
        self.fade_state = "FADE_IN" # Các trạng thái: FADE_IN, PLAYING, FADE_OUT

    def setup(self):
        # Tên map của bạn
        map_path = os.path.join(ASSETS_PATH, "maps", "Castle_of_king.tmx")
        layer_options = {"wall": {"use_spatial_hash": True}}

        try:
            self.tile_map = arcade.load_tilemap(map_path, scaling=TILE_SCALING, layer_options=layer_options)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.camera = arcade.Camera2D()
            self.map_width_pixels = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
        except FileNotFoundError:
            print(f"Lỗi map: {map_path}")

        if self.tile_map and self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        else:
            arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        
        # 1. Kích hoạt camera
        if self.camera:
            self.camera.use()
            
        # 2. Vẽ Map
        if self.scene:
            self.scene.draw()
            
        # 3. Vẽ chữ hướng dẫn ở cuối map
        if self.view_left >= (self.map_width_pixels - SCREEN_WIDTH - 50):
            arcade.draw_text("ENTER -> DAY LEVEL", self.view_left + 300, 300, arcade.color.WHITE, 20, bold=True)

        # 4. VẼ HIỆU ỨNG MÀN ĐEN (Đã sửa lỗi cho Arcade 3.0)
        if self.fade_alpha > 0:
            # Tạo hình chữ nhật bao phủ màn hình tại vị trí camera đang đứng
            rect = arcade.LBWH(self.view_left, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            # Vẽ hình chữ nhật màu đen với độ trong suốt alpha
            arcade.draw_rect_filled(rect, (0, 0, 0, int(self.fade_alpha)))

    def on_update(self, delta_time):
        fade_speed = 5 # Tốc độ sáng/tối (chỉnh số này nếu muốn nhanh chậm)

        # --- A. GIAI ĐOẠN 1: MỚI VÀO (LÀM SÁNG MÀN HÌNH) ---
        if self.fade_state == "FADE_IN":
            self.fade_alpha -= fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_state = "PLAYING" # Sáng xong rồi thì cho chơi
        
        # --- B. GIAI ĐOẠN 2: ĐANG CHƠI (CHO PHÉP DI CHUYỂN) ---
        elif self.fade_state == "PLAYING":
            if self.left_pressed: self.view_left -= self.camera_speed
            if self.right_pressed: self.view_left += self.camera_speed

            # Giới hạn không chạy ra ngoài map
            if self.view_left < 0: self.view_left = 0     
            max_right = self.map_width_pixels - SCREEN_WIDTH
            if self.view_left > max_right: self.view_left = max_right

        # --- C. GIAI ĐOẠN 3: CHUYỂN CẢNH (LÀM TỐI MÀN HÌNH) ---
        elif self.fade_state == "FADE_OUT":
            self.fade_alpha += fade_speed
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                # Khi đã đen thui thì mới chuyển map
                self.switch_to_next_level()

        # Cập nhật vị trí Camera
        center_x = self.view_left + (SCREEN_WIDTH / 2)
        center_y = (SCREEN_HEIGHT / 2)
        if self.camera: self.camera.position = (center_x, center_y)

    def switch_to_next_level(self):
        """ Hàm gọi map tiếp theo """
        print("Chuyển sang Day View...")
        next_view = DayView()
        next_view.setup()
        self.window.show_view(next_view)

    def on_key_press(self, key, modifiers):
        # Di chuyển bằng Mũi tên hoặc A/D
        if key == arcade.key.LEFT or key == arcade.key.A: self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D: self.right_pressed = True
        
        # Nhấn Enter để chuyển cảnh
        elif key == arcade.key.ENTER:
            max_right = self.map_width_pixels - SCREEN_WIDTH
            # Chỉ chuyển khi đang chơi và đang đứng ở cuối map
            if self.view_left >= max_right - 10 and self.fade_state == "PLAYING":
                self.fade_state = "FADE_OUT" # Kích hoạt hiệu ứng tối dần

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A: self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D: self.right_pressed = False