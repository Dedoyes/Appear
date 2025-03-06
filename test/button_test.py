import re
from src import button
from src import utils
import pygame 
import numpy as np

class CatmullRomRender :
    def __init__ (self, screen) : 
        self.screen = screen
        self.points = []
        self.virtualPoints = []
        self.resolution = 20

    def addPoint (self, newPoint) : 
        self.points.append (np.array (newPoint))
        n = len (self.points)
        if n == 1 : 
            self.virtualPoints = [newPoint] * 2
        elif n == 2 : 
            self.virtualPoints = [2 * self.points[0] - self.points[1]] + self.points
        else : 
            self.virtualPoints = (
                [2 * self.points[0] - self.points[1]] + 
                self.points + 
                [2 * self.points[-1] - self.points[-2]]
            )

    def drawCurve (self, color = utils.WHITE, width = 2) : 
        if len (self.points) < 2 : 
            return 
        curve = []
        for i in range (0, len (self.virtualPoints) - 3) : 
            p0 = self.virtualPoints[i]
            p1 = self.virtualPoints[i + 1]
            p2 = self.virtualPoints[i + 2]
            p3 = self.virtualPoints[i + 3]
            for t in np.linspace (0, 1, self.resolution) : 
                x = Catman_Rom (p0[0], p1[0], p2[0], p3[0], t)
                y = Catman_Rom (p0[1], p1[1], p2[1], p3[1], t)
                curve.append ((x, y))
        if curve : 
            pygame.draw.lines (self.screen, color, False, curve, width)

def Catman_Rom (p0, p1, p2, p3, t) : 
    return 0.5 * (
        (-p0 + 3 * p1 - 3 * p2 + p3) * t**3 + 
        (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2 + 
        (-p0 + p2) * t + 
        2 * p1
    )

pygame.init ()
screen = pygame.display.set_mode ((1600, 900))
test_button = button.Button (300, 300, 60, 40, utils.BLUE, utils.RED, 'click')

last_pos = pygame.mouse.get_pos ()
mouse_position = []

renderer = CatmullRomRender (screen)

running = True 
while running : 
    screen.fill (utils.BLACK)
    test_button.draw (screen)
    for event in pygame.event.get () : 
        if event.type == pygame.QUIT : 
            running = False 
    if pygame.MOUSEBUTTONDOWN : 
        renderer.addPoint (pygame.mouse.get_pos ())
    renderer.drawCurve ()
    pygame.display.flip ()
#print (mouse_position)
pygame.quit ()


