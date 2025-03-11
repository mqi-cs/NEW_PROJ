
import pygame  #importing required libraries

pygame.init()           #initialising pygame

screen_width,screen_height = 600,700    #variables for screen width and height

# Define colours
White = (255, 255, 255)
Black = (0, 0, 0)
Green = (0, 255, 0)
Yellow = (255, 255, 0)
Grey = (128, 128, 128)

screen = pygame.display.set_mode((screen_width,screen_height))   #initialising display window

pygame.display.set_caption("Wordle Variant")           #window name
 
running = True                    #main loop allowing to exit app
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(Black)  # Fill the screen with white

    # Draw a black rectangle
    pygame.draw.rect(screen, White, (100, 100, 200, 100))  # (x , y cooridnates, width, height)

    pygame.display.flip()  # Update the screen

pygame.quit() # Quit the game