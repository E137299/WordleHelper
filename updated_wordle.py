import os

def sorted_frequency(letter_frequency):
    values = sorted(letter_frequency.values())
    ranked = ""
    for value in values:
        for letter in letter_frequency:
            if value == letter_frequency[letter]:
                ranked += letter
    return ranked


def sort_wordbank(dictionary):
    return dict(sorted(dictionary.items(), key=lambda x: x[1]))


def letter_in_word(letter, wordbank):
    filtered = {}
    for word in wordbank:
        if letter in word:
            filtered[word] = wordbank[word]
    return filtered


def letter_not_in_word(letter, wordbank, indexes):
    """
    Handles gray letters, including duplicate-letter cases.

    letter  : letter that received a gray result
    wordbank: dictionary {word: score}
    indexes : confirmed positions (green/yellow) for this letter
    """

    filtered = {}
    allowed_count = len(indexes)

    for word, score in wordbank.items():

        # Case 1: letter never confirmed → must not appear
        if allowed_count == 0:
            if letter not in word:
                filtered[word] = score
            continue

        # Case 2: letter confirmed elsewhere → exact count required
        if word.count(letter) != allowed_count:
            continue

        # Letter must appear at all confirmed positions
        valid = True
        for i in indexes:
            if word[i] != letter:
                valid = False
                break

        if valid:
            filtered[word] = score

    return filtered


def get_confirmed_indexes(letter, guess, feedback):
    indexes = []
    for i in range(len(guess)):
        if guess[i] == letter and feedback[i] in ("g", "y"):
            indexes.append(i)
    return indexes


def letter_at_index(letter, index, wordbank):
    filtered = {}
    for word in wordbank:
        if word[index] == letter:
            filtered[word] = wordbank[word]
    return filtered


def letter_not_at_index(letter, index, wordbank):
    filtered = {}
    for word in wordbank:
        if word[index] != letter:
            filtered[word] = wordbank[word]
    return filtered


def freq(wordbank, index):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    counts = {}
    for letter in alphabet:
        counts[letter] = 0
        for word in wordbank:
            if word[index] == letter:
                counts[letter] += 1
    return counts


def min_value(dictionary):
    min_val = float("inf")
    for value in dictionary.values():
        if value < min_val:
            min_val = value
    return min_val


def simplify_dict(dictionary):
    min_val = min_value(dictionary)
    for letter in dictionary:
        dictionary[letter] = int(dictionary[letter] / min_val)
    return dictionary


def get_frequencies(wordbank):
    dictionaries = []
    for index in range(5):
        d = freq(wordbank, index)
        d = simplify_dict(d)
        dictionaries.append(d)
    return dictionaries


def score_word(word, dictionaries):
    score = 0
    for i in range(5):
        score += dictionaries[i][word[i]]
    return score


def score_wordbank(wordbank):
    dictionaries = get_frequencies(wordbank)
    bank = {}
    for word in wordbank:
        bank[word] = score_word(word, dictionaries)
    return bank


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# -------------------- MAIN PROGRAM --------------------

words = open("wordbank.txt", "r")
wordbank = words.read().split()
words.close()

wordbank = score_wordbank(wordbank)
wordbank = sort_wordbank(wordbank)

for attempt in range(6):
    guess = input(f"Guess {attempt + 1}: ").lower()
    score = input(f"How did {guess} score (G/Y/B): ").lower()

    for index, value in enumerate(score):

        # Correctly compute confirmed indexes for THIS letter
        confirmed_indexes = get_confirmed_indexes(
            guess[index], guess, score
        )

        if value == "g":
            wordbank = letter_at_index(guess[index], index, wordbank)

        elif value == "y":
            wordbank = letter_in_word(guess[index], wordbank)
            wordbank = letter_not_at_index(guess[index], index, wordbank)

        else:  # gray
            wordbank = letter_not_in_word(
                guess[index], wordbank, confirmed_indexes
            )

    print("\nPossible words:")
    for word in list(wordbank)[:15]:
        print(word, wordbank[word])
