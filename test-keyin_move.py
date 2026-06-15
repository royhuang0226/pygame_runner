import pygame
import sys
import random

# 1. 初始化 pygame
pygame.init()

# 2. 設定視窗與字型
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("鍵盤輸入測試 - 文字往上飄")
font = pygame.font.SysFont("arial", 40)

clock = pygame.time.Clock()

# 用一個列表來儲存畫面上所有正在飄動的文字
# 裡面每個元素會是一個字典，紀錄文字內容和座標： {"char": "A", "x": 200, "y": 300}
floating_texts = []

# 3. 遊戲主迴圈
while True:
    # --- 事件偵測區 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.unicode: 
                # 每按一個鍵，就產生一個新文字，放在列表裡面
                # 讓它從畫面最底部開始，X 座標可以在中間稍微隨機左右偏移一點點，看起來更活潑
                new_text = {
                    "char": event.unicode,
                    "x": WIDTH // 2 + random.randint(-50, 50),
                    "y": HEIGHT + 20  # 從視窗底部外面一點點開始
                }
                floating_texts.append(new_text)

    # --- 邏輯更新區 ---
    # 走訪所有正在飄動的文字
    # 注意：這裡用 floating_texts[:] 複製一份列表來走訪，這樣才能在迴圈裡面安全地刪除元素
    for text_info in floating_texts[:]:
        # 讓文字往上移動 (Y座標減少)
        text_info["y"] -= 2  # 數字越大飄得越快
        
        # 如果文字已經完全超出畫面上方，就把它從列表中刪除，節省記憶體
        if text_info["y"] < -50:
            floating_texts.remove(text_info)

    # --- 畫面繪製區 ---
    screen.fill((255, 255, 255))
    
    # 把列表裡面的每一個文字都畫出來
    for text_info in floating_texts:
        text_surface = font.render(f"Key: {text_info['char']}", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(text_info["x"], text_info["y"]))
        screen.blit(text_surface, text_rect)
        
    pygame.display.flip()
    clock.tick(60)
