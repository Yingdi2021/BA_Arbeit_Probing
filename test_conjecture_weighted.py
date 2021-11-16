import logging
import numpy as np
from weights import computeUforAllPossibleS_WeightedThreshold_case
from optimum import Optimum

def checkIfConsecutiveRepeatingValueSafeOld(theSet, inputData):
    selectedElements = set(inputData[list(theSet)])
    remainElements = set(inputData)-selectedElements
    consecutive = True
    for i in remainElements:
        if (i <max(selectedElements)) and (i>min(selectedElements)):
            return False
    return consecutive

def checkIfConsecutiveRepeatingValueSafe(maxSet, sorted_index):
    selectedElements = set()
    for i in maxSet:
        index = np.where(sorted_index==i)
        selectedElements.add(index[0][0])
    allElements = set(sorted_index)
    remainElements = allElements-selectedElements
    consecutive = True
    for i in remainElements:
        if (i <max(selectedElements)) and (i>min(selectedElements)):
            consecutive = False
    return consecutive

def test_conjecture_weighted(simulation_nr_per_combination):
    for n in range(4, 11):
        for l in range(4,n):
            for k in range(2, n):
                violate = False
                for i in range(simulation_nr_per_combination):
                    pools = [0.1,0.2,0.3,0.4,0.5, 0.6,0.7,0.8, 0.9]
                    inputData =sorted(np.random.choice(pools, n))
                    # inputData = sorted(np.random.rand(n))
                    inputData = np.round(inputData, 1)
                    # generate a random weight array of size n, of which all elements sum up to n.

                    weights = np.random.dirichlet(np.ones(n))*n

                    # find optimal probe-set(s) for this random input.
                    maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_WeightedThreshold_case(
                        inputData, weights, l, k)

                    # weighted inputdata (product of probs and weights) as basis of the sortierung
                    weighted_inputdata = weights * inputData

                    # sorted index of the weighted inputdata
                    sorted_index_weighted_inputdata = np.argsort(weighted_inputdata)

                    # check if the optimal probe-set(s) violates our conjecture
                    if significant == Optimum.TRUE: # of course only when it's significant
                        violationCount = 0
                        for maxSet in maxSets:
                            if not checkIfConsecutiveRepeatingValueSafe(maxSet, sorted_index_weighted_inputdata):
                                violate = True
                                if not checkIfConsecutiveRepeatingValueSafeOld(maxSet, inputData):
                                    violationCount += 1
                                # print("n=", n, ",l=",l, ",k=", k,"violation!", maxSet, np.array(inputData)[list(
                                #     maxSet)], inputData)
                        if violationCount == len(maxSets):
                            print("found!!!!! inputdata=", inputData, "weights= ", weights, "l=", l, "k=", k)


                print("n=", n, ",l=",l, ",k=", k,"finished. Any violation?", violate)

logging.basicConfig(level=logging.CRITICAL)

test_conjecture_weighted(100)


# inputData = np.array([ 0.1, 0.6,  0.7,  0.8,  0.8])
# weights = np.array([ 0.71693381,  2.60902726,  0.81256404,  0.04224317,  0.81923172])
# threshold = 4
# k = 2
# maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_WeightedThreshold_case(
#     inputData, weights, threshold, k)
#
#
# weighted_inputdata = weights * inputData
# print(weighted_inputdata)
# sorted_index_weighted_inputdata = np.argsort(weighted_inputdata)
# print(sorted_index_weighted_inputdata)
# violate = False
# for maxSet in maxSets:
#     consecutive = checkIfConsecutiveRepeatingValueSafe(maxSet, sorted_index_weighted_inputdata.tolist())
#     if not consecutive:
#         violate = True
#         print("violate!")
# if not violate:
#     print("no violation observed.")


