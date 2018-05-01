import ann
import numpy as np
import random
from PIL import Image


def outliers(bitstring):
    outlier = 0
    for i in range(2, len(bitstring)):
        bit = bitstring[i]
        lastbit = bitstring[i-1]
        lastlastbit = bitstring[i-2]
        if lastlastbit == 0 and lastbit == 1 and bit == 0:
            outlier += 1
    return outlier


def get_char(number):
    return chr(65 + number)


def genjpg(bitstring, filename):
    canvas = Image.new("RGB", (50, 50), 'white')
    pixels = canvas.load()
    for i in range(50):
        for j in range(50):
            value = bitstring[50 * i + j]
            if value == 0:
                pixels[i, j] = (0, 0, 0)
    canvas.save(filename)


# Fitness will feed through the ANN, and return an array with the fitness of each organism
# in: [[[1,0,1,...], ...][[1,0,1,0,...],...], ...] shape: (letter, organism, feature)
# out: [[fitness, fitness, ..], ...] shape: (letter, organism_fitness)
def fitness(matrix):
    for_fitness = []
    size = []

    for i in range(26):
        size.append(len(matrix[i]))
        for_fitness.extend(matrix[i])
    ret_array = ann.fitness_value(size, for_fitness)
    real_comparison = ann.real_comparison(size, for_fitness)
    outliers_count = []
    for i in range(26):
        temp = []
        for j in range(len(matrix[i])):
            temp.append(outliers(matrix[i, j]))
        outliers_count.append(temp)
    return real_comparison + outliers_count


# uses the chance provided by the calling method to randomly mutate on one point if it is chosen to mutate
# Assumptions: individual is a list of 0's, and 1's, chance is a float from 0.0 to 1.0
def mutation(individual, chance):
    mutation_chance = random.random()
    mutated_individual = individual
    if mutation_chance < chance:
        mutate_point = random.randint(0, (len(individual)-1))
        if individual[mutate_point] == 0:
            mutated_individual[mutate_point] = 1
        else:
            mutated_individual[mutate_point] = 0
    return mutated_individual


# Takes in the current generation of organisms and creates the next generation using recombination and mutation
# in: [[[1,0,1,...], ...][[1,0,1,0,...],...], ...] shape: (letter, organism, feature)
# out: [[[1,0,1,...], ...][[1,0,1,0,...],...], ...] shape: (letter, organism, feature)
# 2501 features
# will return an list of the next generation chosen via fitness proportionate 1-point crossover and bitwise mutation
# Assumptions: population is a 2d list of each individual in the population
# fitness is a list of the respective fitness of each individual
def reproduce(population):
    fit = fitness(population)

    next_generation = []

    for i in range(26):
        mating_pool = []
        roulette_wheel = []
        generation_fitness = sum(fit[i])
        for individual in range(len(population[i])):
            inv_fitness = int(round((fit[i, individual] / generation_fitness) * len(population[i])))
            for number in range(inv_fitness):
                roulette_wheel.append(individual)

        while len(mating_pool) < len(population[i]):
            spin = random.randint(0, (len(roulette_wheel) - 1))
            mating_pool.append(population[i, roulette_wheel[spin]])

        letter_population = len(mating_pool)
        letter_next_generation = []
        while len(letter_next_generation) < letter_population:
            if len(mating_pool) >= 2:
                crossover_chance = random.random()

                if crossover_chance < .95:

                    split_points = []
                    for i in range(10):
                        split_points.append(random.randint(1, len(population[0])))
                    split_points.sort()

                    child_one = mating_pool[0][0:split_points[0]].tolist()
                    child_two = mating_pool[1][0:split_points[0]].tolist()

                    for i in range(1, len(split_points)):
                        bit = i % 2
                        obit = (i + 1) % 2
                        child_one.extend(mating_pool[bit][split_points[i-1]:split_points[i]].tolist())
                        child_two.extend(mating_pool[obit][split_points[i-1]:split_points[i]].tolist())

                    child_one.extend(mating_pool[obit][split_points[-1]:])
                    child_two.extend(mating_pool[bit][split_points[-1]:])

                    child_one = mutation(child_one, 1 / len(population[i]))
                    child_two = mutation(child_two, 1 / len(population[i]))

                    letter_next_generation.extend([child_one, child_two])
                    del mating_pool[0]
                    del mating_pool[0]

            if len(mating_pool) >= 1:
                reproduction_chance = random.random()
                if reproduction_chance < .05:
                    clone = mutation(mating_pool[0], 1 / len(population))
                    letter_next_generation.append(np.array(clone))
                    del mating_pool[0]
        next_generation.append(letter_next_generation)
    return np.array(next_generation)


if __name__ == '__main__':
    print("Starting")

    population_size = 100
    generation_limit = 50
    candidates = [[] for i in range(26)]

    print("Generating starting organisms")

    for j in range(26):
        for i in range(int(population_size)):
            image = list(np.random.choice([0, 1], size=(2501,)))
            candidates[j].append(np.array(image))
    candidates = np.array(candidates)

    avg_gen_fitness = [[] for i in range(26)]
    best_fitness = np.full(26, 99999999.)
    best_generation = np.zeros(26)
    best = [[] for i in range(26)]

    print("Starting genetic algorithm...")

    for generation in range(int(generation_limit)):
        print("Generation " + str(generation+1))

        fit = fitness(candidates)
        for i in range(26):
            temp_avg = float(np.sum(fit[i])) / len(fit[i])
            avg_gen_fitness[i].append(temp_avg)
            letter_gen_best_fitness = fit[i][np.argmin(fit[i])]

            print("Best fitness for letter " + get_char(i) + " is " + str(letter_gen_best_fitness) +
                  " and average fitness " + str(temp_avg))

            if letter_gen_best_fitness < best_fitness[i]:
                best_fitness[i] = letter_gen_best_fitness
                best[i] = candidates[i, np.argmin(fit[i])]
                best_generation[i] = int(generation) + 1

        candidates = reproduce(candidates)

    for i in range(26):
        print("Best fit " + get_char(i) + " individual found in generation " + str(best_generation[i])
              + " with a fitness of " + str(best_fitness[i]))
        genjpg(best[i], "Best_" + get_char(i) + ".jpg")
