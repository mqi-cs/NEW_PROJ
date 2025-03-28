import pygame  #importing required libraries
import string  #import alphabet for key input handling
import random  #import random for random word selection



class classic_wordle:
    def __init__(self):
        pass

    def run_game(self):  #function to run the game

        pygame.init()           #initialising pygame

        self.screen_width,self.screen_height = 400,400    #variables for screen width and height.

        # Define colours
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.grey = (128, 128, 128)

        self.wordle_columns = 5   # dimesnions for wordle grid
        self.wordle_rows = 6

        self.margin = 50         #margin so gap between edges of screen and grid

        self.input_font = pygame.font.Font(None, 50)  # Font for input text

        self.button_font = pygame.font.Font(None, 25)  # Font for buttons


        self.current_row = 0               # where to add text input
        self.current_column = 0  

        self.counter = 0                                              

        #List of all alphabet keys - uppercase
        self.alphabet_keys = {getattr(pygame, f"K_{letter}"): letter.upper() for letter in string.ascii_lowercase}

        self.guess_list = [["" for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]            # 2d arrray to hold guesses


        def rand_wordle(self):
            # Open the text file containing words
            with open('wordle_db.txt', 'r') as file:  # Open the file for reading
                words = file.readlines()  # Read all lines in the file

            # Filter the words to find 5-letter words
            five_letter_words = [word.strip() for word in words if len(word.strip()) == 5]

            # Select a random word from the 5-letter words
            if five_letter_words:
                return random.choice(five_letter_words)  # Randomly choose a word
            else:
                return None  # Return None if no 5-letter words are found


        self.wordle = self.rand_wordle()  #word to be guessed
        self.wordle = self.wordle.upper()  # Convert to uppercase

        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))   #initialising display window

        self.pygame.display.set_caption("Wordle Variant")           #window name
        
        self.cell_colours = [[self.black for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]  # Default all to black



        self.rep_letters = []
        self.yellow_letters = []
        self.temp_counter = 0

        def colour(self):
            global temp_counter

            for column in range(self.wordle_columns):

                if self.guess_list[self.current_row][self.column] == self.wordle[self.column]:

                    self.rep_letters.append(self.wordle[column])

                temp_counter += 1


                if temp_counter == self.wordle_columns:

                    for column in range(self.wordle_columns):

                        if  self.guess_list[current_row][column] == self.wordle[column]:

                            self.cell_colours[current_row][column] = self.green

                        elif self.guess_list[current_row][column] in self.wordle and colour_conditional(column):

                            self.yellow_letters.append(self.guess_list[current_row][column])
                            self.cell_colours[current_row][column] = self.yellow  # Wrong position

                        else:  

                            self.cell_colours[current_row][column] = self.grey  # Not in word

            self.temp_counter = 0
            self.rep_letters.clear()
            self.yellow_letters.clear()

        def colour_conditional(index):

            current_l = self.guess_list[current_row][index]

            instances = self.wordle.count(current_l)

            yellow_l = self.yellow_letters.count(current_l)

            correct_g = self.rep_letters.count(current_l)


            if correct_g < instances and yellow_l < instances:

                return True




        def draw_grid(self):    #function to draw grid


            self.screen.fill(self.black)  # Fill the screen with black background


            # Calculate cell size based on screen size
            available_width = self.screen_width - (2 * self.margin)
            available_height = self.screen_height - (2 * self.margin)

            cell_width = available_width // self.wordle_columns
            cell_height = available_height // self.wordle_rows

            # Calculate starting position for grid
            start_x = self.margin
            start_y = self.margin

            for c in range(self.wordle_columns):
                for r in range(self.wordle_rows):
                    x = start_x + (c * cell_width)
                    y = start_y + (r * cell_height)

                    pygame.draw.rect(self.screen, self.cell_colours[r][c], (x, y, cell_width, cell_height))  #cell with no thicknesses, used to fill each cell

                    pygame.draw.rect(self.screen, self.white, (x, y, cell_width, cell_height), 2)  # (x, y coordinates, width, height, thickness)

                    # Calculate center of the cell
                    text_x = x + (cell_width // 2)
                    text_y = y + (cell_height // 2)

                    self.letter = self.guess_list[r][c]

                    draw_input(self.letter,text_x, text_y)

        def draw_input(self,letter,x,y):  

            display_text = self.input_font.render(letter, True, self.white)  # Render the text
            centered_text = display_text.get_rect(center=(x,y))  # Center the text
            self.screen.blit(display_text, centered_text)  # Draw the text on screen



        def input_condition(self,event):

            global running, counter

            counter_condition(event)

            if event.type == pygame.QUIT:
                running = False

            elif event.key in self.alphabet_keys and self.counter != 5 :  # Handle alphabet key input  with restrictions

                self.guess_list[current_row][counter] = self.alphabet_keys[event.key]  # Use counter for column index

                self.counter += 1  # Move to the next column (i.e., increment the counter)

                self.draw_grid()  # Only redraw the grid after input is handled


            elif event.key == pygame.K_BACKSPACE:  # Handle backspace

                if self.current_column > 0:

                    self.counter -= 1  # Move back to the previous column

                    self.guess_list[current_row][counter] = ""  # Clear the current letter

                    draw_grid()  # Only redraw the grid after backspace is handled    

        def counter_condition(self,event):

            global current_row, current_column, counter, running

            current_column = counter  # for backspace function
            

            if counter == 5 and event.key == pygame.K_RETURN :  # Only switches rows when enter is pressed
                
                colour()  # colours letters after checking position after enter is pressed



                if current_row == self.wordle_rows - 1:  # If on the last row
                    self.screen.fill(self.black)
                    draw_text("Game Over", 200, 200)
                    draw_text(f"The word was {self.wordle}", 200, 250)
                    pygame.display.flip()
                    pygame.time.delay(2000)  # Pause for 2 seconds
                    return  # Stop further execution
                
                self.current_row += 1
                self.current_column = 0
                counter = 0


        def draw_text(self,text,x,y):  

            display_text = self.input_font.render(text, True, self.white)  # Render the text
            centered_text = display_text.get_rect(center=(x,y))  # Center the text
            self.screen.blit(display_text, centered_text)  # Draw the text on screen


        def hint_wordle(self):

            rand_number = random.randint(0,4)
            


        self.running = True                    #main loop allowing to exit app
        while self.running:
            for event in pygame.event.get():
                

                if event.type == pygame.KEYDOWN:

                    self.input_condition(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass


            self.running = True
            self.counter = 0
            self.current_row = 0
            self.current_column = 0
            self.draw_grid()  # Always draw the grid


            pygame.display.flip()  # Update the screen

        pygame.quit() # Quit the game


        # End of code

game = classic_wordle()  # Create an instance of the game class