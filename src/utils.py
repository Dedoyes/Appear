import pygame
import math

class Point : 
    def __init__ (self, x, y) : 
        self.x = x 
        self.y = y

BLACK = (0, 0, 0)
ALPHABLACK = (0, 0, 0, 255)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
ALPHAWHITE = (255, 255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

Pi = math.acos (-1.0)
beauty = 0.5 * (math.sqrt (5) - 1)

def max (a, b) : 
    if a > b :
        return a
    else : 
        return b 

def min (a, b) :
    if a < b : 
        return a
    else :
        return b

def F (p0, p1, p) : 
    k = (p1.y - p0.y) / (p1.x - p0.x) 
    return p.y - k * (p.x - p0.x) - p0.y  

def abs (x) :
    if x < 0 : 
        return -x
    else : 
        return x

def draw_soft_circle(surface, color, pos, radius):
    # 主圆（完全不透明黑色）    
    # 边缘模糊圆（多层半透明圆叠加）
    num_layers = 2  # 模糊层数
    firstColor = (color[0], color[1], color[2], 255)
    pygame.draw.circle (surface, firstColor, pos, round (radius) + 1)
    #screen.blit (surface, (0, 0))
    #surface.fill ((255, 255, 255))
    for i in range (1, num_layers):
        # 计算当前层的 Alpha 和半径扩展
        alpha = 40 * i 
        layer_radius = radius + (num_layers - i)
        # 绘制半透明圆
        tempColor = (color[0], color[1], color[2], alpha) 
        #print (alpha)
        #pygame.draw.circle (surface, (255, 255, 255, 255), pos, round (layer_radius))
        pygame.draw.circle (surface, tempColor, pos, round (layer_radius))
    #pygame.draw.circle(surface, (0, 0, 0, 255), pos, round (radius))

def drawLine (p0, p1, screen, width, color) :
    #print ('drawLine')
    if p0.x == p1.x : 
        ymin = min (p0.y, p1.y)
        ymax = max (p0.y, p1.y)
        for y in range (ymin, ymax + 1, 1) :                                                                                             
            draw_soft_circle (screen, color, (round (p0.x), round (y)), round (width))
    elif p0.y == p1.y : 
        xmin = min (p0.x, p1.x)
        xmax = max (p0.x, p1.x)
        for x in range (xmin, xmax + 1, 1) : 
            draw_soft_circle (screen, color, (round (x), round (p0.y)), round (width))
    elif p0.x < p1.x:
        x, y = p0.x, p0.y 
        for x in range (p0.x, p1.x + 1, 1) : 
            draw_soft_circle (screen, color, (round (x), round (y)), round (width))
            nextX = x + 1
            nextY = y 
            valStill = abs (F (p0, p1, Point (nextX, y)))
            valAdd = abs (F (p0, p1, Point (nextX, y + 1)))
            valSub = abs (F (p0, p1, Point (nextX, y - 1)))
            if (valStill <= valAdd) and (valStill <= valSub) :
                nextY = y
            elif (valAdd <= valStill) and (valAdd <= valSub) : 
                nextY = y + 1
            else :
                nextY = y - 1
            y = nextY
    else :
        x, y = p0.x, p0.y 
        for x in range (p0.x, p1.x - 1, -1) : 
            draw_soft_circle (screen, color, (round (x), round (y)), round (width))
            nextX = x - 1 
            nextY = y 
            valStill = abs (F (p0, p1, Point (nextX, y)))
            valAdd = abs (F (p0, p1, Point (nextX, y + 1)))
            valSub = abs (F (p0, p1, Point (nextX, y - 1)))
            if (valStill <= valAdd) and (valStill <= valSub) :
                nextY = y
            elif (valAdd <= valStill) and (valAdd <= valSub) : 
                nextY = y + 1
            else :
                nextY = y - 1
            y = nextY


