
import pygame  #importing required libraries

pygame.init()           #initialising pygame

screen_width,screen_height = 700,900    #variables for screen width and height

# Define colours
White = (255, 255, 255)
Black = (0, 0, 0)
Green = (0, 255, 0)
Yellow = (255, 255, 0)
Grey = (128, 128, 128)

Wordle_Columns = 5   # dimesnions for wordle grid
Wordle_rows = 6

margin = 100         #margin so gap between edges of screen and grid

screen = pygame.display.set_mode((screen_width,screen_height))   #initialising display window

pygame.display.set_caption("Wordle Variant")           #window name
 
def draw_grid():    #function to draw grid
    for c in range(Wordle_Columns):
        for r in range(Wordle_rows):
            pygame.draw.rect(screen, White, ((c*100)+margin, (r*100)+margin, 100, 100), 2)  # (x , y cooridnates, width, height, thickness)



running = True                    #main loop allowing to exit app
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(Black)  # Fill the screen with black background

    draw_grid()  # Draw the grid

    pygame.display.flip()  # Update the screen

pygame.quit() # Quit the game