import pygame
import utils
import button
import sys
import math
import numpy as np 
from scipy.interpolate import CubicSpline

def draw_soft_circle(surface, color, pos, radius):
    # 主圆（完全不透明黑色）    
    # 边缘模糊圆（多层半透明圆叠加）
    num_layers = 2  # 模糊层数
    for i in range (1, num_layers + 1):
        # 计算当前层的 Alpha 和半径扩展
        alpha = int(100 * i / num_layers)
        layer_radius = radius + (num_layers - i) * 2  
        
        # 绘制半透明圆
        color = (0, 0, 0, alpha // 10)
        #print (alpha)
        pygame.draw.circle (surface, (255, 255, 255, 255), pos, int (layer_radius))
        pygame.draw.circle (surface, color, pos, int(layer_radius))
    #pygame.draw.circle(surface, (0, 0, 0, 255), pos, int(radius))


class Point : 
    def __init__ (self, x, y) : 
        self.x = x 
        self.y = y

def drawLine (p0, p1, screen, width) :
    #print ('drawLine')
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
    elif p0.x < p1.x:
        x, y = p0.x, p0.y 
        for x in range (p0.x, p1.x + 1, 1) : 
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
    else :
        x, y = p1.x, p1.y 
        for x in range (p0.x, p1.x - 1, -1) : 
            draw_soft_circle (screen, utils.ALPHABLACK, (int (x), int (y)), int (width))
            nextX = x - 1 
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
    #screen.fill (utils.WHITE)
    finalScreen = pygame.display.set_mode ((width, height))
    finalScreen.fill (utils.WHITE)
    clock = pygame.time.Clock ()
    screen = pygame.Surface ((width, height), pygame.SRCALPHA)
    pygame.display.set_caption ("Appear")

    drawing = False 
    last_pos = (0, 0)
    running = True

    last_pos = None
    points = []

    #draw_soft_circle (screen, (0, 0, 0, 127), (500, 500), 100)
    #finalScreen.blit (screen, (0, 0))
    #pygame.display.flip ()
       
    while running :
        #finalScreen.fill (utils.WHITE)
        screen.fill ((0, 0, 0, 0)) 
        current_pos = pygame.mouse.get_pos ()
        if drawing and last_pos and current_pos : 
            #pygame.draw.line (screen, utils.ALPHABLACK, last_pos, current_pos, 5)
            points.append (current_pos)
            if len (points) >= 2 : 
                #print (points)
                 
                for i in range (len (points) - 1) :
                    dx = points[i + 1][0] - points[i][0]
                    dy = points[i + 1][1] - points[i][1]
                    t = round (math.sqrt (dx**2 + dy**2))
                    for j in range (0, t, 1) : 
                        xj0 = round (points[i][0] + j * (points[i + 1][0] - points[i][0]) / t)
                        xj1 = round (points[i][0] + (j + 1) * (points[i + 1][0] - points[i][0]) / t)
                        yj0 = round (points[i][1] + j * (points[i + 1][1] - points[i][1]) / t)
                        yj1 = round (points[i][1] + (j + 1) * (points[i + 1][1] - points[i][1]) / t)
                        p0 = Point (xj0, yj0)
                        p1 = Point (xj1, yj1)
                        drawLine (p0, p1, screen, width=5)
                        if p0 == p1 : 
                            break
        if drawing : 
            last_pos = current_pos
        for event in pygame.event.get () : 
            if event.type == pygame.QUIT :
                running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN :
                #print ("mouse down")
                drawing = True  
            elif event.type == pygame.MOUSEBUTTONUP : 
                #print ("mouse up")
                drawing = False
                last_pos = None
                points = []
            elif event.type == pygame.MOUSEWHEEL : 
                finalScreen.fill (utils.WHITE)
                screen.fill (utils.ALPHAWHITE)
                drawing = False 
                last_pos = None
                points = []
        #pygame.draw.circle (screen, (0, 0, 0, 1), (100, 100), 10) 
        finalScreen.blit (screen, (0, 0))
        pygame.display.flip ()
        clock.tick (120)
    pygame.quit ()
    sys.exit ()
                
    
