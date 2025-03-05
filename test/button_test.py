from src import button
from src import utils
import pygame 

pygame.init ()
screen = pygame.display.set_mode ((800, 600))
test_button = button.Button (300, 300, 60, 40, utils.BLUE, utils.RED, 'click')

running = True 
while running : 
    screen.fill (utils.BLACK)
    test_button.draw (screen)
    for event in pygame.event.get () : 
        if event.type == pygame.QUIT : 
            running = False 
    pygame.display.flip ()
pygame.quit ()


