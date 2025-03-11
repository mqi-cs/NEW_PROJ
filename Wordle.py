
import pygame  #importing required libraries

pygame.init()           #initialising pygame

screen_width,screen_height = 600,700    #variables for screen width and height

# Define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

screen = pygame.display.set_mode((screen_width,screen_height))   #initialising display window

pygame.display.set_caption("Wordle Variant")           #window name
 
running = True                    #main loop allowing to exit app
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)  # Fill the screen with white

    # Draw a black rectangle
    pygame.draw.rect(screen, BLACK, (100, 100, 200, 100))  # (x , y cooridnates, width, height)

    pygame.display.flip()  # Update the screen

pygame.quit() # Quit the game