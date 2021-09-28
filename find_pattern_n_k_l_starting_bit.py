import pandas as pd
import numpy as np
from find_best_probeset import computeUforAllPossibleS_threshold_case
import statistics
from optimum import Optimum

sifnificance_level = pow(10, -8)
loggingLevel = 0
simulation_num = 1000

n = 5
df = pd.DataFrame({'k': range(2, n)})

for n in range(n, n + 1):
    for l in range(2, n):
        ls = []
        for k in range(2, n):
            print("######################################################")
            # run ${simulation_num} meaningful simulations
            any_instances = 0 # how many of the ${simulation_num} instances are those who are indifferent to probeset?
            true_instances = 0 # how many of ... are those which we are interested in: exists a real optimum!
            pseudo_instances = 0 # how many of ... are those, who have a max-probeset but rather shaky...
            startingBits = []
            while any_instances + true_instances < simulation_num:
                inputData = sorted(np.random.rand(n))
                inputData = np.round(inputData, 3)
                violate = False
                maxSets, maxU, secondBestU, optimumType = computeUforAllPossibleS_threshold_case(inputData, l, k,
                                                                                                 sifnificance_level)
                if optimumType == Optimum.ANY:
                    any_instances += 1
                elif optimumType == Optimum.TRUE:
                    true_instances += 1
                for maxSet in maxSets:
                    startingBits.append(maxSet[0])
                else: # pseudo, ignore
                    pseudo_instances += 1
            # look at the result
            if len(startingBits) > 0:
                averageStartingBit = round(statistics.mean(startingBits), 3)
                ls.append(averageStartingBit)
                print("n=", n, ",l=", l, ",k=", k, ", #ANY_instances=", any_instances, ",#true_instances=",
                      true_instances, "average starting bit=", averageStartingBit)
            else:
                print("n=", n, ",l=", l, ",k=", k, "all instances are ANY.")
        df["l" + str(l)] = ls

print(df)

# if you want to save the df to a file, comment out the following line
# df.to_pickle("n="+str(n)+".pkl")
