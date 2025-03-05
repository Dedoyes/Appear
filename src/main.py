import pygame
import utils

if __name__ == '__main__' : 
    pygame.init ()
    width, height = 800, 600
    screen = pygame.display.set_mode ((width, height))
    pygame.display.set_caption ("Appear")

    bx, by, bw, bh = 350, 250, 100, 50
    button_rect = pygame.Rect (bx, by, bw, bh)
    button_color = (255, 255, 255)
    text_color = (0, 0, 0)

    button_font = pygame.font.Font ('./font/0xProtoNerdFont-Regular.ttf', 20)
    button_text = button_font.render ("Button", True, text_color)

    running = True 
    while running : 
        screen.fill ((0, 0, 0))
        pygame.draw.rect (screen, button_color, button_rect)
        screen.blit (button_text, (button_rect.centerx - button_text.get_width() / 2, button_rect.centery - button_text.get_height() / 2))
        for event in pygame.event.get () : 
            if event.type == pygame.QUIT :  
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN : 
                if button_rect.collidepoint (event.pos) : 
                    print ('Click')
        pygame.display.flip ()
    pygame.quit ()
