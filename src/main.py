import pygame
import utils
import button
import sys
import math
import numpy as np 
from scipy.interpolate import CubicSpline

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
                        p0 = utils.Point (xj0, yj0)
                        p1 = utils.Point (xj1, yj1)
                        utils.drawLine (p0, p1, screen, width=5)
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
                
    
