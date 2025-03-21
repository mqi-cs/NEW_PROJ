import pygame  #importing required libraries
import string  #import alphabet for key input handling


pygame.init()           #initialising pygame

screen_width,screen_height = 400,400    #variables for screen width and height.

# Define colours
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
grey = (128, 128, 128)

wordle_columns = 5   # dimesnions for wordle grid
wordle_rows = 6

margin = 50         #margin so gap between edges of screen and grid

input_font = pygame.font.Font(None, 50)  # Font for input text

current_row = 0               # where to add text input
current_column = 0  

counter = 0                                              

 #List of all alphabet keys
alphabet_keys = {getattr(pygame, f"K_{letter}"): letter for letter in string.ascii_lowercase}

guess_list = [["" for _ in range(wordle_columns)] for _ in range(wordle_rows)]            # 2d arrray to hold guesses



screen = pygame.display.set_mode((screen_width,screen_height))   #initialising display window

pygame.display.set_caption("Wordle Variant")           #window name
 

def draw_grid():    #function to draw grid
    
    # Calculate cell size based on screen size
    available_width = screen_width - (2 * margin)
    available_height = screen_height - (2 * margin)

    cell_width = available_width // wordle_columns
    cell_height = available_height // wordle_rows

    # Calculate starting position for grid
    start_x = margin
    start_y = margin

    for c in range(wordle_columns):
        for r in range(wordle_rows):
            x = start_x + (c * cell_width)
            y = start_y + (r * cell_height)
            pygame.draw.rect(screen, white, (x, y, cell_width, cell_height), 2)  # (x, y coordinates, width, height, thickness)

            # Calculate center of the cell
            text_x = x + (cell_width // 2)
            text_y = y + (cell_height // 2)

            letter = guess_list[r][c]

            draw_input(letter,text_x, text_y)
            

def draw_input(letter,x,y):  

    display_text = input_font.render(letter, True, white)  # Render the text
    centered_text = display_text.get_rect(center=(x,y))  # Center the text
    screen.blit(display_text, centered_text)  # Draw the text on screen



def input_condition(event):

    global running, counter

    counter_condition()

    if event.type == pygame.QUIT:
        running = False

    elif event.key in alphabet_keys:  # Handle alphabet key input

        guess_list[current_row][counter] = alphabet_keys[event.key]  # Use counter for column index

        counter += 1  # Move to the next column (i.e., increment the counter)

        draw_grid()  # Only redraw the grid after input is handled


    elif event.key == pygame.K_BACKSPACE:  # Handle backspace

        if current_column > 0:

            counter -= 1  # Move back to the previous column

            guess_list[current_row][counter] = ""  # Clear the current letter

            draw_grid()  # Only redraw the grid after backspace is handled




def counter_condition():

    global current_row, current_column, counter, running

    current_column = counter  # for backspace function
    

    if counter == 5:
        current_row += 1
        current_column = 0
        counter = 0

    elif current_row >= wordle_rows:
        print("Game Over")



running = True                    #main loop allowing to exit app
while running:
    for event in pygame.event.get():
        

        if event.type == pygame.KEYDOWN:

            input_condition(event)

    screen.fill(black)  # Fill the screen with black background

    draw_grid()  # Always draw the grid


    pygame.display.flip()  # Update the screen

pygame.quit() # Quit the game


# End of code