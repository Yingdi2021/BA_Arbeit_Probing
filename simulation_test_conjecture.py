import numpy as np
from find_best_probeset import computeUforAllPossibleS_threshold_case

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
sifnificance_level = pow(10, -8)

for n in range(4, 11):
    for l in range(4,n+1):
        for k in range(2, n+1):
            # run 1000 simulations for this combination
            for i in range(1000):
                inputData = sorted(np.random.rand(n))
                inputData = np.round(inputData, 3)
                violate = False

                # find optimal probe-set(s) for this random input. surpress output
                maxSets, maxU, secondBestU, significant = computeUforAllPossibleS_threshold_case(inputData, l, k, sifnificance_level, 0)

                # check if the optimal probe-set(s) violates our conjecture
                if significant == True: # of course only when it's significant
                    for maxSet in maxSets:
                        # print(maxSet)
                        if not checkIfConsecutiveRepeatingValueSafe(maxSet, inputData):
                            violate = True
                            print("n=", n, ",l=",l, ",k=", k,"violation!", maxSet, np.array(inputData)[list(maxSet)], "inputData：", inputData)

            print("n=", n, ",l=",l, ",k=", k,"finished. Any violation?", violate)