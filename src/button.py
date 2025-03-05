import pygame 

class Button : 
    def __init__ (self, x, y, width, height, R, G, B) : 
        buttonX = x
        buttonY = y
        buttonWidth = width
        buttonHeight = height
        buttonRect = pygame.Rect (buttonX, buttonY, buttonWidth, buttonHeight)
        buttonColor = (R, G, B)

