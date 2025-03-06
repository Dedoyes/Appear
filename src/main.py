import pygame
import utils
import button
import sys
import numpy as np 
from scipy.interpolate import CubicSpline

if __name__ == '__main__' : 
    pygame.init ()
    width, height = 1920, 1080
    screen = pygame.display.set_mode ((width, height))
    screen.fill (utils.WHITE)
    pygame.display.set_caption ("Appear")

    drawing = False 
    last_pos = (0, 0)
    running = True

    while running : 
        for event in pygame.event.get () : 
            if event.type == pygame.QUIT :
                running = False 
            if event.type == pygame.MOUSEBUTTONDOWN : 
                drawing = True 
                last_pos = event.pos 
            if event.type == pygame.MOUSEBUTTONUP : 
                drawing = False 
            if event.type == pygame.MOUSEMOTION : 
                if drawing : 
                    current_pos = event.pos 
                    pygame.draw.aaline (screen, utils.BLACK, last_pos, current_pos)
                    last_pos = current_pos
        pygame.display.flip ()

    pygame.quit ()
    sys.exit ()
                
    
