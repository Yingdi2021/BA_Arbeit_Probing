import numpy as np
import logging
from find_best_probeset import computeUforAllPossibleS_XOR_case
from optimum import Optimum


def xorGreedy(inputdata, k):
    scores = np.absolute(np.subtract(inputData * 2, 1))
    a = 0
    b = n - 1
    while b - a >= k:
        if scores[a] > scores[b]:
            a += 1
        else:  # scores[a] < scores[b]:
            b -= 1
    return np.arange(a, b + 1, 1)


simulation_nr_per_parameter_combination = 500
sifnificance_level = pow(10, -8)

for n in range(4, 11):
    for k in range(2, n + 1):
        violation_moreThanOneOptimal = 0
        violation_differentOptimal = 0
        violationOptimalProbeSets = set()
        for i in range(simulation_nr_per_parameter_combination):
            inputData = sorted(np.random.rand(n))
            inputData = np.round(inputData, 3)
            logging.debug("input data=%s", inputData)

            # find the optimal probe-set(s) for this random input.
            maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_XOR_case(inputData, k, sifnificance_level)

            # and the probe-set returned by the greedy algorithm?
            greedyResultSet = xorGreedy(inputData, k)

            # check if the optimal probe-set found is the same as
            if significant == Optimum.TRUE:
                # if len(maxSets) > 1:
                for maxSet in maxSets:
                    comparison = np.asarray(maxSet) == greedyResultSet
                    if comparison.all():
                        continue
                        # print("the same. Greedy is correct!")
                    else:
                        print("input data:", inputData)
                        print("scores: ", np.absolute(np.subtract(inputData * 2, 1)))
                        print("n=%s, k=%s, maxSet is: %s" % (n, k, np.asarray(maxSet)))
                        print("n=%s, k=%s, set returned by greedy is: %s" % (n, k, greedyResultSet))
                        print("violation!")
