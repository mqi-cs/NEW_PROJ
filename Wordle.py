import pygame     #importing required libraries 
import string     #import alphabet for key input handling
import random     #import random for random word selection 
import time       # import time for timed wordle
class ClassicWordle:            #class 


    def __init__(self):           #passing self into constructor method
        pygame.init()              #initialising pygame

        
        self.screen_width, self.screen_height = 400, 400   #variables for screen width and height.

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  #initialising display window
        pygame.display.set_caption("Wordle Variant")   #window name

        
        self.input_font = pygame.font.Font(None, 50)     # Font for input text
        self.button_font = pygame.font.Font(None, 25)    # Font for buttons for later use

       
        self.white = (255, 255, 255)    #defining colours for text,background and cell colours
        self.black = (0, 0, 0)             
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.grey = (128, 128, 128)
        self.purple = (128, 0, 128)
        
        self.wordle_columns = 5    # dimesnions for wordle grid
        self.wordle_rows = 6
        self.margin = 50    # gap between edges of screen and grid

       
        self.current_row = 0      #keep track of where to add text input 
        self.current_column = 0
        self.counter = 0

        self.running = True  # used to check if game is running for input handling

        
        self.wordle = self.get_random_word().upper()   #word to be guessed in uppercase

        self.guess_list = [["" for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]  # 2d arrray to hold guesses

        self.cell_colours = [[self.black for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]  #default all blocks initially to black

      
        self.rep_letters = []   #list to hold letters in correct position
        self.yellow_letters = []   #list of letters somewhere in wordle
        self.temp_counter = 0

        self.hint_counter = 1   #number of hints available to user
        
        self.alphabet_keys = {getattr(pygame, f"K_{letter}"): letter.upper() for letter in string.ascii_lowercase}    #List of all alphabet keys - uppercase

    def get_random_word(self):     # Open the text file containing words 
       
        with open('wordle_db.txt', 'r') as file:  # Open the file for reading
            words = file.readlines()    # Read all lines in the file

        five_letter_words = [word.strip() for word in words if len(word.strip()) == 5] # Filter the words to find 5-letter words
        return random.choice(five_letter_words) if five_letter_words else "ERROR"   #Randomly choose a word and return error if none selected

    def hint(self):

        if self.hint_counter > 0:   #if hint counter is greater than 0, hint can be given

            rand_index = random.randint(0, self.wordle_columns - 1)   #randomly select an index from 0 to 4
            rand_letter = self.wordle[rand_index]                  #randomly select a letter from wordle
    

            for prev_guesses in range(self.current_row):
        
                if rand_letter in self.guess_list[prev_guesses]:   #if letter already in guess list, call hint function again
                    return self.hint()                                        #recursion to call hint function again

                else:

                    self.guess_list[self.current_row][rand_index] = rand_letter  #add letter to guess list at random index
                    self.cell_colours[self.current_row][rand_index] = self.purple  #colour cell purple to indicate hint given

        self.hint_counter -= 1

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

    def input_condition(self, event):

        self.counter_condition(event)

        if event.type == pygame.QUIT:    # quit program when x icon pressed
            self.running = False

        elif event.key in self.alphabet_keys and self.counter != 5:  #if key pressed is in alphabet keys and counter not at max
            self.guess_list[self.current_row][self.counter] = self.alphabet_keys[event.key]    #add letter to guess list
            self.counter += 1        #increment counter to next column
            self.draw_grid()   ##draw grid with new letter

        elif event.key == pygame.K_BACKSPACE and self.counter > 0:     #if backspace pressed and counter greater than 0 so that it does not go negative
            self.counter -= 1
            self.guess_list[self.current_row][self.counter] = ""       #deletes letter from guess list
            self.draw_grid()


        elif event.key == pygame.K_1:     #hint button
            self.hint()                       #calls hint function to add letter to grid and colour it purple



    def counter_condition(self, event):

        self.current_column = self.counter

        if self.counter == 5 and event.key == pygame.K_RETURN:          #enters guess when all letters are entered and enter key pressed
            self.colour()                                                   #checks postions of letters and colours them accordingly


            if self.current_row == self.wordle_rows - 1:            # game over conditions and procedures
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

    def run(self):                        #loop to check user input and display grid

        while self.running:      
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  
                    self.input_condition(event)    #function run for every key pressed
            self.draw_grid()             #continuously draws grid
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


if __name__ == "__main__":    #main loop
    game = ClassicWordle()     #instance of class 
    game.run()             #run method of class to make wordle

