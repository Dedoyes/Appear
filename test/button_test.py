import re
from src import button
from src import utils
import pygame 
import numpy as np

class Point :
    def __init__ (self, x, y) : 
        self.x = x 
        self.y = y

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

    def drawCurve (self, color = utils.BLACK, width = 20) : 
        if len (self.points) < 2 : 
            return 
        curve = []
        for i in range (0, len (self.virtualPoints) - 3) : 
            p0 = self.virtualPoints[i]
            p1 = self.virtualPoints[i + 1]
            p2 = self.virtualPoints[i + 2]
            p3 = self.virtualPoints[i + 3]
            for t in np.linspace (0, 1, self.resolution) : 
                x = round (Catman_Rom (p0[0], p1[0], p2[0], p3[0], t))
                y = round (Catman_Rom (p0[1], p1[1], p2[1], p3[1], t))
                if len (curve) >= 1 : 
                    drawLine (curve[-1], Point (x, y), self.screen)
                curve.append (Point (x, y)) 
                #print (curve)
                
        #if curve : 
            #pygame.draw.lines (self.screen, color, False, curve, width)
           
def Catman_Rom (p0, p1, p2, p3, t) : 
    return 0.5 * (
        (-p0 + 3 * p1 - 3 * p2 + p3) * t**3 + 
        (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2 + 
        (-p0 + p2) * t + 
        2 * p1
    )

def drawLine (p0, p1, screen) : 
    if p0.x == p1.x : 
        ymin = utils.min (p0.y, p1.y)
        ymax = utils.max (p0.y, p1.y)
        for y in range (ymin, ymax + 1, 1) : 
            screen.set_at ((p0.x, y), utils.BLACK)
    elif p0.y == p1.y : 
        xmin = utils.min (p0.x, p1.x)
        xmax = utils.max (p0.x, p1.x)
        for x in range (xmin, xmax + 1, 1) : 
            screen.set_at ((x, p0.y), utils.BLACK)
    else : 
        startPoint = p0 
        endPoint = p1
        if p1.x < p0.x : 
            startPoint = p1 
            endPoint = p0
        x, y = startPoint.x, startPoint.y 
        for x in range (startPoint.x, endPoint.x + 1, 1) : 
            screen.set_at ((x, y), utils.BLACK)
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

pygame.init ()
screen = pygame.display.set_mode ((1600, 900))
test_button = button.Button (300, 300, 60, 40, utils.BLUE, utils.RED, 'click')

last_pos = pygame.mouse.get_pos ()
mouse_position = []

renderer = CatmullRomRender (screen)

running = True 
while running : 
    screen.fill (utils.WHITE)
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


