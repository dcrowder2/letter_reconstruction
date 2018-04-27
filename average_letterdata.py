import ann
import numpy as np

feature_vector = []
with open("bitstrings.txt") as file:
    i = 0
    for line in file:
        line = line.split(" ")
        temp = [float(line[0])]
        print("Reading line " + str(i))
        i += 1
        for value in line[1]:
            # if value != "\n":
            if value == "0":
                temp.append(.1)
            else:
                temp.append(.9)
        # print(np.array(temp).shape)
        feature_vector.append(np.array(temp))
features = np.array(feature_vector)
count = np.zeros(27)
fitness = ann.fitness_value(np.array(features))
print(fitness.shape)
print(features.shape)
# i = 0
# for letter in features:
#     count[int(letter[0])] += fitness[i]
#     i += 1
# average = count/55
# np.savetxt("average_output.txt", np.array(average))


