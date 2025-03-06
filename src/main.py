import pygame
import utils
import button
import sys
import numpy as np 
from scipy.interpolate import CubicSpline

def draw_soft_circle(surface, color, pos, radius):
    # 主圆（完全不透明黑色）
    pygame.draw.circle(surface, (0, 0, 0, 255), pos, int(radius))
    
    # 边缘模糊圆（多层半透明圆叠加）
    num_layers = 5  # 模糊层数
    for i in range(1, num_layers + 1):
        # 计算当前层的 Alpha 和半径扩展
        alpha = int(255 * (1 - i/num_layers))  # Alpha 递减（255 → 0）
        layer_radius = radius + i * 2  # 半径逐步扩大
        
        # 绘制半透明圆
        color = (0, 0, 0, alpha)
        pygame.draw.circle(surface, color, pos, int(layer_radius))

class Point : 
    def __init__ (self, x, y) : 
        self.x = x 
        self.y = y

def drawLine (p0, p1, screen, width) : 
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



if __name__ == '__main__' : 
    pygame.init ()
    width, height = 1920, 1080
    screen = pygame.display.set_mode ((width, height), pygame.SRCALPHA)
    screen.fill (utils.WHITE)
    clock = pygame.time.Clock ()
    pygame.display.set_caption ("Appear")

    drawing = False 
    last_pos = (0, 0)
    running = True

    last_pos = None
    points = []

    while running : 
        current_pos = pygame.mouse.get_pos ()
        if drawing and last_pos and current_pos : 
            #pygame.draw.line (screen, utils.BLACK, last_pos, current_pos, 5)
            points.append (current_pos)
            if len (points) >= 3 : 
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
        if drawing : 
            last_pos = current_pos
        for event in pygame.event.get () : 
            if event.type == pygame.QUIT :
                running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN : 
                drawing = True  
            elif event.type == pygame.MOUSEBUTTONUP : 
                drawing = False
                last_pos = None
                points = []
        pygame.display.flip ()
        clock.tick (120)
    pygame.quit ()
    sys.exit ()
                
    
