import matplotlib.pyplot as plt
from find_best_probeset import *
from optimum import Optimum

sifnificance_level = pow(10, -8)
meaningful_simulation_num = 10

for n in range(5, 9):
    for k in range(2, n):

        colors = np.arange(0, 1, 1 / n)

        fake_y = np.ones(n)
        fake_y_selected = np.ones(k)

        counter = 0
        while counter < meaningful_simulation_num:

            x = sorted(np.random.randint(1, 1000, size=n))

            inputData = np.divide(x, 1000)

            # plot the NoneOrAll cases
            # maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_XorY_case(inputData, 0, n, k, sifnificance_level)
            # plot the exactOne cases
            maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_ExactX_case(inputData, 1, k,
                                                                                          sifnificance_level)

            if significant == Optimum.TRUE:
                y = fake_y + counter
                plt.scatter(x, y, c=colors, marker='o', alpha=0.3, cmap='plasma')
                for maxSet in maxSets:
                    print(inputData)
                    print(maxSet)
                    x_selected = np.array(x)[list(maxSet)]
                    y_selected = fake_y_selected + counter
                    plt.scatter(x_selected, y_selected, c='black', alpha=1, marker='o', s=20)
                counter += 1

        plt.grid(axis='y')
        plt.yticks(np.arange(0, meaningful_simulation_num + 1, 1))
        plt.title("n= " + str(n) + ", k=" + str(k))
        plt.show()
        plt.close()
