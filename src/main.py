import pygame
from pygame.locals import *
import utils
import button
import sys
import math
import numpy as np 
from scipy.interpolate import CubicSpline
import os 

current_dir = os.path.dirname (os.path.abspath (__file__))
parent_dir = os.path.dirname (current_dir)
saves_dir = os.path.join (parent_dir, "saves")
picture_dir = os.path.join (parent_dir, "picture")
paintFilename = f"painter.png"
paintFullPath = os.path.join (picture_dir, paintFilename)

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
    
    brush_size = 100

    orgin_cursor_image = pygame.image.load (paintFullPath).convert_alpha ()
    orgin_cursor_rect = orgin_cursor_image.get_rect ()
    pygame.mouse.set_visible (False)
    new_size = (brush_size, brush_size)
    cursor_image = pygame.transform.scale (orgin_cursor_image, new_size)
    cursor_rect = cursor_image.get_rect ()

    finalScreen.fill (utils.WHITE)
    screen.fill (utils.ALPHAWHITE)
    drawing = False 
    last_pos = None
    points = []

    while running :
        #finalScreen.fill (utils.WHITE)
        #screen.fill ((0, 0, 0, 0))
        canavas = pygame.Surface ((width, height), pygame.SRCALPHA)
        canavas.fill ((0, 0, 0, 0))
        pygame.draw.circle (finalScreen, (255, 0, 0), (100, 100), 10) 
        current_pos = pygame.mouse.get_pos ()
        cursor_rect.center = (current_pos[0], current_pos[1])
        canavas.blit (cursor_image, cursor_rect)
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
                        utils.drawLine (p0, p1, screen, 5)
                        if p0 == p1 : 
                            break
            elif len (points) == 1 : 
                p0 = utils.Point (round (points[0][0]), round (points[0][1]))
                utils.drawLine (p0, p0, screen, 5) 
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
            elif event.type == KEYDOWN : 
                if event.key == K_s and (event.mod & KMOD_CTRL) : 
                    filename = f"saves.png"
                    fullPath = os.path.join (saves_dir, filename)
                    pygame.image.save (screen, fullPath)
                    print ("success save as screenshot.png")
        #pygame.draw.circle (screen, (0, 0, 0, 1), (100, 100), 10) 
        finalScreen.blit (screen, (0, 0))
        finalScreen.blit (canavas, (0, 0))
        pygame.display.flip ()
        clock.tick (120)
    pygame.quit ()
    sys.exit ()
                
    
