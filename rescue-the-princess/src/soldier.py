from character import Character

class Soldier(Character):
    def __init__(self):
        super().__init__(
            base_folder="Valkyrie_2/PNG/PNG Sequences", 
            prefix="0_Valkyrie",
            
            # --- CÁC THÔNG SỐ CỦA RIÊNG SOLDIER ---
            # Bạn nhớ kiểm tra folder xem có đúng số lượng này không nhé
            idle_count=18,
            walk_count=24,
            run_count=12,
            jump_count=6,
            
            # Animation tấn công
            slash_count=12,      
            air_slash_count=12,
            hurt_count=12
        )