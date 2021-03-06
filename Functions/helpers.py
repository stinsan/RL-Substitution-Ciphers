import os

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

    words_found = 0
    for word in message:
        word = word.lower().strip()
        if word in words or word.isnumeric():
            words_found = words_found + 1
        else:
            c = word[len(word) - 1]
            # removes last char if it is a special symbol
            if not c.isalpha():
                word = word[:-1]
                if word in words or word.isnumeric():
                    words_found = words_found + 1

    return words_found / len(message)


# ---------------------------------------------------------------------------------------
class Letter:
    def __init__(self, letter, frequency):
        self.letter = letter
        self.freq = frequency


def get_letter_frequencies(message):
    # Initialize list with letters [a, b, c, ...] and frequencies initially at 0.
    letter_list = [Letter(chr(letter), 0) for letter in range(97, 123)]

    for letter in message:
        if letter.isalpha():
            if letter.islower():
                index = ord(letter) - 97  # 97 = 'a'
            else:
                index = ord(letter) - 65  # 65 = 'A'

            letter_list[index].freq += 1

    return letter_list


def get_n_most_frequent_letters(letter_list, n):
    ret = list()
    sorted_letters = sorted(letter_list, key=lambda letter: letter.freq, reverse=True)

    for i in range(0, n):
        ret.append(sorted_letters[i].letter)

    return ret


# ---------------------------------------------------------------------------------------,
def shift_message(message, shift):
    message_arr = list(message)

    for i in range(0, len(message_arr)):
        letter = message_arr[i]
        if letter.isalpha():
            message_arr[i] = shift_letter(letter, shift)

    return "".join(message_arr)


def shift_letter(letter, shift):
    offset = ord(letter) + shift

    if letter.isupper() and offset > 90 or letter.islower() and offset > 122:
        offset = ord(letter) + shift - 26

    return chr(offset)


def get_files_in_dir(dir_path):
    file_names = os.listdir(dir_path)

    files = list()
    for file_name in file_names:
        file = os.path.join(dir_path, file_name)
        files.append(file)

    return files

# ---------------------------------------------------------------------------------------,

def compare_SARSA_QLearingPlot(rewards_SARSA, rewards_Q_learning, num_episodes, group_size, title):
    avg_rewards_SARSA = get_avg_reward_by_group(rewards_SARSA, group_size, num_episodes)
    avg_rewards_Q_learning = get_avg_reward_by_group(rewards_Q_learning, group_size, num_episodes)


    plt.plot(range(0, num_episodes, group_size),avg_rewards_SARSA, label = "SARSA")
    plt.plot(range(0, num_episodes, group_size),avg_rewards_Q_learning, label = "Q-learning")
    plt.xlabel('Episode')
    
    # Set the y axis label of the current axis.
    plt.ylabel('Average reward per ' + str(group_size) + ' episodes')
    # Set a title of the current axes.
    plt.title(title)
    # show a legend on the plot
    plt.legend()
    # Display a figure.
    plt.show()

def get_avg_reward_by_group(rewards, group_size, num_episodes):
    rewards_per_group = np.split(np.array(rewards), num_episodes/group_size)
    reward_bin = []
    count = group_size
    for r in rewards_per_group:
        reward_bin.append(sum(r/ group_size))
        count += group_size
    return reward_bin





