

# Matrix will be a similar construction to the dataset described by this,
# https://archive.ics.uci.edu/ml/machine-learning-databases/letter-recognition/letter-recognition.names
# it will feed through the ANN, and return an array with the fitness of each organism
# in: [[letter, features..], [letter, features..], ..]
# out: [fitness, fitness, ..]
def fitness(matrix):
    # TODO by Dakota
    return []


# This will take in the bit string/map of the pixels for the generated letters and create the feature vector based on
# https://archive.ics.uci.edu/ml/machine-learning-databases/letter-recognition/letter-recognition.names
# in: [[letter, 0, 1, 0, ..], [letter, 1,0,1, ..], ..]
# out: [[letter, features..], [letter, features], ..]
def prepare_data(organisms):
    # TODO by Henry/Dakota
    return []


# Takes in the current generation of organisms and creates the next generation using recombination and mutation
# in: [[letter, 0, 1, 0, ..], [letter, 1,0,1, ..], ..]
# out: [[letter, 0, 1, 0, ..], [letter, 1,0,1, ..], ..]
def reproduce(organisms):
    fit = fitness(prepare_data(organisms))
    # TODO by Dakota/Henry, maybe just reuse code from PA1
    return []

