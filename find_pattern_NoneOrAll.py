import logging
import numpy as np
from find_best_probeset import computeUforAllPossibleS_XorY_case
from optimum import Optimum
import statistics
import pickle

sifnificance_level = pow(10, -8)
simulation_num = 1000

n = 5
x = 0
y = n

true_percentage = []
any_percentage = []
startingBit_average = []
startingBit_std = []

for k in range(2, n):
    any_instances = 0 # how many of the ${simulation_num} instances are those who are indifferent to probeset?
    true_instances = 0 # how many of ... are those which we are interested in: exists a real optimum!
    pseudo_instances = 0 # how many of ... are those, who have a max-probeset but rather shaky...
    startingBits = []
    while any_instances+true_instances < simulation_num:
        inputData = sorted(np.random.rand(n))
        inputData = np.round(inputData, 3)
        maxSets, maxU, secondBestU, signif = computeUforAllPossibleS_XorY_case(inputData,x, y, k, sifnificance_level)

        if signif == Optimum.ANY:
            any_instances += 1
        elif signif == Optimum.TRUE:
            true_instances += 1
            for maxSet in maxSets:
                startingBits.append(maxSet[0])
        else: # pseudo, ignore
            pseudo_instances += 1
    # look at the result
    if len(startingBits)>0:
        averageStartingBit = round(statistics.mean(startingBits),4)
        startingBit_average.append(averageStartingBit)
        if len(startingBits)>1:
            std = round(statistics.stdev(startingBits),3)
        else:
            std = float("Nan")
        startingBit_std.append(std)
        logging.error("n=%s, k=%s, #true_instances=%s (out of %s), average starting bit = %s, std=%s", n, k,
                      true_instances, simulation_num, averageStartingBit, std)
    else:
        logging.error("n=%s, k=%s, #true_instances=%s, all %s instances are ANY.", n, k, true_instances,
                      simulation_num)
        startingBit_average.append(float("Nan"))
        startingBit_std.append(float("Nan"))
    true_percentage.append(true_instances*100/simulation_num)
    any_percentage.append(any_instances*100/simulation_num)

print("true_percentage:", true_percentage)
print("any_percentage:", any_percentage)
print("startingBit_average:", startingBit_average)
print("startingBit_std", startingBit_std)

f = open("none_or_all_n="+str(n)+".pkl", 'wb')
pickle.dump([true_percentage, any_percentage, startingBit_average], f)
f.close()
