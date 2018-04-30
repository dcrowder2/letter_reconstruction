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

# uses the chance provided by the calling method to randomly mutate on one point if it is chosen to mutate
# Assumptions: individual is a list of 0's, and 1's, chance is a float from 0.0 to 1.0
def mutation(individual, chance):
    mutation_chance = random.random()
    mutated_individual = individual
    if mutation_chance < chance:
        mutate_point = random.randint(0, len(individual))
        if individual[mutate_point] == 0:
            mutated_individual[mutate_point] = 1
        else:
            mutated_individual[mutate_point] = 0
    return mutated_individual

# Takes in the current generation of organisms and creates the next generation using recombination and mutation
# in: [[letter, 0, 1, 0, ..], [letter, 1,0,1, ..], ..]
# out: [[letter, 0, 1, 0, ..], [letter, 1,0,1, ..], ..]
#
# will return an list of the next generation chosen via fitness proportionate 1-point crossover and bitwise mutation
# Assumptions: population is a 2d list of each individual in the population
# fitness is a list of the respective fitness of each individual
def reproduce(population):
    fitness = fitness(population)
    next_generation = []
    mating_pool = []
    roulette_wheel = []
    generation_fitness = sum(fitness)
    for individual in range(len(population)):
        inv_fitness = int(round(float(fitness[individual]) / generation_fitness * len(population)))
        for number in range(inv_fitness):
            roulette_wheel.append(individual)
    while len(mating_pool) < len(population):
        spin = random.randint(0, (len(roulette_wheel) - 1))
        mating_pool.append(population[roulette_wheel[spin]])
    while len(next_generation) < len(population):
        if len(mating_pool) >= 2:
            crossover_chance = random.random()
            if crossover_chance < .95:
                split_points = []
                for i in range(10):
                    split_points.append(random.randint(1, len(population[0])))
                split_points.sort()
                child_one = mating_pool[0][0:split_points[0]]
                child_two = mating_pool[0][0:split_points[0]]
                for i in range(2, len(split_points)):
                    child_one.extend(mating_pool[0][split_points[i-1]:split_points[i]])
                    child_two.extend(mating_pool[0][split_points[i-1]:split_points[i]])
                child_one = mutation(child_one, 1 / len(population))
                child_two = mutation(child_two, 1 / len(population))
                next_generation.extend([child_one, child_two])
                del mating_pool[0]
                del mating_pool[0]
        if len(mating_pool) >= 1:
            reproduction_chance = random.random()
            if reproduction_chance < .05:
                clone = mutation(mating_pool[0], 1 / len(population))
                next_generation.append(clone)
                del mating_pool[0]
    return next_generation

