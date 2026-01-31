from character_chat import CharacterChat
import arcade
from settings import *

class King(CharacterChat):
    def __init__(self):
        super().__init__(
            base_folder="King/Idle",       
            idle_prefix="0_King_Idle_",    
            idle_start=1,                  
            idle_end=4 
        )

        self.dialog_lines = [
            "Chào chiến binh KV!",
            "Ta là vua của vương quốc này.",
            "Hãy chuẩn bị cho hành trình giải cứu công chúa!"
        ]
        self.dialog_index = 0
        self.is_talking = False

    def draw_dialog(self):
        if self.is_talking and self.dialog_index < len(self.dialog_lines):
            dialog = arcade.Text(
                self.dialog_lines[self.dialog_index],
                self.center_x + 50,
                self.center_y + 100,
                arcade.color.WHITE,
                14,
                width=250,
                multiline=True
            )
            dialog.draw()

    def on_key_press(self, key, soldier):
        if key == arcade.key.F and self.check_interaction(soldier):
            self.is_talking = True
            self.dialog_index += 1
            if self.dialog_index > len(self.dialog_lines) - 1:
                self.dialog_index = 0
