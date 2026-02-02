import os
import pyglet
import arcade
from settings import ASSETS_PATH

class SoundManager:
    def __init__(self):
        # --- NHẠC NỀN ---
        self.bg_player = None
        self.music_volume = 0.5
        self.is_muted_music = False

        # --- ÂM THANH HIỆU ỨNG ---
        self.effect_volume = 0.5
        self.is_muted_effect = False
        
        # Đăng ký tất cả âm thanh ở đây
        self.sounds = {
            "click": self.load_sound("sounds/click.wav"),
            "door": self.load_sound("sounds/open_door.wav"),
            
            # --- THÊM CÁC FILE MỚI VÀO ĐÂY ---
            "step": self.load_sound("sounds/armor_step.wav"),  # Tiếng bước chân
            "sword": self.load_sound("sounds/sword_swing.wav") # Tiếng chém
        }

    def load_sound(self, relative_path):
        path = os.path.join(ASSETS_PATH, relative_path)
        if os.path.exists(path):
            return arcade.load_sound(path)
        print(f"!!! Warning: Không tìm thấy file âm thanh: {path}")
        return None

    # --- XỬ LÝ NHẠC NỀN (MUSIC) ---
    def play_music(self, filename):
        path = os.path.join(ASSETS_PATH, "sounds", filename)
        if os.path.exists(path):
            if self.bg_player:
                self.stop_music() # Dừng nhạc cũ trước khi phát mới
                
            source = pyglet.media.load(path, streaming=False)
            self.bg_player = pyglet.media.Player()
            self.bg_player.queue(source)
            self.bg_player.loop = True
            self.bg_player.volume = 0.0 if self.is_muted_music else self.music_volume
            self.bg_player.play()

    def stop_music(self):
        if self.bg_player:
            self.bg_player.pause()
            self.bg_player.delete()
            self.bg_player = None

    def set_music_volume(self, vol):
        self.music_volume = max(0.0, min(1.0, vol))
        if self.bg_player and not self.is_muted_music:
            self.bg_player.volume = self.music_volume

    def toggle_music_mute(self):
        self.is_muted_music = not self.is_muted_music
        if self.bg_player:
            self.bg_player.volume = 0.0 if self.is_muted_music else self.music_volume

    # --- XỬ LÝ HIỆU ỨNG (SFX) ---
    def set_effect_volume(self, vol):
        self.effect_volume = max(0.0, min(1.0, vol))

    def toggle_effect_mute(self):
        self.is_muted_effect = not self.is_muted_effect

    # --- [QUAN TRỌNG] ĐÃ CẬP NHẬT ĐỂ HỖ TRỢ VOLUME RIÊNG ---
    def play_effect(self, name, loop=False, volume_override=None):
        """
        - name: Key tên âm thanh trong self.sounds (ví dụ: 'step', 'door')
        - loop: Lặp hay không
        - volume_override: Nếu truyền vào, sẽ dùng volume này thay vì volume chung.
                           (Ví dụ: tiếng bước chân muốn nhỏ hơn tiếng chém)
        """
        if name in self.sounds and self.sounds[name]:
            if not self.is_muted_effect:
                # Tính toán âm lượng cuối cùng
                final_volume = self.effect_volume
                
                # Nếu có volume riêng thì nhân với volume tổng (để vẫn chỉnh to nhỏ được)
                if volume_override is not None:
                    final_volume = self.effect_volume * volume_override

                return self.sounds[name].play(volume=final_volume, loop=loop)
        return None