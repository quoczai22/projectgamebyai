from character_chat import CharacterChat
import arcade
from settings import *
from pixel_text import PixelText  # <--- Import class chữ Pixel

class King(CharacterChat):
    def __init__(self):
        super().__init__(
            base_folder="King/Idle",       
            idle_prefix="0_King_Idle_",    
            idle_start=1,
            idle_end=12
        )

        # Thoại riêng của vua
        self.dialog_lines = [
            "Chào chàng trai!\n",
            "Ta nghe bảo cậu \n muốn giúp ta giải cứu công chúa?",
            "Nếu cậu thành công,\n ta sẽ ban thưởng hậu hĩnh \ncho cậu!",
            "(lối ra ở phía đông của lâu \nđài)",
            "Hãy cẩn thận trên đường đi,\n có rất nhiều quái vật đang \nchờ đợi cậu đấy!"
        ]
        # Không cần self.font_name = "Arial" nữa vì PixelText tự lo

    def draw_interaction_hint(self, soldier):
        """Vẽ nút F trên đầu nếu người chơi đứng gần"""
        if self.check_interaction(soldier) and not self.is_talking:
            button_x = self.center_x
            button_y = self.center_y + 60

            # Arcade 3.x: tạo rect bằng XYWH
            rect = arcade.XYWH(button_x - 15, button_y - 15, 30, 30)

            arcade.draw_rect_filled(rect, arcade.color.WHITE)
            arcade.draw_rect_outline(rect, arcade.color.BLACK, border_width=2)

            # --- SỬA FONT TẠI ĐÂY ---
            # Dùng PixelText thay cho arcade.Text thường
            PixelText(
                "E",
                button_x - 13, # Giữ nguyên vị trí bạn canh chỉnh
                button_y - 22,
                arcade.color.BLACK,
                size=14,       # Đổi tham số '14' thành 'size=14'
                bold=True,
                anchor_x="center"
                # Không cần truyền font_name nữa
            ).draw()

    def on_key_press(self, key, soldier):
        """Xử lý khi nhấn phím F để bật/tắt hội thoại"""
        if not self.check_interaction(soldier):
            self.is_talking = False
            self.dialog_index = 0
            return

        if key == arcade.key.E:
            if not self.is_talking:
                self.is_talking = True
                self.dialog_index = 0
            else:
                self.dialog_index += 1
                if self.dialog_index >= len(self.dialog_lines):
                    self.is_talking = False
                    self.dialog_index = 0