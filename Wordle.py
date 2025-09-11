import pygame     #importing pygame for game development
import string     #import string for handling alphabet for key input handling
import random     #import random for random word selection 
import time       # import time for timed wordle for timings
from wordle_list import setup_database, get_random_word, valid_guess,specific_word  #importing functions from wordle_list.py for database handling
class MainMenu:                                              # for main menu interface
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width                                  #initialising variables for display setup
        self.height = height
        self.bg_color =(20, 20, 20)
        self.font = pygame.font.SysFont("arial", 36)         #font for buttons


        # Button dimensions and spacing
        self.button_width = 300
        self.button_height = 80
        self.button_spacing = 40

        # Create buttons in menu screen
        self.buttons = self.button_positioning()

    def button_positioning(self):
        total_height = (self.button_height * 3) + (self.button_spacing * 2) #total height of all buttons with spacing
        start_y = (self.height - total_height) // 2        # starting coordinates to centre buttons correctly
        start_x = (self.width - self.button_width) // 2

        return [
            Button(start_x, start_y, self.button_width, self.button_height, "Classic Mode", ),
            Button(start_x, start_y + self.button_height + self.button_spacing, self.button_width, self.button_height, "Timed Mode", ),
            Button(start_x, start_y + 2 * (self.button_height + self.button_spacing), self.button_width, self.button_height, "Hard Mode",),
        ]   #buttons for every game mode

    def run(self):        
        while True:         #loop to check for button clicks and display buttons
            self.screen.fill(self.bg_color)   #fills background with colour

            for event in pygame.event.get():  #handles input/events
                if event.type == pygame.QUIT:
                    pygame.quit()                  #exit program if x icon pressed

                for i, button in enumerate(self.buttons):   # Iterate through all buttons
                    if button.is_clicked(event):   #checks if any buttons have been clicked
                        if i == 0:    # If the first button is clicked
                            return "classic"   #string triggers classic mode
                        elif i == 1:     # If the second button is clicked and so on
                            return "timed"
                        elif i == 2:
                            return "hard"
              

            for button in self.buttons:    #draws every button
                button.draw(self.screen)

            pygame.display.flip()  #updates display

class Button:            #used to make various buttons 
    def __init__(self, x, y, width, height, text,font_size=36):
        self.rect = pygame.Rect(x, y, width, height)            #rectangle shape for button
        self.text = text
        self.font = pygame.font.SysFont("arial", font_size)            #various variables for properties of the buttons
        self.bg_color =(128, 128, 128)
        self.text_color = (255, 255, 255)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()   #mouse position
        color = self.bg_color  #hover colour
        pygame.draw.rect(screen, color, self.rect, border_radius=12)      #draws rectangle for a button
        text_surface = self.font.render(self.text, True, self.text_color)   #renders text
        text_rect = text_surface.get_rect(center=self.rect.center)    #centres text in button
        screen.blit(text_surface, text_rect)    #draws text in button

    def is_clicked(self, event):   #checks if button has been clicked
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)




