import matplotlib.pyplot as plt
import numpy as np

from find_best_probeset import *
from optimum import Optimum

sifnificance_level = pow(10, -8)
simulation_num_per_figure = 20
repitition_num = 1

for n in range(4, 10):
    for k in range(2, n):
        for rep in range(repitition_num):
            colors = np.arange(0, 1, 1 / n)

            fake_y = np.ones(n)
            fake_y_selected = np.ones(k)

            counter = 0
            while counter < simulation_num_per_figure:

                x = sorted(np.random.randint(501, 1000, size=n))
                # x[-1] = 999
                # x = sorted(np.random.randint(1, 499, size=n))

                inputData = np.divide(x, 1000)
                # inputData =np.array([0.068, 0.214, 0.377, 0.529, 0.613])
                # x = np.multiply(inputData, 1000)

                # plot the NoneOrAll cases
                maxSets, maxU, secondBestU, optimumType = computeUforAllPossibleS_XorY_case(inputData, 0, n, k, sifnificance_level)
                # plot the exactOne cases
                # maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_ExactX_case(inputData, 1, k, sifnificance_level)
                # plot the XOR cases
                # maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_XOR_case(inputData, k, significance_level)


                if optimumType == Optimum.TRUE:
                    y = fake_y + counter
                    plt.scatter(x, y, c=colors, marker='o', alpha=0.3, cmap='plasma')
                    for maxSet in maxSets:
                        print(inputData)
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
