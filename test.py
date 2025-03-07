import pygame
from src import utils
import sys

def draw_soft_circle(surface, color, pos, radius):
    # 主圆（使用传入颜色，Alpha=255）
    main_color = (color[0], color[1], color[2], 255)
    pygame.draw.circle(surface, main_color, pos, int(radius))
    
    # 边缘模糊圆（Alpha 指数衰减）
    num_layers = 3  # 减少层数
    for i in range(1, num_layers + 1):
        alpha = int(color[3] * (0.6 ** i))  # 指数衰减
        layer_radius = radius + i * 3  # 扩大半径步长
        layer_color = (color[0], color[1], color[2], alpha)
        pygame.draw.circle(surface, layer_color, pos, int(layer_radius))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def drawLine(p0, p1, screen, width):
    line_color = (0, 255, 0, 80)  # 降低基础 Alpha 值（原为 128）
    if p0.x == p1.x : 
        ymin = utils.min (p0.y, p1.y)
        ymax = utils.max (p0.y, p1.y)
        for y in range (ymin, ymax + 1, 1) :                                                                                             
            draw_soft_circle (screen, utils.ALPHABLACK, (int (p0.x), int (y)), int (width))
    elif p0.y == p1.y : 
        xmin = utils.min (p0.x, p1.x)
        xmax = utils.max (p0.x, p1.x)
        for x in range (xmin, xmax + 1, 1) : 
            draw_soft_circle (screen, utils.ALPHABLACK, (int (x), int (p0.y)), int (width))
    else : 
        startPoint = p0 
        endPoint = p1
        if p1.x < p0.x : 
            startPoint = p1 
            endPoint = p0
        x, y = startPoint.x, startPoint.y 
        for x in range (startPoint.x, endPoint.x + 1, 1) : 
            draw_soft_circle (screen, utils.ALPHABLACK, (int (x), int (y)), int (width))
            nextX = x + 1
            nextY = y 
            valStill = utils.abs (utils.F (p0, p1, Point (nextX, y)))
            valAdd = utils.abs (utils.F (p0, p1, Point (nextX, y + 1)))
            valSub = utils.abs (utils.F (p0, p1, Point (nextX, y - 1)))
            if (valStill <= valAdd) and (valStill <= valSub) :
                nextY = y
            elif (valAdd <= valStill) and (valAdd <= valSub) : 
                nextY = y + 1
            else :
                nextY = y - 1
            y = nextY


if __name__ == '__main__':
    pygame.init()
    width, height = 1920, 1080
    finalScreen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    screen = pygame.Surface((width, height), pygame.SRCALPHA)

    drawing = False
    points = []
    running = True

    while running:
        # 清空主屏幕和临时 Surface
        finalScreen.fill(utils.WHITE)  # 修复叠加问题的关键！
        screen.fill((0, 0, 0, 0))

        current_pos = pygame.mouse.get_pos()
        if drawing and len(points) >= 1:
            points.append(current_pos)
            if len(points) >= 3:
                for i in range (len (points) - 1) :
                    t = 5
                    for j in range (0, t, 1) : 
                        xj0 = points[i][0] + j * (points[i + 1][0] - points[i][0]) // t 
                        xj1 = points[i][0] + (j + 1) * (points[i + 1][0] - points[i][0]) // t
                        yj0 = points[i][1] + j * (points[i + 1][1] - points[i][1]) // t
                        yj1 = points[i][1] + (j + 1) * (points[i + 1][1] - points[i][1]) // t
                        p0 = Point (xj0, yj0)
                        p1 = Point (xj1, yj1)
                        drawLine (p0, p1, screen, width=5)
                        if p0 == p1 : 
                            break

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                points = [current_pos]
            elif event.type == pygame.MOUSEBUTTONUP:
                drawing = False

        # 渲染
        finalScreen.blit(screen, (0, 0))
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()
