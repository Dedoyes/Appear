import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA)  # 启用 Alpha
clock = pygame.time.Clock()

# 创建半透明 Surface
surface = pygame.Surface((200, 200), pygame.SRCALPHA)
surface.fill((0, 0, 0, 128))  # 半透明红色

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # 白色背景
    screen.blit(surface, (300, 200))  # 绘制半透明红色方块
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
