import pygame 
import math
import utils

class rectButton : 
    def __init__ (self, x, y, width, height, buttonColor, textColor, text) : 
        self.buttonX = x
        self.buttonY = y
        self.buttonWidth = width
        self.buttonHeight = height
        self.buttonRect = pygame.Rect (self.buttonX, self.buttonY, self.buttonWidth, self.buttonHeight)
        self.buttonColor = buttonColor
        self.textColor = textColor
        self.buttonFont = pygame.font.Font ('./font/0xProtoNerdFont-Regular.ttf', 20)
        self.buttonText = self.buttonFont.render (text, True, self.textColor)

    def draw (self, screen) : 
        pygame.draw.rect (screen, self.buttonColor, self.buttonRect)                                                                                                                                                         
        screen.blit (self.buttonText, (self.buttonRect.centerx - self.buttonText.get_width () / 2, self.buttonRect.centery - self.buttonText.get_height () / 2))

class CircleButton : 
    def __init__ (self, pos, color, rad, angle) : 
        self.pos = pos
        self.color = color 
        self.rad = round (rad)
        self.angle = angle
    
    def draw (self, screen) : 
        pygame.draw.circle (screen, (0, 0, 0), self.pos, self.rad + 4)
        pygame.draw.circle (screen, self.color, self.pos , self.rad)
        x1 = 0.618 * self.rad * math.cos (self.angle)
        y1 = 0.618 * self.rad * math.sin (self.angle)
        p1 = utils.Point (round (x1 + self.pos[0]), round (y1 + self.pos[1]))
        x2 = 0.618 * self.rad * math.cos (self.angle + 0.5 * utils.Pi)
        y2 = 0.618 * self.rad * math.sin (self.angle + 0.5 * utils.Pi)
        p2 = utils.Point (round (x2 + self.pos[0]), round (y2 + self.pos[1]))
        x3 = 0.618 * self.rad * math.cos (self.angle - 0.5 * utils.Pi)
        y3 = 0.618 * self.rad * math.sin (self.angle - 0.5 * utils.Pi)
        p3 = utils.Point (round (x3 + self.pos[0]), round (y3 + self.pos[1]))
        x4 = -x1
        y4 = -y1 
        p4 = utils.Point (round (x4 + self.pos[0]), round (y4 + self.pos[1]))
        utils.drawLine (p1, p2, screen, 1, utils.ALPHABLACK)
        utils.drawLine (p1, p3, screen, 1, utils.ALPHABLACK)
        utils.drawLine (p1, p4, screen, 1, utils.ALPHABLACK)

    def isTouch (self, pos) : 
        dx = pos[0] - self.pos[0]
        dy = pos[1] - self.pos[1]
        return dx**2 + dy**2 <= self.rad**2

class ColorPool : 
    def __init__ (self, color, pos, rad) : 
        self.color = color
        self.pos = pos
        self.rad = rad
    
    def draw (self, screen) : 
        pygame.draw.circle (screen, (0, 0, 0), self.pos, self.rad + 2)
        pygame.draw.circle (screen, self.color, self.pos, self.rad)

    def isTouch (self, pos) : 
        dx = pos[0] - self.pos[0]
        dy = pos[1] - self.pos[1]
        return dx**2 + dy**2 <= self.rad**2