class ClassicWordle:            #class 


    def __init__(self):           #passing self into constructor method
        pygame.init()              #initialising pygame



        self.screen_width, self.screen_height = 400, 400   #variables for screen width and height.

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  #initialising display window
        pygame.display.set_caption("Wordle Variant")   #window name

        
        self.input_font = pygame.font.Font(None, 50)     # Font for input text
        self.win_font = pygame.font.Font(None, 25)    # Font for buttons for later use

       
        self.white = (255, 255, 255)    #defining colours for text,background and cell colours
        self.black = (0, 0, 0)             
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.grey = (128, 128, 128)
        self.purple = (128, 0, 128)
        
        self.wordle_columns = 5   # dimesnions for wordle grid
        self.wordle_rows = 6
        self.margin = 50    # gap between edges of screen and grid

       
        self.current_row = 0      #keep track of where to add text input 
        self.current_column = 0
        self.counter = 0

        self.running = True  # used to check if game is running for input handling

        self.guess_list = [["" for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]  # 2d arrray to hold guesses

        self.cell_colours = [[self.black for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]  #default all blocks initially to black

      
        self.rep_letters = []   #list to hold letters in correct position
        self.yellow_letters = []   #list of letters somewhere in wordle
        self.temp_counter = 0

        self.hint_counter = 1   #number of hints available to user
        
        self.alphabet_keys = {getattr(pygame, f"K_{letter}"): letter.upper() for letter in string.ascii_lowercase}    #List of all alphabet keys - uppercase

        self.unrevealed_indices = [i for i in range(self.wordle_columns)]  

        self.home_button = Button(
            x=self.screen_width - 60,  # Place it 60 pixels from the right edge
            y=20,                      # 20 pixels from the top
            width=40, height=40,       # Button dimensions
            text="<=",                 # Unicode home icon
        )

        setup_database(self.wordle_columns)
        self.wordle = get_random_word().upper()  # Get a random word from the database



    def guessing_alg(self):

        while self.current_row < self.wordle_rows :  # Loop until the word is guessed or all rows are used

            bot_guess = get_random_word().upper()  # Get a random word from the database

            for i in range(len(bot_guess)):


                self.guess_list[self.current_row][i] = bot_guess[i]    #add letter to guess list


            for i in range(self.wordle_columns):

                for y in range(self.current_row):


                    if self.cell_colours[y][i] == self.green:

                        specific_word(self.guess_list[y][i],i,1) 

                    elif self.cell_colours[y][i] == self.grey:

                        specific_word(self.guess_list[y][i],i,0)

            
            self.colour()
            pygame.display.flip()  # Update the display
            pygame.time.delay(750)  # Show the colored guess for a moment
    
            self.current_row += 1                            # next row and column reset for next guess
            self.current_column = 0    





    def hint(self):
        # Only give a hint if available and there are unrevealed indices
        if self.hint_counter > 0 and len(self.unrevealed_indices) > 0 and self.current_row > 0:  # <--- Removed (self.current_row)>0 check
            # Pick a random unrevealed index that is not already green in any previous row
            valid_indices = []
            for i in self.unrevealed_indices:
                already_green = any(self.cell_colours[cycle][i] == self.green for cycle in range(self.current_row))
                if not already_green:
                    valid_indices.append(i)
            if not valid_indices:
                self.draw_win("No hints available")
                pygame.display.flip()
                pygame.time.delay(500)
                return

            i = random.choice(valid_indices)
            self.guess_list[self.current_row][i] = self.wordle[i]
            self.cell_colours[self.current_row][i] = self.purple
            self.unrevealed_indices.remove(i)
            self.hint_counter -= 1
            self.draw_grid()
            pygame.display.flip()
        else:
            self.draw_win("No hints available")
            pygame.display.flip()
            pygame.time.delay(500)


    def colour(self):

        for column in range(self.wordle_columns):        #loops for each column in the grid

            if self.guess_list[self.current_row][column] == self.wordle[column]:     #if letter is in correct position
                self.rep_letters.append(self.wordle[column])                         # adds letter to list of correct letters
            self.temp_counter += 1                               #counter incremented


        if self.temp_counter == self.wordle_columns:  #loop commences after all correct letters are added to list

            for column in range(self.wordle_columns):                 #loop for each column in the grid
                letter = self.guess_list[self.current_row][column]    

                if letter == self.wordle[column]:                              #if current letter is in correct position
                    self.cell_colours[self.current_row][column] = self.green       #cell colour is green
                elif letter in self.wordle and self.colour_conditional(column):  #if letter is in wordle but not in correct position
                    self.yellow_letters.append(letter)                              #adds letter to list of yellow letters 
                    self.cell_colours[self.current_row][column] = self.yellow          #cell colour is yellow
                else:
                    self.cell_colours[self.current_row][column] = self.grey         #if letter is not in wordle, cell colour is grey

        self.temp_counter = 0                #clear variables for next guess comparison                                   
        self.rep_letters.clear()                                              
        self.yellow_letters.clear()

    def colour_conditional(self, index):           #function to check if letter is in wordle but not in correct position

        current_l = self.guess_list[self.current_row][index]     #current letter in the grid
        instances = self.wordle.count(current_l)                 #number of instances of letter in wordle
        yellow_l = self.yellow_letters.count(current_l)          #number of instances of letter in yellow letters list
        correct_g = self.rep_letters.count(current_l)            #number of instances of letter in correct letters list
        return correct_g < instances and yellow_l < instances    #returns true if letter is in wordle but not in correct position

    def draw_grid(self):                    #draws wordle grid and additionals

        self.screen.fill(self.black)        #background

        available_width = self.screen_width - (2 * self.margin)          #varaibles for dimesnions of grid and spacing
        available_height = self.screen_height - (2 * self.margin)
        cell_width = available_width // self.wordle_columns
        cell_height = available_height // self.wordle_rows
        start_x, start_y = self.margin, self.margin

        for c in range(self.wordle_columns):     #loops through columns and rows drawing boxes to form grid
            for r in range(self.wordle_rows):
                x = start_x + (c * cell_width)
                y = start_y + (r * cell_height)
                pygame.draw.rect(self.screen, self.cell_colours[r][c], (x, y, cell_width, cell_height))
                pygame.draw.rect(self.screen, self.white, (x, y, cell_width, cell_height), 2)

                self.draw_input(self.guess_list[r][c], x + cell_width // 2, y + cell_height // 2)   #draws letters in grid

    def draw_input(self, letter, x, y):   #function to draw letters in grid

        display_text = self.input_font.render(letter, True, self.white)
        centered_text = display_text.get_rect(center=(x, y))
        self.screen.blit(display_text, centered_text)

    def draw_text(self, text, x, y):         #function to draw text generally

        display_text = self.input_font.render(text, True, self.white)       
        centered_text = display_text.get_rect(center=(x, y))
        self.screen.blit(display_text, centered_text)


    def draw_win(self, text):
        # Calculate the position for the text underneath the grid
        grid_height = self.margin + ((self.screen_height - 2 * self.margin) // self.wordle_rows) * self.wordle_rows
        x = self.screen_width // 2  # Center horizontally
        y = grid_height + 30  # Place the text 30 pixels below the grid

        # Render and draw the text
        display_text = self.win_font.render(text, True, self.purple)
        centered_text = display_text.get_rect(center=(x, y))
        self.screen.blit(display_text, centered_text)



    def input_condition(self, event):

        self.counter_condition(event)

        if event.type == pygame.QUIT:    # quit program when x icon pressed
            self.running = False

        elif event.key == pygame.K_1:     #hint button
            self.hint()                       #calls hint function to add letter to grid and colour it purple

        elif event.key == pygame.K_2:  #if enter key pressed
            self.guessing_alg()


        elif event.key in self.alphabet_keys and self.counter != self.wordle_columns:  #if key pressed is in alphabet keys and counter not at max
            self.guess_list[self.current_row][self.counter] = self.alphabet_keys[event.key]    #add letter to guess list
            self.counter += 1        #increment counter to next column
            self.draw_grid()   ##draw grid with new letter

        elif event.key == pygame.K_BACKSPACE and self.counter > 0:     #if backspace pressed and counter greater than 0 so that it does not go negative
            self.counter -= 1
            self.guess_list[self.current_row][self.counter] = ""       #deletes letter from guess list
            self.draw_grid()





    def counter_condition(self, event):

        self.current_column = self.counter

        guessed_word = "".join(self.guess_list[self.current_row]).upper()

 
        if self.counter == self.wordle_columns and valid_guess(guessed_word) and event.key == pygame.K_RETURN:          #enters guess when all letters are entered and enter key pressed
            self.colour()                                                   #checks postions of letters and colours them accordingly

            
            if guessed_word == self.wordle:

                self.cell_colours[self.current_row] = [self.green] * self.wordle_columns  # Set the entire row to green

                self.draw_grid  # Update the display to show the final guess

                self.draw_win(f"The word was {self.wordle}")

                pygame.display.flip()

                pygame.time.delay(20000)  # Wait 2 seconds

                return



            # Check if it's the last row and the word is not correct
            if self.current_row == self.wordle_rows - 1:
                self.screen.fill(self.black)
                self.draw_text("Game Over", 200, 200)
                self.draw_text(f"The word was {self.wordle}", 200, 250)
                pygame.display.flip()
                pygame.time.delay(2000)
                return
            

            self.current_row += 1                            # next row and column reset for next guess
            self.current_column = 0
            self.counter = 0

            if self.hint_counter == 0:      #make sure max 1 hint per guess
                self.hint_counter += 1   #increment hint counter to allow for hint again

    
    

    def run(self):                        #loop to check user input and display grid

        while self.running:      
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  
                    self.input_condition(event)    #function run for every key pressed

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_button.rect.collidepoint(event.pos):
                        return 


            self.draw_grid()             #continuously draws grid
            self.home_button.draw(self.screen)
            pygame.display.flip()           #update display
        pygame.quit()


class HardWordle(ClassicWordle):  # same constructor and methods as classic except colour()

    def colour(self):               #polymorphism
        for column in range(self.wordle_columns):                
            letter = self.guess_list[self.current_row][column]    

            if letter == self.wordle[column]:                              
                 self.cell_colours[self.current_row][column] = self.green         
                                                                           #removed logic for yellow letters 
            else:
               self.cell_colours[self.current_row][column] = self.grey         

 # clear everything after completion

    def hint(self):
        pass

class TimedWordle(ClassicWordle):

    def __init__(self, time_limit=120):
        super().__init__()

        self.time_limit = time_limit  # in seconds
        self.start_time = time.time()

        self.match_counter = 0  # Counter for rounds won


    def draw_timer(self):
        elapsed = time.time() - self.start_time
        remaining = max(0, int(self.time_limit - elapsed))
        timer_text = self.win_font.render(f"Time left: {remaining}s", True, self.white)
        self.screen.blit(timer_text, (10, 10))

        if remaining == 0:
            self.reveal_word_and_quit()

    def reveal_word_and_quit(self):
        self.screen.fill(self.black)
        self.draw_text("Time's up!", 200, 180)
        self.draw_text(f"The word was {self.wordle}", 200, 230)
        self.draw_text(f"Rounds won: {self.match_counter}", 200, 280)
        pygame.display.flip()
        pygame.time.delay(3000)


    def counter_condition(self, event):

        self.current_column = self.counter
        guessed_word = "".join(self.guess_list[self.current_row]).upper()

        if self.counter == self.wordle_columns and valid_guess(guessed_word) and event.key == pygame.K_RETURN:          #enters guess when all letters are entered and enter key pressed
            self.colour()                                                   #checks postions of letters and colours them accordingly

            self.guessed_word = "".join(self.guess_list[self.current_row]).upper()

            if guessed_word == self.wordle:

                self.match_counter += 1  # Increment the match counter

                self.time_limit += 25  # Add 30 seconds for the next round

                self.reset_game()  # Reset the game for a new round
                return

              
            # Check if it's the last row and the word is not correct
            if self.current_row == self.wordle_rows - 1:
                self.screen.fill(self.black)
                self.draw_text("Game Over", 200, 200)
                self.draw_text(f"The word was {self.wordle}", 200, 250)
                pygame.display.flip()
                pygame.time.delay(2000)
                self.running = False
                return
            
            self.current_row += 1                            # next row and column reset for next guess
            self.current_column = 0
            self.counter = 0

            if self.hint_counter == 0:      #make sure max 1 hint per guess
                self.hint_counter += 1   #increment hint counter to allow for hint again

            self.wordle_rows += 1

            self.guess_list.append(["" for _ in range(self.wordle_columns)])
            self.cell_colours.append([self.black for _ in range(self.wordle_columns)])


            cell_height = (self.screen_height - 2 * self.margin) // self.wordle_rows
            total_height = self.margin * 2 + (cell_height * self.wordle_rows)
            self.screen_height = total_height + self.margin
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            
    def reset_game(self):
        # Generate a new Wordle
        self.wordle = get_random_word().upper()

        # Reset the grid
        self.guess_list = [["" for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]
        self.cell_colours = [[self.black for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]

        # Reset counters
        self.current_row = 0
        self.current_column = 0
        self.counter = 0
        self.wordle_rows = 6

    

        # Reset hint counter
        self.hint_counter = 1

        # Reset screen dimensions to default
        self.screen_width, self.screen_height = 400, 400  # Default dimensions
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Reset screen size

        self.cell_height = (self.screen_height - 2 * self.margin) // self.wordle_rows


        # Redraw the grid
        self.screen.fill(self.black)
        self.draw_grid()
        pygame.display.flip()



    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.input_condition(event)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.home_button.rect.collidepoint(event.pos):
                        return 

            self.draw_grid()
            self.draw_timer()
            self.home_button.draw(self.screen)
            pygame.display.flip()
        pygame.quit()    


pygame.init()

# Define screen dimensions
WIDTH, HEIGHT = 400, 400
bg_colour = (0, 0, 0)  # Black background


# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Game")


while True:

    menu = MainMenu(screen, 400, 400)
    selected_mode = menu.run()

    if selected_mode == "classic":
        game = ClassicWordle()
        game.run()
    elif selected_mode == "hard":
        game = HardWordle()
        game.run()
    elif selected_mode == "timed":
        game = TimedWordle()
        game.run()

#