import matplotlib.pyplot as plt
import numpy as np
from find_best_probeset import computeUforAllPossibleS_ExactX_case, findsubsets
from optimum import Optimum

n = 4
k = 3
possible_bits = np.linspace(0.1, 0.9, 9)
combinations = findsubsets(set(range(9)), n)

for combi in combinations:
    print(combi)


sifnificance_level = pow(10, -8)
simulation_num_per_figure = 18

colors = np.arange(0, 1, 1 / n)

fake_y = np.ones(n)
fake_y_selected = np.ones(k)
counter = 0
for combi in combinations:
    inputData = possible_bits[list(combi)]
    print("inputdata=", inputData)
    x = np.multiply(inputData, 1000)
    maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_ExactX_case(inputData, 1, k, sifnificance_level)
    print(significant)

    if significant == Optimum.TRUE:
        y = fake_y + counter
        plt.scatter(x, y, c=colors, marker='o', alpha=0.3, cmap='Accent')
        print("maxSet(s):")
        for maxSet in maxSets:
            print(maxSet)
            x_selected = np.array(x)[list(maxSet)]
            y_selected = fake_y_selected + counter
            plt.scatter(x_selected, y_selected, c='black', alpha=1, marker='o', s=20)
        counter += 1

    if counter == simulation_num_per_figure:
        plt.grid(axis='y')
        plt.xticks(np.linspace(0, 1000, 11), ['0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1'])
        plt.xlabel("p")
        plt.yticks(np.arange(0, simulation_num_per_figure + 1, 1))
        plt.ylabel("instance Nr")
        plt.title("n= " + str(n) + ", k=" + str(k))
        plt.show()
        plt.close()
        counter = 0

