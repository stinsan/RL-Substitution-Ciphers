import matplotlib.pyplot as plt
import numpy as np
import random


# num_episodes % group_size == 0
class SARSA:
    def __init__(self, env, alpha, gamma, num_episodes, exploration_decay, group_size):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.num_episodes = num_episodes
        self.exploration_decay = exploration_decay
        self.group_size = group_size

        self.exploration_rate = 1  # Initially, the agent will know nothing.

        self.q_table = np.zeros((self.env.num_states, self.env.num_actions))

    def run(self):

        min_exploration_rate = 0.001

        # will hold the rewards from all the episodes so we can see how they change as it progresses
        all_episode_rewards = []

        # SARSA
        # Everything that happens within a single episode
        for episode in range(self.num_episodes):
            state = self.env.reset()

            curr_episode_reward = 0

            # everything that happens for a single time step in each episode
            steps_needed = 0
            for step in range(26):  # 26 becuase we dont want the agent to select letters more than once
                steps_needed = step + 1

                action = self.get_action(state)

                next_state, reward, complete = self.env.step(action)

                # Update Q table for Q(s,a)
                self.q_table[state, action] = self.q_table[state, action] + self.alpha * (reward + self.gamma * self.q_table[next_state, self.get_action(next_state)] - self.q_table[state, action])

                state = next_state
                curr_episode_reward += reward

                # message was decrypted
                if complete:
                    print("Episode " + str(episode + 1) + ": " + str(steps_needed) + ' trial(s) needed.')
                    break

            self.exploration_rate = min_exploration_rate + (1 - min_exploration_rate) * np.exp(-self.exploration_decay * episode)

            all_episode_rewards.append(curr_episode_reward)

        # ----------------- Stats , figures -------------------
        rewards_per_group_size= np.split(np.array(all_episode_rewards), self.num_episodes/self.group_size)
        out = []
        count = self.group_size
        print("********** Average rewards **********")
        print("Trials: Avg Reward")
        for r in rewards_per_group_size:
            print(count, ": ", str(sum(r/self.group_size)))
            out.append(sum(r/self.group_size))
            count += self.group_size

        print("********** Calculated Optimal Policy **********")
        self.print_optimal_policy()

        plt.plot(range(0, self.num_episodes, self.group_size), out)
        plt.ylabel("Reward")
        plt.xlabel("Trials")
        plt.show()

    def get_action(self, state):
        if random.uniform(0, 1) > self.exploration_rate:  # Exploit
            action = np.argmax(self.q_table[state, :])
        else:  # Explore
            action = random.choice(self.env.actions)

        return action

    def print_optimal_policy(self):
        alphabet = [chr(ascii_char) for ascii_char in range(97, 123)]
        optimal_shifts = list()
        for i in range(len(self.q_table)):
            optimal_shifts.append(np.argmax(self.q_table[i]))

        optimal_policy = zip(alphabet, optimal_shifts)
        for action in optimal_policy:
            print(action)