# creates set of all words in dictionary 
def make_word_set(path_to_words_file):
	f = open(path_to_words_file)
	data = f.read().split()

	for i in range(0, len(data)):
		data[i] = data[i].lower()

	words = set(data)
	return words

# returns the ratio of valid words to number of words in message
def valid_words_in_message(message, words):
	message = message.split()

	wordsFound = 0
	for word in message:
		word = word.lower().strip()
		if word in words or word.isnumeric():
			wordsFound = wordsFound + 1
		else:
			c = word[len(word) - 1]
			#removes last char if it is a special symbol
			if not c.isalpha():
				word = word[:-1]
				if word in words or word.isnumeric():
					wordsFound = wordsFound + 1
			#else:  # debug
				#print(word) 
	return wordsFound / len(message)

## ---------------------------------------------------------------------------------------

class Letter:
    def __init__(self, letter, freq):
        self.letter = letter
        self.freq = freq

# returns list of letters sorted by their frequency in the message
def get_letter_frequency(message):
	message = message.lower()

	# get letter frequency
	freq_list = [0] * 26
	for letter in message:
		if letter.isalpha():
			index = ord(letter) - 97 # 97 = a
			freq_list[index] = freq_list[index] + 1
	# Debug
	#print(freq_list)

	# sort by frequency 
	frequencys = [0] * 26
	for i in range(0, 26):
		frequencys[i] = Letter(chr( i + ord('a')), freq_list[i])

	frequencys.sort(key=lambda x: x.freq, reverse=True)

	""" ------- Debug -------
	for i in frequencys:
		print("{c} : {count}".format(c = i.letter, count = i.freq))
	"""

	out = [0] * 26
	for i in range(0,26):
		out[i] = frequencys[i].letter

	return out

## ---------------------------------------------------------------------------------------, 

def shift_message(message, shift):
	message_arr = list(message)
	for i in range(0,len(message_arr)):
		letter = message_arr[i]
		if letter.isalpha():
			message_arr[i] = shift_letter(letter, shift)
	return "".join(message_arr)

def shift_letter(letter, shift):
	offset = (ord(letter) + shift)
	if(letter.isupper() and offset > 90 or letter.islower() and offset > 122):
		offset = (ord(letter) + shift - 26) 
	return chr(offset)










