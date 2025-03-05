import pygame 

class Button : 
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
