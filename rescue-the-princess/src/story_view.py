import arcade
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_PATH
from castle_level import CastleView

class StoryView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # --- CỐT TRUYỆN ĐÃ CĂN CHỈNH ---
        # Mình đã thêm nhiều dấu \n hơn để ngắt dòng sớm, tránh tràn màn hình
        self.story_lines = [
            "Ngày xửa ngày xưa, tại một vương quốc xa xôi...\nCó một vị vua nhân từ tên VH\nvà một công chúa xinh đẹp tên là N.",
            
            "Hai người sống hạnh phúc bên nhau cho đến một ngày...\nCô công chúa đến tuổi cặp kê.\nNhà vua quyết định tổ chức một buổi dạ hội lớn\nđể kén phò mã cho nàng.",
            
            "Tuy nhiên, trong lúc buổi dạ hội diễn ra,\nmột bầy quái vật hung ác đã tấn công vương quốc\nvà bắt cóc công chúa N!",
            
            "Vua VH vô cùng đau lòng và tuyên bố\nsẽ ban thưởng hậu hĩnh cho ai giải cứu được công chúa.",
            
            "Chàng trai quả cảm tên KV, nghe tin về sự kiện này,\nđã quyết định lên đường đi đến lâu đài nhà vua\n nhận lĩnh trỉ.",
            
            "Bạn trong vai KV, sẽ phải vượt qua vô số thử thách\nvà chiến đấu với những con quái vật nguy hiểm...",
            
            "VÀ GIẢI CỨU CÔNG CHÚA!\n(Nhấn Enter để bắt đầu sứ mệnh)"
        ]
        
        # --- CÁC BIẾN ĐIỀU KHIỂN ---
        self.current_line_index = 0
        self.text_to_display = ""
        self.full_text = ""
        self.char_index = 0
        self.frame_counter = 0
        self.typing_speed = 3
        
        # --- LOAD FONT ---
        self.pixel_font = "Arial"
        font_path = os.path.join(ASSETS_PATH, "fonts", "PressStart2P-Regular.ttf")
        if os.path.exists(font_path):
            arcade.load_font(font_path)
            self.pixel_font = "Press Start 2P"

        self.start_new_line()

    def start_new_line(self):
        if self.current_line_index < len(self.story_lines):
            self.full_text = self.story_lines[self.current_line_index]
            self.text_to_display = ""
            self.char_index = 0
            self.frame_counter = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(False)

    def on_update(self, delta_time):
        if self.char_index < len(self.full_text):
            self.frame_counter += 1
            if self.frame_counter % self.typing_speed == 0:
                self.text_to_display += self.full_text[self.char_index]
                self.char_index += 1

    def on_draw(self):
        self.clear()
        
        # 1. Vẽ chữ "Người kể chuyện:"
        arcade.draw_text(
            "Người dẫn truyện:",
            50, SCREEN_HEIGHT - 100,
            arcade.color.RED,
            font_size=20,
            font_name=self.pixel_font
        )

        # 2. VẼ NỘI DUNG (GIẢM SIZE CHỮ XUỐNG 14)
        lines = self.text_to_display.split('\n')
        start_y = SCREEN_HEIGHT - 150
        gap = 35  # Giảm khoảng cách dòng một chút cho gọn

        for i, line in enumerate(lines):
            arcade.draw_text(
                line,
                50,
                start_y - (i * gap),
                arcade.color.WHITE,
                font_size=13, # <--- Giảm xuống 13 để chắc chắn vừa khung
                font_name=self.pixel_font
            )

        # 3. Hướng dẫn bấm Enter
        if self.char_index >= len(self.full_text):
            if (self.window.time * 2) % 2 > 1:
                arcade.draw_text(
                    "PRESS ENTER >",
                    SCREEN_WIDTH - 250, 50,
                    arcade.color.GOLD,
                    font_size=12,
                    font_name=self.pixel_font
                )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.char_index < len(self.full_text):
                self.text_to_display = self.full_text
                self.char_index = len(self.full_text)
            else:
                self.current_line_index += 1
                if self.current_line_index < len(self.story_lines):
                    self.start_new_line()
                else:
                    game_view = CastleView()
                    game_view.setup()
                    self.window.show_view(game_view)
        
        elif key == arcade.key.ESCAPE:
            arcade.exit()