import matplotlib.pyplot as plt
import numpy as np
import random


# num_episodes % group_size == 0
def q_learning(env, alpha, gamma, num_episodes, exploration_decay, group_size):

    # because initially the agent will know nothing
    exploration_rate = 1
    min_exploration_rate = 0.001

    q_table = np.zeros((env.num_states, env.num_actions))

    # will hold the rewards from all the episodes so we can see how they change as it progresses
    rewards_all_episodes = []

    # Q learning
    # Everything that happens within a single episode
    for episode in range(num_episodes):
        state = env.reset()

        rewards_current_episode = 0

        # everything that happens for a single time step in each episode
        steps_needed = 0
        for step in range(26):  # 26 becuase we dont want the agent to select letters more than once
            steps_needed = step + 1

            # agent will exploit
            if random.uniform(0, 1) > exploration_rate:
                action = np.argmax(q_table[state, :])
            else:  # agent will explore
                action = random.choice(env.actions)

            next_state, reward, complete = env.step(action)

            # Update Q table for Q(s,a)
            q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * np.max(q_table[next_state, :]) - q_table[state, action])

            state = next_state
            rewards_current_episode += reward

            # message was decrypted
            if complete:
                print("Episode " + str(episode + 1) + ": " + str(steps_needed) + ' trial(s) needed.')
                break

        exploration_rate = min_exploration_rate + (1 - min_exploration_rate) * np.exp(-exploration_decay * episode)

        rewards_all_episodes.append(rewards_current_episode)

    # ----------------- Stats , figures -------------------
    rewards_per_group_size= np.split(np.array(rewards_all_episodes), num_episodes/group_size)
    out = []
    count = group_size
    print("********** Average rewards **********")
    print("Trials: Avg Reward")
    for r in rewards_per_group_size:
        print(count, ": ", str(sum(r/group_size)))
        out.append(sum(r/group_size))
        count += group_size

    print("********** Calculated Optimal Policy **********")
    print_optimal_policy(q_table)

    plt.plot(range(0, num_episodes, group_size), out)
    plt.ylabel("Reward")
    plt.xlabel("Trials")
    plt.show()

    return rewards_all_episodes


def print_optimal_policy(q_table):
    alphabet = [chr(ascii_char) for ascii_char in range(97, 123)]
    optimal_shifts = list()
    for i in range(len(q_table)):
        optimal_shifts.append(np.argmax(q_table[i]))

    optimal_policy = zip(alphabet, optimal_shifts)
    for action in optimal_policy:
        print(action)