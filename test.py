import pygame
import os

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PNG 光标绘图工具")

# ======================
# 1. 资源加载与初始化
# ======================
# 加载透明光标图片（尺寸建议 32x32）
cursor_img = pygame.image.load("cursor.png").convert_alpha()
cursor_rect = cursor_img.get_rect()

# 创建画布（存储所有绘制内容）
canvas = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
canvas.fill((255, 255, 255, 0))  # 初始透明背景

# 隐藏系统光标
pygame.mouse.set_visible(False)

# ======================
# 2. 绘图参数设置
# ======================
drawing = False
last_pos = None
brush_color = (0, 0, 255)  # 蓝色画笔
brush_size = 10

# ======================
# 3. 主循环
# ======================
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 鼠标按下开始绘制
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键
                drawing = True
                last_pos = pygame.mouse.get_pos()
        
        # 鼠标释放停止绘制
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                last_pos = None
        
        # 鼠标移动绘制
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = pygame.mouse.get_pos()
            if last_pos:
                # 在画布上绘制线条
                pygame.draw.line(
                    canvas, 
                    brush_color + (255,),  # 添加完全不透明Alpha
                    last_pos, 
                    current_pos, 
                    brush_size
                )
            last_pos = current_pos

    # ======================
    # 4. 画面刷新逻辑（关键）
    # ======================
    # 清空屏幕（但不影响画布）
    screen.fill((255, 255, 255))  # 白色背景
    
    # 绘制历史痕迹到屏幕
    screen.blit(canvas, (0, 0))
    
    # 绘制光标到屏幕（最后绘制保证在最上层）
    mouse_pos = pygame.mouse.get_pos()
    cursor_rect.center = mouse_pos
    screen.blit(cursor_img, cursor_rect)

    # 更新显示
    pygame.display.flip()

pygame.quit()
