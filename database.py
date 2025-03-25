import random

def random_wordle():
    # Open the text file containing words
    with open('words.txt', 'r') as file:  # Open the file for reading
        words = file.readlines()  # Read all lines in the file

    # Filter the words to find 5-letter words
    five_letter_words = [word.strip() for word in words if len(word.strip()) == 5]

    # Select a random word from the 5-letter words
    if five_letter_words:
        return random.choice(five_letter_words)  # Randomly choose a word
    else:
        return None  # Return None if no 5-letter words are found