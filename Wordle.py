import pygame
import string
import random

class WordleGame:
    def __init__(self):
        pygame.init()

        # Display
        self.screen_width, self.screen_height = 400, 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Wordle Variant")

        # Fonts
        self.input_font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 25)

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.yellow = (255, 255, 0)
        self.grey = (128, 128, 128)

        # Game settings
        self.wordle_columns = 5
        self.wordle_rows = 6
        self.margin = 50

        # Game state
        self.current_row = 0
        self.current_column = 0
        self.counter = 0
        self.running = True

        # Word and guesses
        self.wordle = self.get_random_word().upper()
        self.guess_list = [["" for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]
        self.cell_colours = [[self.black for _ in range(self.wordle_columns)] for _ in range(self.wordle_rows)]

        # Input tracking
        self.rep_letters = []
        self.yellow_letters = []
        self.temp_counter = 0
        self.alphabet_keys = {getattr(pygame, f"K_{letter}"): letter.upper() for letter in string.ascii_lowercase}

    def get_random_word(self):
        with open('wordle_db.txt', 'r') as file:
            words = file.readlines()
        five_letter_words = [word.strip() for word in words if len(word.strip()) == 5]
        return random.choice(five_letter_words) if five_letter_words else "ERROR"

    def colour(self):
        for column in range(self.wordle_columns):
            if self.guess_list[self.current_row][column] == self.wordle[column]:
                self.rep_letters.append(self.wordle[column])
            self.temp_counter += 1

        if self.temp_counter == self.wordle_columns:
            for column in range(self.wordle_columns):
                letter = self.guess_list[self.current_row][column]
                if letter == self.wordle[column]:
                    self.cell_colours[self.current_row][column] = self.green
                elif letter in self.wordle and self.colour_conditional(column):
                    self.yellow_letters.append(letter)
                    self.cell_colours[self.current_row][column] = self.yellow
                else:
                    self.cell_colours[self.current_row][column] = self.grey

        self.temp_counter = 0
        self.rep_letters.clear()
        self.yellow_letters.clear()

    def colour_conditional(self, index):
        current_l = self.guess_list[self.current_row][index]
        instances = self.wordle.count(current_l)
        yellow_l = self.yellow_letters.count(current_l)
        correct_g = self.rep_letters.count(current_l)
        return correct_g < instances and yellow_l < instances

    def draw_grid(self):
        self.screen.fill(self.black)
        available_width = self.screen_width - (2 * self.margin)
        available_height = self.screen_height - (2 * self.margin)
        cell_width = available_width // self.wordle_columns
        cell_height = available_height // self.wordle_rows
        start_x, start_y = self.margin, self.margin

        for c in range(self.wordle_columns):
            for r in range(self.wordle_rows):
                x = start_x + (c * cell_width)
                y = start_y + (r * cell_height)
                pygame.draw.rect(self.screen, self.cell_colours[r][c], (x, y, cell_width, cell_height))
                pygame.draw.rect(self.screen, self.white, (x, y, cell_width, cell_height), 2)
                self.draw_input(self.guess_list[r][c], x + cell_width // 2, y + cell_height // 2)

    def draw_input(self, letter, x, y):
        display_text = self.input_font.render(letter, True, self.white)
        centered_text = display_text.get_rect(center=(x, y))
        self.screen.blit(display_text, centered_text)

    def draw_text(self, text, x, y):
        display_text = self.input_font.render(text, True, self.white)
        centered_text = display_text.get_rect(center=(x, y))
        self.screen.blit(display_text, centered_text)

    def input_condition(self, event):
        self.counter_condition(event)
        if event.type == pygame.QUIT:
            self.running = False

        elif event.key in self.alphabet_keys and self.counter != 5:
            self.guess_list[self.current_row][self.counter] = self.alphabet_keys[event.key]
            self.counter += 1
            self.draw_grid()

        elif event.key == pygame.K_BACKSPACE and self.counter > 0:
            self.counter -= 1
            self.guess_list[self.current_row][self.counter] = ""
            self.draw_grid()

    def counter_condition(self, event):
        self.current_column = self.counter
        if self.counter == 5 and event.key == pygame.K_RETURN:
            self.colour()
            if self.current_row == self.wordle_rows - 1:
                self.screen.fill(self.black)
                self.draw_text("Game Over", 200, 200)
                self.draw_text(f"The word was {self.wordle}", 200, 250)
                pygame.display.flip()
                pygame.time.delay(2000)
                self.running = False
                return
            self.current_row += 1
            self.current_column = 0
            self.counter = 0

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.input_condition(event)
            self.draw_grid()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    game = WordleGame()
    game.run()
