import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import arcade
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from menu_view import MenuView

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)

    def setup(self):
        start_view = MenuView()
        self.show_view(start_view)

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
