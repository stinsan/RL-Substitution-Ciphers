from functions import *
import numpy as np 
import random
import time

class State:
	def __init__(self, letter):
		self.letter = letter
		self.previous_actions = set()

	def add(self, action):
		self.previous_actions.add(action)

	def contains(self, action):
		if action in self.previous_actions:
			return True
		return False

class Enviornment:
	def __init__(self):
		self.files = get_files_in_dir("/Users/miguelbarrios/Documents/School/Machine Learning/RLProject/RL-Substitution-Ciphers/training/ciphertexts/shift")
		self.words = make_word_set("/Users/miguelbarrios/Documents/School/Machine Learning/RLProject/RL-Substitution-Ciphers/Words/words.txt")
		self.message = ""
		self.num_states = 26
		self.num_actions = 26
		self.states = range(26)
		self.actions = range(26)
		self.states = [None] * 26
		self.letter_freq = []

	# returns starting state
	def reset(self):
		self.message = random.choice(self.files)
		letter = 97
		for i in range(26):
			self.states[i] = State(chr(letter) ) 
			letter += 1
		self.letter_freq = get_letter_frequency(self.message)
		state_index = ord(self.letter_freq[0]) - ord('a')
		return state_index

	#returns: [next_state, reward, if done]
	def step(self, action):
		done = False
		reward = -1
		next_state = 0
		updated_message = shift_message(self.message, action)
		# Optimize
		next_state = ord('a') - ord(get_letter_frequency(self.message)[0])
		ratio = valid_words_in_message(updated_message, self.words)
		if(ratio > 0.8):
			reward = 26
			done = True
		return [next_state, reward, done]



# Special symbols 
symbols = ['.', ',',';','?', ':', '!']


env = Enviornment()
alpha = 0.1
gamma = 0.99
num_episodes = 250
exploration_decay_rate = 0.01
group_size = 25
q_learning(env, alpha, gamma, num_episodes, exploration_decay_rate, group_size)

