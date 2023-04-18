import os

def sorted_frequency(letter_frequency):
	values = sorted(letter_frequency.values())
	ranked=""
	for value in values:
		for letter in letter_frequency:
			if value == letter_frequency[letter]:
				ranked+=letter
	return ranked

def sort_wordbank(dictionary):
	return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=False))


def letter_in_word(letter, wordbank):
	dict = {}
	for word in wordbank:
		if letter in word:
			dict[word] = wordbank[word]
	return dict

def letter_not_in_word(letter, wordbank, index):
    dict = {}
    for word in wordbank:
        if word.count(letter) < 2:
            dict[word] = wordbank[word]
        else:
            if letter != word[index]:
                dict[word] = wordbank[word]
    return dict

def letter_at_index(letter,index,wordbank):
	dict = {}
	for word in wordbank:
		if letter == word[index]:
			dict[word] = wordbank[word]
	return dict

def letter_not_at_index(letter,index,wordbank):
	dict = {}
	for word in wordbank:
		if letter != word[index]:
			dict[word] = wordbank[word]
	return dict


def freq(wordbank,index):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    dict = {}
    for letter in alphabet:
        dict[letter]=0
        for word in wordbank:
            if letter == word[index]:
                dict[letter]+=1
    return dict

def min_value(dict):
    min=10000000000
    min_key = ""
    for letter,value in dict.items():
        if value < min:
            min = value
            min_key = letter
    return min

def simplify_dict(dict):
    for letter in dict:
        dict[letter]=int(dict[letter]/min_value(dict))
    return dict   

def get_frequencies(wordbank):
    dictionaries = []
    for index in range(5):
        dict = freq(wordbank,index)
        dict = simplify_dict(dict)
        dictionaries.append(dict)
    return dictionaries

def score_word(word,dictionaries):
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



words = open("wordbank.txt","r") #opens text file for reading
wordbank = words.read() #stores contents of txt file in variable
wordbank = wordbank.split() #place words into a list.

wordbank = score_wordbank(wordbank)
wordbank = sort_wordbank(wordbank)

for attempt in range(7):
    guess = input("Guess "+str(attempt+1)+":   ")
    score = input("How did "+guess+" score:  ").upper()

    for index, value in enumerate(score):
        if value == "G":
            wordbank = letter_at_index(guess[index],index,wordbank)
        elif value == "Y":
            wordbank = letter_in_word(guess[index],wordbank)
            wordbank = letter_not_at_index(guess[index],index, wordbank)
        else:
            wordbank = letter_not_in_word(guess[index], wordbank, index)
    for word in wordbank:
        print(word, wordbank[word])
		
				