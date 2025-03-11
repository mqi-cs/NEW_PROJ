
import pygame  #importing required libraries

screen_width,screen_height = 600,700    #variables for screen width and height

screen = pygame.display.set_mode((screen_width,screen_height))   #initialising display window

pygame.display.set_caption("Wordle Variant")           #window name
 

pygame.init()           #initialising pygame


running = True                    #main loop allowing to exit app
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # Update the screen

pygame.quit()