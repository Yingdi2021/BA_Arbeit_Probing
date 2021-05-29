import numpy as np
import logging
from find_best_probeset import computeUforAllPossibleS_XOR_case
from optimum import Optimum


def xorGreedy(inputdata, k):
    scores = np.absolute(np.subtract(inputData * 2, 1))
    scores = np.round(scores, 3)
    a = 0
    b = len(inputdata) - 1
    while b - a >= k:
        if scores[a] > scores[b]:
            a += 1
        else:  # scores[a] < scores[b]:
            b -= 1
    return np.arange(a, b + 1, 1), scores

def GreedyResultInconsistentWithMaxSet(maxSet, greedyResultSet, scores, inputData):
    maxSet = np.asarray(maxSet)

    # 1. if they are exactly the same --ok!
    comparison = maxSet == greedyResultSet
    if comparison.all():
        return False

    # 2. if they are one-bit shifted from each other due to the repeating value in scores --ok!
    comparison1 = maxSet == np.add(greedyResultSet,1)
    comparison2 = maxSet == np.subtract(greedyResultSet,1)
    if comparison1.all() and scores[greedyResultSet[0]]==scores[maxSet[-1]]:
        return False
    if comparison2.all() and scores[greedyResultSet[-1]]==scores[maxSet[0]]:
        return False

    # 3. if they are only different in those bits, who have the same probs (in inputData) -- ok!
    temp = False
    comparison = maxSet == greedyResultSet
    for i in range(len(comparison)):
        if not comparison[i]:
            if inputData[maxSet[i]] != inputData[greedyResultSet[i]]:
                temp = True
    if not temp:
        return False

    # if none of above is the case, then ---> inconsistent. Violation observed.
    return True

simulation_nr_per_parameter_combination = 500
sifnificance_level = pow(10, -8)

for n in range(4, 11):
    for k in range(2, n + 1):
        violation_moreThanOneOptimal = 0
        violation_differentOptimal = 0
        violationOptimalProbeSets = set()
        violation = False
        for i in range(simulation_nr_per_parameter_combination):

            violation_for_this_instance = False

            inputData = sorted(np.random.rand(n))
            inputData = np.round(inputData, 3)

            # find the optimal probe-set(s) for this random input.
            maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_XOR_case(inputData, k, sifnificance_level)

            # and the probe-set returned by the greedy algorithm?
            greedyResultSet, scores = xorGreedy(inputData, k)

            # go through the real optimal-set(s) and make sure everything will also be predicted by greedy
            for maxSet in maxSets:
                if GreedyResultInconsistentWithMaxSet(maxSet, greedyResultSet, scores, inputData):
                    violation_for_this_instance = True

            # TODO go through all set(s) returned by Greedy and make sure they are all indeed optimal

            if violation_for_this_instance:
                print("input data:", inputData)
                print("scores: ", np.absolute(np.subtract(inputData * 2, 1)))
                print("n=%s, k=%s, maxSets is: " % (n, k))
                for maxSet in maxSets:
                        print(np.asarray(maxSet))
                print("set returned by greedy is: %s" % greedyResultSet)
                print("violation!")
                violation = True
        print("n=%s, k=%s, any violation?: %s" % (n, k, violation))

