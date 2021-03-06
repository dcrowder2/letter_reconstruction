import numpy as np

w1 = np.genfromtxt("weights1(.77622).txt")
w2 = np.genfromtxt("weights2(.77622).txt")

real_values = np.genfromtxt("average_output.txt")


def sigmoid(number):
    return 1 / (1 + np.exp(-number))


def soft_max(array):
    z = np.sum(np.exp(array))
    return np.exp(array) / z


def feed_through(data):
    s_1 = np.dot(data, w1)
    z_1 = sigmoid(s_1)

    s_2 = np.dot(z_1, w2)
    z_2 = sigmoid(s_2)
    output = []
    for item in z_2:
        output.append(soft_max(item))
    return output


def fitness_value(size, data):
    ret_array = [[] for no_use in range(26)]
    prev_size = 0
    for i in range(26):
        letter_data = data[prev_size:prev_size + size[i]]
        prev_size += size[i]
        activations = feed_through(letter_data)
        for item in letter_data:
            difference = abs(np.sum(activations[i] - activations))
            ret_array[i].append(difference)
    return np.array(ret_array)


def real_comparison(size, data):
    ret_array = [[] for no_use in range(26)]
    prev_size = 0
    for i in range(26):
        letter_data = data[prev_size:prev_size + size[i]]
        prev_size += size[i]
        activations = feed_through(letter_data)
        for item in letter_data:
            difference = abs(np.sum(activations - real_values[i]))
            ret_array[i].append(difference)
    return np.array(ret_array)