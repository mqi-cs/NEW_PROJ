import sqlite3
import random

def setup_database(guess_length=5):

    conn = sqlite3.connect('wordle.db')  # Connect to the SQLite database
    cursor = conn.cursor()


    # Drop the existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS words')

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL
        )
    ''')                   # Create the words table with a 5-letter word constraint

    # Check if the table is empty
    cursor.execute('SELECT COUNT(*) FROM words')
    if cursor.fetchone()[0] == 0:
   
                     # Read words from wordle_db.txt
        with open('wordle_db.txt', 'r') as file:
            words = [line.strip() for line in file if len(line.strip()) == guess_length]  # Only include 5-letter words

            # Insert words into the database
        cursor.executemany('INSERT INTO words (word) VALUES (?)', [(word,) for word in words])
        conn.commit()

    conn.close()

def get_random_word():
  
    conn = sqlite3.connect('wordle.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    # Fetch a random word from the database
    cursor.execute('SELECT word FROM words ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def valid_guess(word):
  
    conn = sqlite3.connect('wordle.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    # Query to check if the word exists in the database
    cursor.execute('SELECT COUNT(*) FROM words WHERE word = ?', (word.lower(),))
    result = cursor.fetchone()[0]
    conn.close()

    return result > 0  # Return True if the word exists, otherwise False

def specific_word(letter,digit,bool_val):

    conn = sqlite3.connect('wordle.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    pattern = '_' * digit + letter + '%'

    if bool_val ==1 :

        cursor.execute('SELECT word FROM words WHERE word LIKE ? ORDER BY RANDOM() LIMIT 1', (pattern,))
        result = cursor.fetchone()
        conn.close()
        return result
        
    elif bool_val == 0:

        cursor.execute("DELETE FROM words WHERE word LIKE ?", (pattern,))
        conn.commit()

    