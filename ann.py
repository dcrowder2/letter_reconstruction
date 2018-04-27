import numpy as np


def ann():
    w1 = np.genfromtxt("weights1(.77622).txt")
    w2 = np.genfromtxt("weights2(.77622).txt")

    def sigmoid(number):
        return 1 / (1 + np.exp(-number))

    def soft_max(array):
        z = np.sum(np.exp(array))
        return np.exp(array) / z

    def feed_through(data):
        s_1 = np.dot(data[:, 1:], w1)
        z_1 = sigmoid(s_1)

        s_2 = np.dot(z_1, w2)
        z_2 = sigmoid(s_2)
        output = []
        for item in z_2:
            output.append(soft_max(item))
        return output

    def fitness_value(data):
        activations = feed_through(data)
        ret_array = []
        for item in data:
            difference = np.sum(activations[item[0] - 1] - activations)
            ret_array.append(difference)
        return ret_array
