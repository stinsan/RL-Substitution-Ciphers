from functions import *
import matplotlib.pyplot as plt
import numpy as np 
import os
import random
import time

# num_episodes % group_size == 0
def q_learning(env, alpha, gamma, num_episodes, exploration_decay, group_size):

	# because initialy the agent will know nothing
	exploration_rate = 1
	min_exploration_rate = 0.001

	q_table = np.zeros((env.num_states, env.num_actions))

	# will hold the rewards from all the episodes so we can see how they change as it progresses
	rewards_all_episodes = []

	# Q learning
	# Everything that happens within a single episode
	for episode in range(num_episodes):
		print("Episode: " + str(episode) + " " , end = "")
		state = env.reset()

		complete = False
		rewards_current_episode = 0

		# everything that happens for a single time step in each episode
		steps_needed = 0
		for step in range(26): #26 becuase we dont want the agent to select letters more than once
			steps_needed = step

			# agent will exploit
			if random.uniform(0,1) > exploration_rate:
				action = np.argmax(q_table[state,:])
			else: # agent will explore
				action = random.choice(env.actions)

			next_state, reward, complete = env.step(action)

			# Update Q table for Q(s,a)
			q_table[state, action] = q_table[state,action] + alpha * (reward + gamma * np.max(q_table[next_state, :]) - q_table[state, action])

			state = next_state
			rewards_current_episode += reward

			# message was decrypted
			if complete:
				break

		print("Trials needed: " + str(steps_needed))
		
		exploration_rate = min_exploration_rate + (1 - min_exploration_rate) * np.exp(-exploration_decay * episode)

		rewards_all_episodes.append(rewards_current_episode)

	# ----------------- Stats , figures -------------------
	rewards_per_group_size= np.split(np.array(rewards_all_episodes), num_episodes/group_size)
	out = []
	count = group_size
	print("**********Average rewards**********")
	print("Trials: Avg Reward")
	for r in rewards_per_group_size:
		print(count, ": ", str(sum(r/group_size)))
		out.append(sum(r/group_size))
		count += group_size

	plt.plot(range(1,num_episodes, group_size), out)
	plt.ylabel("Reward")
	plt.xlabel("Trials")
	plt.show()

	print("\n###### Q-table ######")
	print(q_table)

# -------------------------------------------------------------------------------------------

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

def get_files_in_dir(dir_path):
	file_names = os.listdir(dir_path)
	dir_path += "/"
	files = []
	for file_name in file_names:
		file = open(dir_path + file_name)
		message = file.read()
		files.append(message)
	return files





