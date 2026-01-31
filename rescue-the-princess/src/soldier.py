from character import Character

class Soldier(Character):
    def __init__(self):
        super().__init__(base_folder="Valkyrie_2/PNG/PNG Sequences", prefix="0_Valkyrie")
        # Soldier sẽ nhận input từ user (keyboard)
