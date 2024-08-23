def display_wordbank(wordbank):
    for word in wordbank:
        print(word)

def letter_at_index(letter, index, wordbank):
    temp = []
    for word in wordbank:
        if letter == word[index]:
            temp.append(word)
    return temp

def letter_in_word(letter, wordbank):
    temp = []
    for word in wordbank:
        if letter in word:
            temp.append(word)
    return temp

def letter_not_at_index(letter, index, wordbank):
    temp = []
    for word in wordbank:
        if letter != word[index]:
            temp.append(word)
    return temp

def letter_not_in_word(letter, index, wordbank):
    temp = []
    for word in wordbank:
        if word.count(letter) == 0:
            temp.append(word)
        elif word.count(letter) > 1: 
            if letter != word[index]:
                temp.append(word)
    return temp

words = open("wordbank.txt","r") #opens text file for reading
wordbank = words.read() #stores contents of txt file in variable
wordbank = wordbank.split() #place words into a list.


for attempt in range(7):
    guess = input("Guess "+str(attempt+1)+":   ").lower()
    score = input("How did "+guess+" score:  ").upper()

    for index, value in enumerate(score):
        if value == "G":
            wordbank = letter_at_index(guess[index],index,wordbank)
        elif value == "Y":
            wordbank = letter_in_word(guess[index],wordbank)
            wordbank = letter_not_at_index(guess[index],index, wordbank)
        else:
            wordbank = letter_not_in_word(guess[index], index, wordbank)
    for word in wordbank:
        print(word)