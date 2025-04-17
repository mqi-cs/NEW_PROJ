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
        self.win_font = pygame.font.Font(None, 50)    # Font for buttons for later use

       
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

        
        #self.wordle = self.get_random_word().upper()   #word to be guessed in uppercase
        self.wordle = "APPLE"  # For testing purposes

        self.guess_list = [["" for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]  # 2d arrray to hold guesses

        self.cell_colours = [[self.black for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]  #default all blocks initially to black

      
        self.rep_letters = []   #list to hold letters in correct position
        self.yellow_letters = []   #list of letters somewhere in wordle
        self.temp_counter = 0

        self.hint_counter = 1   #number of hints available to user
        
        self.alphabet_keys = {getattr(pygame, f"K_{letter}"): letter.upper() for letter in string.ascii_lowercase}    #List of all alphabet keys - uppercase

        self.unrevealed_indices = [i for i in range(self.wordle_columns)]       

    def get_random_word(self):     # Open the text file containing words 
       
        with open('wordle_db.txt', 'r') as file:  # Open the file for reading
            words = file.readlines()    # Read all lines in the file

        five_letter_words = [word.strip() for word in words if len(word.strip()) == 5] # Filter the words to find 5-letter words
        return random.choice(five_letter_words) if five_letter_words else "ERROR"   #Randomly choose a word and return error if none selected



    def hint(self):

        if self.hint_counter > 0 and len(self.unrevealed_indices) > 0 and (self.current_row)>0 :  # Check if hints are available and unrevealed indices exist

            i = random.choice(self.unrevealed_indices)


            for cycle in range(self.current_row):


                if self.cell_colours[cycle][i] == self.green: 
                    
                    self.unrevealed_indices.remove(i) if i in self.unrevealed_indices else None # Remove the index from the list to avoid duplicates
    

                    self.hint()

                else: 

                    self.guess_list[self.current_row][i] = self.wordle[i]
                    self.cell_colours[self.current_row][i] = self.purple  #  color to show it's a hint

                    
                    self.unrevealed_indices.remove(i)  if i in self.unrevealed_indices else None # Remove the index from the list to avoid duplicate
                    self.hint_counter -= 1

        else:

            self.draw_win("No hints available")  # Display a message if no hints are left
            pygame.display.flip()
            pygame.time.delay(500)  # Wait 




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

        elif event.key in self.alphabet_keys and self.counter != 5:  #if key pressed is in alphabet keys and counter not at max
            self.guess_list[self.current_row][self.counter] = self.alphabet_keys[event.key]    #add letter to guess list
            self.counter += 1        #increment counter to next column
            self.draw_grid()   ##draw grid with new letter

        elif event.key == pygame.K_BACKSPACE and self.counter > 0:     #if backspace pressed and counter greater than 0 so that it does not go negative
            self.counter -= 1
            self.guess_list[self.current_row][self.counter] = ""       #deletes letter from guess list
            self.draw_grid()





    def counter_condition(self, event):

        self.current_column = self.counter

        if self.counter == 5 and event.key == pygame.K_RETURN:          #enters guess when all letters are entered and enter key pressed
            self.colour()                                                   #checks postions of letters and colours them accordingly

            guessed_word = "".join(self.guess_list[self.current_row]).upper()
            
            if guessed_word == self.wordle:

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
        self.running = False


    def counter_condition(self, event):

        self.current_column = self.counter

        if self.counter == 5 and event.key == pygame.K_RETURN:          #enters guess when all letters are entered and enter key pressed
            self.colour()                                                   #checks postions of letters and colours them accordingly

            guessed_word = "".join(self.guess_list[self.current_row]).upper()

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
        self.wordle = self.get_random_word().upper()

        # Reset the grid
        self.guess_list = [["" for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]
        self.cell_colours = [[self.black for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]

        # Reset counters
        self.current_row = 0
        self.current_column = 0
        self.counter = 0

        # Reset hint counter
        self.hint_counter = 1

        # Reset screen dimensions to default
        self.screen_width, self.screen_height = 400, 400  # Default dimensions
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Reset screen size



        # Redraw the grid
        self.screen.fill(self.black)
        self.draw_grid()
        pygame.display.flip()



    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.input_condition(event)
            self.draw_grid()
            self.draw_timer()
            pygame.display.flip()
        pygame.quit()    


class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("arial", 36)
        self.clock = pygame.time.Clock()

        # Colors
        self.bg_color = (20, 20, 20)
        self.text_color = (255, 255, 255)

        # Button settings
        self.button_width = 300
        self.button_height = 80
        self.button_spacing = 40

        # Create buttons
        self.buttons = self.create_buttons()

    def create_buttons(self):
        total_height = (self.button_height * 3) + (self.button_spacing * 2)
        start_y = (self.height - total_height) // 2
        start_x = (self.width - self.button_width) // 2

        return [
            self.Button(start_x, start_y, self.button_width, self.button_height, "Classic Mode", self.font, (30, 144, 255), self.text_color, (70, 160, 255)),
            self.Button(start_x, start_y + self.button_height + self.button_spacing, self.button_width, self.button_height, "Timed Mode", self.font, (34, 139, 34), self.text_color, (60, 179, 60)),
            self.Button(start_x, start_y + 2 * (self.button_height + self.button_spacing), self.button_width, self.button_height, "Hard Mode", self.font, (178, 34, 34), self.text_color, (220, 20, 60)),
        ]

    def run(self):
        while True:
            self.screen.fill(self.bg_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                for i, button in enumerate(self.buttons):
                    if button.is_clicked(event):
                        if i == 0:
                            print("Launching Classic Mode...")
                            return "classic"
                        elif i == 1:
                            print("Launching Timed Mode...")
                            return "timed"
                        elif i == 2:
                            print("Launching Hard Mode...")
                            return "hard"

            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

    class Button:
        def __init__(self, x, y, width, height, text, font, bg_color, text_color, hover_color):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.font = font
            self.bg_color = bg_color
            self.text_color = text_color
            self.hover_color = hover_color

        def draw(self, screen):
            mouse_pos = pygame.mouse.get_pos()
            color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.bg_color
            pygame.draw.rect(screen, color, self.rect, border_radius=12)
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

        def is_clicked(self, event):
            return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)




if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wordle")

    menu = MainMenu(screen, WIDTH, HEIGHT)
    selected_mode = menu.run()

    if selected_mode == "classic":
        ClassicWordle().run()
    elif selected_mode == "timed":
        TimedWordle().run()
    elif selected_mode == "hard":
        HardWordle().run()
