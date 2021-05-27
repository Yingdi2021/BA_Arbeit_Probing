import logging

import numpy as np
from find_best_probeset import computeUforAllPossibleS_threshold_case
from find_best_probeset import computeUforAllPossibleS_ExactX_case
from find_best_probeset import computeUforAllPossibleS_XorY_case
from optimum import Optimum

#################### Helper-functions #########################
# check if a given sub-set is consecutive. e.g. 234, 123, 3456, etc
# if the in-consecutivity is caused exclusively by repeating values
# in the input-data, it will still been seen as consecutive.
def checkIfConsecutiveRepeatingValueSafe(theSet, inputData):
    selectedElements = set(inputData[list(theSet)])
    remainElements = set(inputData)-selectedElements
    consecutive = True
    for i in remainElements:
        if (i <max(selectedElements)) and (i>min(selectedElements)):
            consecutive = False
    return consecutive

# deprecated: this function is too strict.
# use checkIfConsecutiveRepeatingValueSafe instead.
def checkIfConsecutive(set):
    sortedSet = sorted(list(set))
    return sortedSet == list(range(sortedSet[0], sortedSet[-1]+1))
################################################################

####################### Simulation #############################
def test_conjecture_threshold_case(simulation_nr_per_combination):
    for n in range(4, 11):
        for l in range(4,n+1):
            for k in range(2, n+1):
                violate = False
                for i in range(simulation_nr_per_combination):
                    inputData = sorted(np.random.rand(n))
                    inputData = np.round(inputData, 3)

                    # find optimal probe-set(s) for this random input. surpress output
                    maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_threshold_case(inputData, l, k,
                                                                                                     sifnificance_level)

                    # check if the optimal probe-set(s) violates our conjecture
                    if significant == True: # of course only when it's significant
                        for maxSet in maxSets:
                            if not checkIfConsecutiveRepeatingValueSafe(maxSet, inputData):
                                violate = True
                                print("n=", n, ",l=",l, ",k=", k,"violation!", maxSet, np.array(inputData)[list(maxSet)], "inputData：", inputData)

                print("n=", n, ",l=",l, ",k=", k,"finished. Any violation?", violate)

def test_conjecture_exactX_case(simulation_nr_per_combination):
    for n in range(4, 11):
        for m in range(1,2):
            for k in range(2, n):
                violate = False
                any_instances = 0
                true_instances = 0
                violationOptimalProbeSets = set()
                for i in range(simulation_nr_per_combination):
                    inputData = sorted(np.random.rand(n))
                    inputData = np.round(inputData, 3)

                    # find optimal probe-set(s) for this random input. surpress output
                    maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_ExactX_case(inputData, m, k,
                                                                                                  sifnificance_level)
                    # check if the optimal probe-set(s) violates our conjecture
                    if significant == Optimum.ANY:
                        any_instances += 1
                    elif significant == Optimum.TRUE: # of course only when it's significant
                        true_instances += 1
                        for maxSet in maxSets:
                            if not checkIfConsecutiveRepeatingValueSafe(maxSet, inputData):
                                violate = True
                                # print("n=", n, ",m=",m, ",k=", k, "violation!", maxSet, np.array(inputData)[list(maxSet)], "inputData：", inputData)
                                violationOptimalProbeSets.add(maxSet)
                print("n=", n, ",m=",m, ",k=", k,"finished. Any violation?", violate)
                if violate:
                    print("non-consecutive optimal-Probeset(s):", violationOptimalProbeSets)

def test_conjecture_XorY_case(simulation_nr_per_combination):
    for n in range(4, 11):
        for x in range(0,1):
            for y in range(n,n+1):
                for k in range(2, n+1):
                    violate = False
                    violationOptimalProbeSets = set()
                    for i in range(simulation_nr_per_combination):
                        inputData = sorted(np.random.rand(n))
                        inputData = np.round(inputData, 3)
                        logging.debug("input data=%s", inputData)

                        # find optimal probe-set(s) for this random input. surpress output
                        maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_XorY_case(inputData, x, y, k,
                                                                                                    sifnificance_level)

                        # check if the optimal probe-set(s) violates our conjecture
                        if significant == Optimum.TRUE: # of course only when there's a true optimal subset
                            for maxSet in maxSets:
                                logging.debug("n=%s, k=%s, maxSet found: %s", n,k,maxSet)
                                if not checkIfConsecutiveRepeatingValueSafe(maxSet, inputData):
                                    violate = True
                                    # print("n=", n, ",m=",m, ",k=", k, "violation!", maxSet, np.array(inputData)[list(maxSet)], "inputData：", inputData)
                                    violationOptimalProbeSets.add(maxSet)

                    print("n=", n, ",x=",x, "y=",y, ",k=", k,"finished. Any violation?", violate)
                    if violate:
                            print("optimal Probeset(s):", violationOptimalProbeSets)

sifnificance_level = pow(10, -8)
simulation_nr_per_combination = 1000

# test the conjecture for the classical threshold case
# test_conjecture_threshold_case(simulation_nr_per_combination)

# test the conjecture for the exactX case
test_conjecture_exactX_case(simulation_nr_per_combination)

# test the conjecture for the none_or_all case
# test_conjecture_XorY_case(simulation_nr_per_combination)