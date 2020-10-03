from functions import *


# Special symbols 
symbols = ['.', ',',';','?', ':', '!']

# Set containing all words in dictionary
words = make_word_set("/Users/miguelbarrios/Documents/School/Machine Learning/RLProject/RL-Substitution-Ciphers/Words/words.txt")


filePath = "/Users/miguelbarrios/Documents/School/Machine Learning/RLProject/RL-Substitution-Ciphers/training/ciphertexts/shift/Clinton_1993_shift_cipher.txt"

f = open(filePath)
message = f.read()

updatedMessage = shift_message(message,14)
letter_frequency = get_letter_frequency(message)
ratio1 = valid_words_in_message(message, words)
print(letter_frequency)
print(ratio1)


# Test 
for i in range(0,26):
	updatedMessage = shift_message(message,i)
	ratio = valid_words_in_message(updatedMessage,words)
	print("Trial {trial}: {ratio}".format(trial = i,ratio = ratio))
	if(ratio > 0.8):
		break
