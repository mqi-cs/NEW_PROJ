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

wordle = "hello"  #word to be guessed

screen = pygame.display.set_mode((screen_width,screen_height))   #initialising display window

pygame.display.set_caption("Wordle Variant")           #window name
 
cell_colours = [[black for _ in range(wordle_columns)] for _ in range(wordle_rows)]  # Default all to black



rep_letters = []
yellow_letters = []
temp_counter = 0

def colour():
    global temp_counter

    for column in range(wordle_columns):

        if guess_list[current_row][column] == wordle[column]:

            rep_letters.append(wordle[column])

        temp_counter += 1


        if temp_counter == wordle_columns:

            for column in range(wordle_columns):

                if  guess_list[current_row][column] == wordle[column]:

                    cell_colours[current_row][column] = green

                elif guess_list[current_row][column] in wordle and colour_conditional(column):

                    yellow_letters.append(guess_list[current_row][column])
                    cell_colours[current_row][column] = yellow  # Wrong position

                else:  

                    cell_colours[current_row][column] = grey  # Not in word

    temp_counter = 0
    rep_letters.clear()

def colour_conditional(index):

    current_l = guess_list[current_row][index]

    instances = wordle.count(current_l)

    yellow_l = yellow_letters.count(current_l)

    correct_g = rep_letters.count(current_l)


    if correct_g < instances and yellow_l < instances:

        return True




def draw_grid():    #function to draw grid


    screen.fill(black)  # Fill the screen with black background


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

            pygame.draw.rect(screen, cell_colours[r][c], (x, y, cell_width, cell_height))  #cell with no thicknesses, used to fill each cell

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

    counter_condition(event)

    if event.type == pygame.QUIT:
        running = False

    elif event.key in alphabet_keys and counter != 5 :  # Handle alphabet key input  with restrictions

        guess_list[current_row][counter] = alphabet_keys[event.key]  # Use counter for column index

        counter += 1  # Move to the next column (i.e., increment the counter)

        draw_grid()  # Only redraw the grid after input is handled


    elif event.key == pygame.K_BACKSPACE:  # Handle backspace

        if current_column > 0:

            counter -= 1  # Move back to the previous column

            guess_list[current_row][counter] = ""  # Clear the current letter

            draw_grid()  # Only redraw the grid after backspace is handled    

def counter_condition(event):

    global current_row, current_column, counter, running

    current_column = counter  # for backspace function
    

    if counter == 5 and event.key == pygame.K_RETURN :  # Only switches rows when enter is pressed
        
        colour()  # colours letters after checking position after enter is pressed

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

    draw_grid()  # Always draw the grid


    pygame.display.flip()  # Update the screen

pygame.quit() # Quit the game


# End of code
