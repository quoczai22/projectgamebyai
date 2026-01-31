import arcade
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, ASSETS_PATH
from castle_level import CastleView

class StoryView(arcade.View):
    def __init__(self):
        super().__init__()
        
        # --- CỐT TRUYỆN ---
        self.story_lines = [
            "Ngày xửa ngày xưa, tại một vương quốc xa xôi...\nCó một vị vua nhân từ tên VH và một công chúa xinh đẹp tên là N.",
            "Hai người sống hạnh phúc bên nhau cho đến một ngày...\nCô công chúa đến tuổi cặp kê. Nhà vua quyết định tổ chức một buổi dạ hội lớn\nđể kén phò mã cho nàng.",
            "Tuy nhiên, trong lúc buổi dạ hội diễn ra...\n một bầy quái vật hung ác đã tấn công vương quốc và bắt cóc công chúa N!",
            "Vua VH vô cùng đau lòng và tuyên bố sẽ ban thưởng hậu hĩnh cho ai giải cứu được công chúa...",
            "Chàng trai quả cảm tên KV, nghe tin về sự kiện này, đã quyết định lên đường đi đến lâu đài nhà vua nhận lĩnh trỉ.\n",
            "Bạn trong vai KV, sẽ phải vượt qua vô số thử thách và chiến đấu với những con quái vật nguy hiểm...",
            "VÀ GIẢI CỨU CÔNG CHÚA!\n(Nhấn Enter để bắt đầu sứ mệnh)"
        ]
        
        # --- BIẾN ĐIỀU KHIỂN ---
        self.current_line_index = 0
        self.text_to_display = ""
        self.full_text = ""
        self.char_index = 0
        self.frame_counter = 0
        self.typing_speed = 3

        # --- FONT ---
        self.pixel_font = "Arial"
        font_path = os.path.join(ASSETS_PATH, "fonts", "PressStart2P-Regular.ttf")
        if os.path.exists(font_path):
            arcade.load_font(font_path)
            self.pixel_font = "Press Start 2P"

        # --- ÂM THANH TYPING (QUAN TRỌNG) ---
        click_path = os.path.join(ASSETS_PATH, "sounds", "click.wav")
        self.click_sound = None
        self.typing_player = None # Biến để quản lý việc phát/dừng nhạc
        
        if os.path.exists(click_path):
            # Load âm thanh vào bộ nhớ
            self.click_sound = arcade.load_sound(click_path)

        self.start_new_line()

    def start_new_line(self):
        if self.current_line_index < len(self.story_lines):
            self.full_text = self.story_lines[self.current_line_index]
            self.text_to_display = ""
            self.char_index = 0
            self.frame_counter = 0

    def stop_typing_sound(self):
        """Hàm tắt âm thanh gõ phím"""
        if self.typing_player:
            # Kiểm tra xem player có hàm pause/delete không (tùy phiên bản Arcade/Pyglet)
            if hasattr(self.typing_player, 'pause'):
                self.typing_player.pause()
            if hasattr(self.typing_player, 'delete'):
                self.typing_player.delete()
            self.typing_player = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(False)

    def on_hide_view(self):
        # Khi rời khỏi màn hình này thì tắt tiếng ngay
        self.stop_typing_sound()

    def on_update(self, delta_time):
        # Kiểm tra xem có đang gõ chữ không
        is_typing = self.char_index < len(self.full_text)

        if is_typing:
            self.frame_counter += 1
            if self.frame_counter % self.typing_speed == 0:
                self.text_to_display += self.full_text[self.char_index]
                self.char_index += 1

            # --- LOGIC ÂM THANH: BẬT ---
            # Nếu đang gõ mà chưa có nhạc -> Bật nhạc (Loop)
            if self.click_sound and self.typing_player is None:
                # Play với loop=True để âm thanh 10s tự lặp lại nếu đoạn văn quá dài
                self.typing_player = self.click_sound.play(loop=True, volume=0.5)
        
        else:
            # --- LOGIC ÂM THANH: TẮT ---
            # Nếu gõ xong rồi mà nhạc vẫn chạy -> Tắt nhạc
            if self.typing_player:
                self.stop_typing_sound()

    def on_draw(self):
        self.clear()
        
        arcade.draw_text(
            "Người dẫn truyện:",
            50, SCREEN_HEIGHT - 100,
            arcade.color.RED,
            font_size=20,
            font_name=self.pixel_font
        )

        lines = self.text_to_display.split('\n')
        start_y = SCREEN_HEIGHT - 150
        gap = 35

        for i, line in enumerate(lines):
            arcade.draw_text(
                line,
                50,
                start_y - (i * gap),
                arcade.color.WHITE,
                font_size=13,
                font_name=self.pixel_font
            )

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
            # Nếu chữ đang chạy -> Bấm Enter để hiện hết ngay
            if self.char_index < len(self.full_text):
                self.text_to_display = self.full_text
                self.char_index = len(self.full_text)
                # QUAN TRỌNG: Tắt tiếng ngay lập tức khi skip
                self.stop_typing_sound()
            
            # Nếu chữ đã hiện hết -> Sang đoạn sau
            else:
                self.stop_typing_sound() # Đảm bảo tắt tiếng
                self.current_line_index += 1
                if self.current_line_index < len(self.story_lines):
                    self.start_new_line()
                else:
                    game_view = CastleView()
                    game_view.setup()
                    self.window.show_view(game_view)
        
        elif key == arcade.key.ESCAPE:
            self.stop_typing_sound()
            arcade.exit()