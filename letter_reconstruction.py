import ann
import numpy as np

real_values = np.genfromtxt("average_output.txt")


# Fitness will feed through the ANN, and return an array with the fitness of each organism
# in: [[letter, 1,0,0,..], [letter, 0,1,1,..], ..]
# out: [fitness, fitness, ..]
def fitness(matrix):
    ret_array = ann.fitness_value(matrix)
    real_comparison = real_values - ret_array
    return ret_array  # np.abs(real_comparison)


# Takes in the current generation of organisms and creates the next generation using recombination and mutation
# in: [[letter, 0, 1, 0, ..], [letter, 1,0,1, ..], ..]
# out: [[letter, 0, 1, 0, ..], [letter, 1,0,1, ..], ..]
def reproduce(organisms):
    fit = fitness(organisms)
    # TODO by Henry, maybe just reuse code from PA1
    return []

