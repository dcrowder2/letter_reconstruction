import ann
import numpy as np
import random
from PIL import Image

real_values = np.genfromtxt("average_output.txt")

def genjpg(bitstring, filename):
    canvas = Image.new("RGB", (50, 50), 'white')
    pixels = canvas.load()
    for i in range(50):
        for j in range(50):
            value = bitstring[50 * i + j]
            if value == '0':
                pixels[i, j] = (0, 0, 0)
    canvas.save(filename)


# Fitness will feed through the ANN, and return an array with the fitness of each organism
# in: [[letter, 1,0,0,..], [letter, 0,1,1,..], ..]
# out: [fitness, fitness, ..]
def fitness(matrix):
    ret_array = ann.fitness_value(matrix)
    # real_comparison = real_values - ret_array  TODO: fix ValueError: operands could not be broadcast together with shapes (27,) (2600,)
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
# 2501 features
# will return an list of the next generation chosen via fitness proportionate 1-point crossover and bitwise mutation
# Assumptions: population is a 2d list of each individual in the population
# fitness is a list of the respective fitness of each individual
def reproduce(population):
    fit = fitness(population)
    next_generation = []
    mating_pool = []
    roulette_wheel = []
    generation_fitness = sum(fit)
    for individual in range(len(population)):
        inv_fitness = int(round(float(fit[individual]) / generation_fitness * len(population)))
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
                child_one = list(mating_pool[0][0:split_points[0]])
                child_two = list(mating_pool[0][0:split_points[0]])
                for i in range(2, len(split_points)):
                    child_one.extend(mating_pool[0][split_points[i-1]:split_points[i]])
                    child_two.extend(mating_pool[0][split_points[i-1]:split_points[i]])
                child_one = mutation(child_one, 1 / len(population))
                child_two = mutation(child_two, 1 / len(population))
                next_generation.extend(np.array([np.array(child_one), np.array(child_two)]))
                del mating_pool[0]
                del mating_pool[0]
        if len(mating_pool) >= 1:
            reproduction_chance = random.random()
            if reproduction_chance < .05:
                clone = mutation(mating_pool[0], 1 / len(population))
                next_generation.append(np.array(clone))
                del mating_pool[0]
    return np.array(next_generation)


if __name__ == '__main__':
    print("Starting")
    population_size = 100
    generation_limit = 100
    candidates = []
    print("Generating starting organisms")
    for j in range(26):
        for i in range(int(population_size)):
            image = [j + 1]
            image.extend(list(np.random.choice([0, 1], size=(2501,))))
            candidates.append(np.array(image))
    candidates = np.array(candidates)
    avg_gen_fitness = []
    best_fitness = 0
    print("Starting genetic algorithm...")
    for generation in range(int(generation_limit)):
        print(candidates.shape)
        print("Generation " + str(generation+1))
        fit = fitness(candidates)
        avg_gen_fitness.append(float(np.sum(fit)) / len(fit))
        gen_best_fitness = fit[np.argmax(fit)]
        print("Best fitness " + str(gen_best_fitness) + " and average fitness " + str(float(np.sum(fit)) / len(fit)))
        if gen_best_fitness > best_fitness:
            best_fitness = gen_best_fitness
            best = candidates[np.argmax(fit)]
            best_generation = generation
        candidates = reproduce(candidates)


    print("Best fit individual found in generation " + str(best_generation) + " with a fitness of " + str(best_fitness))
    genjpg(best[1:], "Best.jpg")
