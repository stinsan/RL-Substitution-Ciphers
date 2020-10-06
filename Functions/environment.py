from Functions.helpers import *
import random


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


class Environment:
	def __init__(self):
		self.plaintext_files = get_files_in_dir(os.path.join(os.getcwd(), '..',  'Training', 'plaintexts'))
		self.ciphertext_files = get_files_in_dir(os.path.join(os.getcwd(), '..',  'Training', 'ciphertexts'))
		self.key_files = get_files_in_dir(os.path.join(os.getcwd(), '..',  'Training', 'keys'))

		self.ciphertext = ""
		self.key = ""
		self.plaintext = ""

		self.num_states = 26
		self.num_actions = 26

		self.actions = range(26)

		self.letter_frequencies = []

	# returns starting state
	def reset(self):
		rand = random.randint(0, len(self.ciphertext_files) - 1)
		self.plaintext = open(self.plaintext_files[rand], 'r').read()
		self.ciphertext = open(self.ciphertext_files[rand], 'r').read()
		self.key = open(self.key_files[rand], 'r').read()

		self.letter_frequencies = get_letter_frequencies(self.ciphertext)

		start_state = ord(get_n_most_frequent_letters(self.letter_frequencies, 1)[0]) - ord('a')

		return start_state

	# returns: [next_state, reward, if done]
	def step(self, action):
		done = False
		reward = -1
		decryption = shift_message(self.ciphertext, action)
		self.ciphertext = decryption

		# Optimize
		self.letter_frequencies = get_letter_frequencies(decryption)
		next_state = ord(get_n_most_frequent_letters(self.letter_frequencies, 1)[0]) - ord('a')

		if decryption == self.plaintext:
			reward = 0
			done = True

		return [next_state, reward, done]
