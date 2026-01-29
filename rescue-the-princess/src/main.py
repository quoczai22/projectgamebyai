import pygame
import sys
import os
import xml.etree.ElementTree as ET

# --- CẤU HÌNH GAME ---
TITLE = "Mario Style Cave Explorer (Safe Mode)"
WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 32 # Scale lên để dễ nhìn nếu pixel art gốc quá nhỏ

# Màu sắc mặc định
BG_COLOR = (30, 30, 30) # Màu xám tối hang động
PLAYER_COLOR = (255, 50, 50) # Đỏ

# Vật lý Mario
GRAVITY = 0.8
FRICTION = 0.85
ACCELERATION = 0.6
JUMP_FORCE = -17
MAX_SPEED = 7

class RobustMap:
    """
    Class xử lý bản đồ 'thông minh'.
    Nó sẽ cố gắng đọc file TMX. Nếu thiếu ảnh, nó sẽ tự vẽ các ô màu.
    """
    def __init__(self, filename):
        self.filename = filename
        self.tile_size = 16 # Mặc định của Tiled
        self.scale_factor = 2 # Phóng to lên
        self.width = 0
        self.height = 0
        self.tiles = {} # Lưu vị trí các ô gạch: (x, y) -> gid
        self.solid_rects = [] # Danh sách các khối cứng để va chạm
        
        self.load_map()

    def load_map(self):
        print(f"--- Đang tải bản đồ: {self.filename} ---")
        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()
            
            # 1. Lấy thông tin cơ bản
            self.map_w = int(root.attrib.get('width'))
            self.map_h = int(root.attrib.get('height'))
            self.tile_size = int(root.attrib.get('tilewidth'))
            
            # Tính toán kích thước thực tế sau khi phóng to
            final_tile_size = self.tile_size * self.scale_factor
            self.width = self.map_w * final_tile_size
            self.height = self.map_h * final_tile_size
            
            # 2. Đọc dữ liệu các Layer (ưu tiên CSV)
            # Chúng ta sẽ gộp tất cả layer lại thành một map va chạm cho đơn giản
            for layer in root.findall('layer'):
                data = layer.find('data')
                if data is not None and data.attrib.get('encoding') == 'csv':
                    csv_text = data.text.strip()
                    # Chuyển chuỗi CSV thành mảng số
                    rows = csv_text.split('\n')
                    
                    # Duyệt qua từng ô để xây dựng map
                    y_idx = 0
                    tile_count = 0
                    
                    # Dọn dẹp chuỗi và tách số
                    clean_ids = [int(gid) for gid in csv_text.replace('\n', '').split(',') if gid.strip()]
                    
                    for i, gid in enumerate(clean_ids):
                        if gid != 0: # 0 là ô trống
                            # Tính tọa độ x, y
                            x = (i % self.map_w) * final_tile_size
                            y = (i // self.map_w) * final_tile_size
                            
                            self.tiles[(x, y)] = gid
                            self.solid_rects.append(pygame.Rect(x, y, final_tile_size, final_tile_size))
            
            print(f"-> Đã load thành công {len(self.solid_rects)} ô gạch từ file XML/TMX.")
            print("-> Chế độ: RAW XML (Chạy được ngay cả khi thiếu ảnh)")

        except Exception as e:
            print(f"LỖI NGHIÊM TRỌNG KHI ĐỌC MAP: {e}")
            # Tạo map rỗng để không crash
            self.width = WIDTH
            self.height = HEIGHT

    def render(self, surface, camera_x, camera_y):
        """Vẽ map dựa trên dữ liệu đã đọc"""
        final_tile_size = self.tile_size * self.scale_factor
        
        # Chỉ vẽ những ô đang nằm trong màn hình (Tối ưu hóa)
        screen_rect = pygame.Rect(camera_x, camera_y, WIDTH, HEIGHT)
        
        for rect in self.solid_rects:
            if screen_rect.colliderect(rect):
                # Tính vị trí vẽ trên màn hình
                draw_x = rect.x - camera_x
                draw_y = rect.y - camera_y
                
                # Giả lập màu sắc: Dựa vào tọa độ để tạo chút ngẫu nhiên cho đỡ chán
                # Vì ta không có ảnh, ta dùng màu nâu/xám để giả lập đất/đá
                color_val = (100 + (rect.x % 50), 80 + (rect.y % 40), 50) 
                pygame.draw.rect(surface, color_val, (draw_x, draw_y, final_tile_size, final_tile_size))
                # Vẽ viền cho rõ
                pygame.draw.rect(surface, (50, 30, 20), (draw_x, draw_y, final_tile_size, final_tile_size), 1)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, map_obj):
        super().__init__()
        self.width = 24
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.map = map_obj
        self.facing_right = True

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Di chuyển trái phải (có quán tính)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= ACCELERATION
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += ACCELERATION
            self.facing_right = True
        else:
            # Ma sát trượt khi không bấm nút
            self.vel_x *= FRICTION

        # Giới hạn tốc độ
        if self.vel_x > MAX_SPEED: self.vel_x = MAX_SPEED
        if self.vel_x < -MAX_SPEED: self.vel_x = -MAX_SPEED
        
        # Ngăn trượt vô tận (nếu quá chậm thì dừng hẳn)
        if abs(self.vel_x) < 0.1: self.vel_x = 0

        # Nhảy
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY

    def move_and_collide(self):
        # 1. Di chuyển theo trục X
        self.rect.x += int(self.vel_x)
        hits = self.get_collisions()
        for tile in hits:
            if self.vel_x > 0: # Đang đi sang phải -> Đụng cạnh trái của tường
                self.rect.right = tile.left
                self.vel_x = 0
            elif self.vel_x < 0: # Đang đi sang trái -> Đụng cạnh phải của tường
                self.rect.left = tile.right
                self.vel_x = 0

        # 2. Di chuyển theo trục Y
        self.rect.y += int(self.vel_y)
        self.on_ground = False # Mặc định là đang bay
        hits = self.get_collisions()
        for tile in hits:
            if self.vel_y > 0: # Đang rơi xuống -> Đụng đất
                self.rect.bottom = tile.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0: # Đang nhảy lên -> Đụng trần
                self.rect.top = tile.bottom
                self.vel_y = 0

        # Chết nếu rơi khỏi map
        if self.rect.y > self.map.height + 100:
            self.respawn()

    def get_collisions(self):
        # Chỉ kiểm tra va chạm với các tile ở gần player (Tối ưu hiệu năng)
        # Thay vì check 1000 ô gạch, chỉ check các ô xung quanh
        nearby_tiles = []
        for tile_rect in self.map.solid_rects:
            # Chỉ check nếu tile nằm trong phạm vi 100px quanh người chơi
            if abs(tile_rect.x - self.rect.x) < 100 and abs(tile_rect.y - self.rect.y) < 100:
                if self.rect.colliderect(tile_rect):
                    nearby_tiles.append(tile_rect)
        return nearby_tiles

    def respawn(self):
        self.rect.x = 100
        self.rect.y = 100
        self.vel_x = 0
        self.vel_y = 0

    def draw(self, surface, camera_x, camera_y):
        # Vẽ người chơi
        draw_pos = (self.rect.x - camera_x, self.rect.y - camera_y)
        pygame.draw.rect(surface, PLAYER_COLOR, (*draw_pos, self.width, self.height))
        
        # Vẽ mắt để biết hướng nhìn
        eye_color = (255, 255, 255)
        pupil_color = (0, 0, 0)
        
        if self.facing_right:
            eye_x = draw_pos[0] + 14
        else:
            eye_x = draw_pos[0] + 4
            
        pygame.draw.rect(surface, eye_color, (eye_x, draw_pos[1] + 6, 6, 6))
        
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # --- TÌM FILE TMX TỰ ĐỘNG ---
        # Ưu tiên các file map bạn đã gửi
        possible_maps = ["HallWayNightCave.tmx", "finalsence.tmx", "examplecave.tmx", "HallwayDayNight.tmx"]
        selected_map = None
        
        for m in possible_maps:
            if os.path.exists(m):
                selected_map = m
                break
        
        if not selected_map:
            # Nếu không tìm thấy file nào, tạo một file map demo
            print("Không tìm thấy file .tmx nào trong thư mục này.")
            print("Vui lòng copy file .tmx vào cùng thư mục với file .py")
            # Tạo dữ liệu giả để game không crash
            sys.exit()
            
        self.map = RobustMap(selected_map)
        self.player = Player(100, 100, self.map)
        
        self.camera_x = 0
        self.camera_y = 0

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.player.update()
        
        # --- CAMERA LOGIC ---
        # Camera đi theo người chơi, nhưng mượt hơn
        target_x = self.player.rect.centerx - WIDTH // 2
        target_y = self.player.rect.centery - HEIGHT // 2
        
        # Lerp (Làm mượt chuyển động camera)
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Giới hạn camera không chạy ra ngoài map
        self.camera_x = max(0, min(self.camera_x, self.map.width - WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map.height - HEIGHT))

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Vẽ map
        self.map.render(self.screen, int(self.camera_x), int(self.camera_y))
        
        # Vẽ player
        self.player.draw(self.screen, int(self.camera_x), int(self.camera_y))
        
        # Vẽ hướng dẫn
        font = pygame.font.SysFont('Arial', 18)
        text = font.render(f"FPS: {int(self.clock.get_fps())} | Map: {self.map.filename}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()