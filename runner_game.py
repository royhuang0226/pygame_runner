import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 遊戲常數設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

# 顏色定義 (RGB)
WHITE = (255, 255, 255)
BG_COLOR = (240, 240, 240)
PLAYER_COLOR = (50, 150, 255)    # 藍色
OBSTACLE_COLOR = (255, 80, 80)   # 紅色
GROUND_COLOR = (100, 100, 100)   # 灰色
TEXT_COLOR = (50, 50, 50)

# 建立遊戲視窗與時鐘
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("簡單跑酷遊戲")
clock = pygame.time.Clock()

# 字型設定 (使用系統預設字型)
font = pygame.font.SysFont("arial", 30)

# --- 遊戲物件類別 ---

class Player:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 100
        self.y = SCREEN_HEIGHT - 110  # 剛好站在地面上
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 跳躍與重力機制
        self.gravity = 0.8
        self.jump_speed = -16
        self.velocity_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True

    def update(self):
        # 應用重力
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        
        # 地面碰撞限制
        floor_y = SCREEN_HEIGHT - 50 - self.height
        if self.y >= floor_y:
            self.y = floor_y
            self.velocity_y = 0
            self.is_jumping = False
            
        # 更新碰撞矩形位置
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, self.rect)


class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = random.randint(40, 80)  # 隨機高度增加挑戰性
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - 50 - self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 7

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, OBSTACLE_COLOR, self.rect)


# --- 遊戲主程式與狀態 ---

def main():
    player = Player()
    obstacles = []
    score = 0
    game_over = False
    
    # 自訂事件：每 1.2 秒 (1200毫秒) 生成一個障礙物
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1200)

    # 遊戲主迴圈
    while True:
        # 1. 事件偵測 (Event Loop)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # 遊戲結束時按下空白鍵重新開始
                        return main() 
                    else:
                        player.jump()
                        
            # 時間到了就生成新障礙物
            if event.type == obstacle_timer and not game_over:
                obstacles.append(Obstacle())

        # 2. 遊戲狀態更新 (Update)
        if not game_over:
            player.update()
            
            # 更新所有障礙物
            for obstacle in obstacles[:]:
                obstacle.update()
                
                # 如果障礙物走出左邊邊界，就刪除並加分
                if obstacle.x < -obstacle.width:
                    obstacles.remove(obstacle)
                    score += 1
                
                # 碰撞偵測：利用 rect.colliderect
                if player.rect.colliderect(obstacle.rect):
                    game_over = True

        # 3. 畫面繪製 (Render/Draw)
        screen.fill(BG_COLOR)  # 清空畫面
        
        # 畫地面
        pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # 畫角色與障礙物
        player.draw()
        for obstacle in obstacles:
            obstacle.draw()
            
        # 畫分數
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 20))
        
        # 畫遊戲結束畫面
        if game_over:
            over_text = font.render("GAME OVER - Press SPACE to Restart", True, OBSTACLE_COLOR)
            # 將文字居中顯示
            text_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(over_text, text_rect)

        # 更新視窗、控制幀率
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()