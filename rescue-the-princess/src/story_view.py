import arcade
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from sound_manager import SoundManager
from castle_level import CastleView
from pixel_text import PixelText # Import class chữ mới

class StoryView(arcade.View):
    def __init__(self, sound_manager: SoundManager):
        super().__init__()
        self.sound_manager = sound_manager
        
        self.story_lines = [
            "Ngày xửa ngày xưa, tại một vương quốc xa xôi...\nCó một vị vua nhân từ tên VH và một công chúa xinh đẹp tên là N.",
            "Hai người sống hạnh phúc bên nhau cho đến một ngày...\nCô công chúa đến tuổi cặp kê. Nhà vua quyết định tổ chức một buổi dạ hội lớn\nđể kén phò mã cho nàng.",
            "Tuy nhiên, trong lúc buổi dạ hội diễn ra...\n một bầy quái vật hung ác đã tấn công vương quốc và bắt cóc công chúa N!",
            "Vua VH vô cùng đau lòng và tuyên bố sẽ ban thưởng hậu hĩnh cho ai giải cứu được công chúa...",
            "Chàng trai quả cảm tên KV, nghe tin về sự kiện này, đã quyết định lên đường đi đến lâu đài nhà vua nhận lĩnh chỉ.\n",
            "Bạn trong vai KV, sẽ phải vượt qua vô số thử thách và chiến đấu với những con quái vật nguy hiểm...",
            "VÀ GIẢI CỨU CÔNG CHÚA!\n(Nhấn Enter để bắt đầu sứ mệnh)"
        ]
        
        self.current_line_index = 0
        self.text_to_display = ""
        self.full_text = ""
        self.char_index = 0
        self.frame_counter = 0
        self.typing_speed = 3
        
        self.typing_player = None # Quản lý âm thanh loop

        # Text tĩnh
        self.narrator_text = PixelText("Người dẫn truyện:", 50, SCREEN_HEIGHT - 100, arcade.color.RED, size=20)
        self.press_enter_text = PixelText("PRESS ENTER >", SCREEN_WIDTH - 250, 50, arcade.color.GOLD, size=12)
        
        self.text_objects = []
        self.start_new_line()

    def start_new_line(self):
        if self.current_line_index < len(self.story_lines):
            self.full_text = self.story_lines[self.current_line_index]
            self.text_to_display = ""
            self.char_index = 0
            self.frame_counter = 0
            self.text_objects = []

    def stop_typing_sound(self):
        """Tắt âm thanh gõ phím an toàn"""
        if self.typing_player:
            try:
                if hasattr(self.typing_player, 'pause'): self.typing_player.pause()
                if hasattr(self.typing_player, 'delete'): self.typing_player.delete()
            except: pass
            self.typing_player = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(False)

    def on_hide_view(self):
        self.stop_typing_sound()

    def on_update(self, delta_time):
        is_typing = self.char_index < len(self.full_text)

        if is_typing:
            self.frame_counter += 1
            if self.frame_counter % self.typing_speed == 0:
                self.text_to_display += self.full_text[self.char_index]
                self.char_index += 1
                
                # Cập nhật hiển thị text
                self.text_objects = []
                lines = self.text_to_display.split('\n')
                start_y = SCREEN_HEIGHT - 150
                for i, line in enumerate(lines):
                    self.text_objects.append(
                        PixelText(line, 50, start_y - (i * 35), arcade.color.WHITE, size=13)
                    )

            # Bật âm thanh loop nếu chưa bật
            if self.typing_player is None:
                self.typing_player = self.sound_manager.play_effect("click", loop=True)
        else:
            # Tắt âm thanh nếu đã gõ xong
            if self.typing_player:
                self.stop_typing_sound()

    def on_draw(self):
        self.clear()
        self.narrator_text.draw()
        for obj in self.text_objects: obj.draw()

        if self.char_index >= len(self.full_text):
            if (self.window.time * 2) % 2 > 1:
                self.press_enter_text.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            if self.char_index < len(self.full_text):
                # Skip: Hiện hết chữ ngay lập tức
                self.text_to_display = self.full_text
                self.char_index = len(self.full_text)
                self.stop_typing_sound()
                
                # Vẽ lại full text
                self.text_objects = []
                lines = self.text_to_display.split('\n')
                start_y = SCREEN_HEIGHT - 150
                for i, line in enumerate(lines):
                    self.text_objects.append(
                        PixelText(line, 50, start_y - (i * 35), arcade.color.WHITE, size=13)
                    )
            else:
                self.stop_typing_sound()
                self.current_line_index += 1
                if self.current_line_index < len(self.story_lines):
                    self.start_new_line()
                else:
                    # Chuyển sang Castle Level
                    try:
                        game_view = CastleView(self.sound_manager)
                    except:
                        # Fallback nếu CastleView chưa update __init__
                        game_view = CastleView()
                        game_view.sound_manager = self.sound_manager
                        
                    game_view.setup()
                    self.window.show_view(game_view)
                    
        elif key == arcade.key.ESCAPE:
            self.stop_typing_sound()
            arcade.exit()