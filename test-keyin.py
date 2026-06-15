import pygame
import sys

# 1. 初始化 pygame
pygame.init()

# 2. 設定視窗與字型
screen = pygame.display.set_mode((400, 300))  # 寬 400，高 300 的視窗
pygame.display.set_caption("鍵盤輸入測試 (停留三秒)")      # 視窗標題
font = pygame.font.SysFont("arial", 40)       # 設定顯示字型與大小

clock = pygame.time.Clock()

# 用來記錄要顯示的文字，以及文字出現的時間
current_char = ""
show_time = 0

# 3. 遊戲主迴圈
while True:
    # 取得遊戲啟動到現在的總時間（單位：毫秒）
    current_time = pygame.time.get_ticks()
    
    # --- 事件偵測區 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # 偵測是否有鍵盤按下的事件
        if event.type == pygame.KEYDOWN:
            # event.unicode 可以把按鍵轉換成文字（例如 'a', '1' 等）
            if event.unicode: 
                current_char = event.unicode
                show_time = current_time  # 記錄打字當下的時間

    # --- 邏輯更新區 ---
    # 如果有字，而且現在時間減去打字時間大於 3000 毫秒（3 秒），就清空文字
    if current_char != "" and (current_time - show_time > 3000):
        current_char = ""

    # --- 畫面繪製區 ---
    screen.fill((255, 255, 255))  # 把背景塗成白色 (RGB)
    
    # 如果有字需要顯示
    if current_char != "":
        # 把文字轉成圖片 (文字內容, 是否平滑邊緣, 黑色)
        text_surface = font.render(f"Key: {current_char}", True, (0, 0, 0))
        # 抓取這張文字圖片的矩形，並對齊在視窗正中央
        text_rect = text_surface.get_rect(center=(200, 150))
        # 把文字畫到螢幕上
        screen.blit(text_surface, text_rect)
        
    pygame.display.flip()  # 更新畫面顯示
    clock.tick(60)         # 限制每秒最多 60 幀
