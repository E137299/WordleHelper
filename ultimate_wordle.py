import os
from collections import defaultdict
import os

WORD_LENGTH = 5


# -------------------- FREQUENCY + SCORING --------------------

def calculate_position_frequencies(words):
    """
    Returns a list of dictionaries.
    Each dictionary maps letter → frequency for that position.
    """
    frequencies = [defaultdict(int) for _ in range(WORD_LENGTH)]

    for word in words:
        for i, letter in enumerate(word):
            frequencies[i][letter] += 1

    return frequencies


def score_word(word, frequencies):
    """
    Score a word by summing positional letter frequencies.
    """
    score = 0
    for i, letter in enumerate(word):
        score += frequencies[i][letter]
    return score


def score_wordbank(words):
    frequencies = calculate_position_frequencies(words)
    scored = {}

    for word in words:
        scored[word] = score_word(word, frequencies)

    return scored


# -------------------- WORDLE FILTERS --------------------

def get_confirmed_indexes(letter, guess, feedback):
    return [
        i for i in range(len(guess))
        if guess[i] == letter and feedback[i] in ("g", "y")
    ]


def letter_at_index(letter, index, wordbank):
    return {
        word: score
        for word, score in wordbank.items()
        if word[index] == letter
    }


def letter_not_at_index(letter, index, wordbank):
    return {
        word: score
        for word, score in wordbank.items()
        if word[index] != letter
    }


def letter_in_word(letter, wordbank):
    return {
        word: score
        for word, score in wordbank.items()
        if letter in word
    }


def letter_not_in_word(letter, wordbank, confirmed_indexes):
    """
    Handles gray letters correctly, including duplicates.
    """
    filtered = {}
    allowed_count = len(confirmed_indexes)

    for word, score in wordbank.items():

        # No confirmed copies → letter must not appear
        if allowed_count == 0:
            if letter not in word:
                filtered[word] = score
            continue

        # Exact number of copies required
        if word.count(letter) != allowed_count:
            continue

        # Must appear in confirmed positions
        if all(word[i] == letter for i in confirmed_indexes):
            filtered[word] = score

    return filtered


# -------------------- MAIN PROGRAM --------------------

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


with open("wordbank.txt", "r") as f:
    words = f.read().split()

wordbank = score_wordbank(words)

# Sort from best → worst
wordbank = dict(sorted(wordbank.items(), key=lambda x: x[1], reverse=True))

for attempt in range(6):
    clear_screen()
    print("\nTop suggestions:")
    for word in list(wordbank)[:10]:
        print(word, wordbank[word])

    guess = input(f"\nGuess {attempt + 1}: ").lower()
    feedback = input("Result (G/Y/B): ").lower()

    for index, result in enumerate(feedback):
        letter = guess[index]
        confirmed = get_confirmed_indexes(letter, guess, feedback)

        if result == "g":
            wordbank = letter_at_index(letter, index, wordbank)

        elif result == "y":
            wordbank = letter_in_word(letter, wordbank)
            wordbank = letter_not_at_index(letter, index, wordbank)

        else:  # gray
            wordbank = letter_not_in_word(letter, wordbank, confirmed)
