from Functions.environment import *
from Functions.q_learning import q_learning
from Functions.sarsa import SARSA

if __name__ == '__main__':
	env = Environment()
	alpha = 0.1
	gamma = 0.99
	num_episodes = 500
	exploration_decay_rate = 0.005
	group_size = 25
	# q_learning(env, alpha, gamma, num_episodes, exploration_decay_rate, group_size)

	sarsa = SARSA(env, alpha, gamma, num_episodes, exploration_decay_rate, group_size)
	sarsa.run()
