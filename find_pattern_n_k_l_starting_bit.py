import pandas as pd
import numpy as np
from find_best_probeset import computeUforAllPossibleS
import statistics

sifnificance_level = pow(10, -8)
loggingLevel = 0
simulation_num = 100

n = 5
df = pd.DataFrame({'k': range(2, n)})

for n in range(n, n + 1):
    for l in range(2, n):
        ls = []
        for k in range(2, n):
            print("######################################################")
            # run ${simulation_num} meaningful simulations
            meaningful = 0
            startingBits = []
            while meaningful < simulation_num:
                inputData = sorted(np.random.rand(n))
                inputData = np.round(inputData, 3)
                violate = False
                maxSets, maxU, secondBestU, signif = computeUforAllPossibleS(
                    inputData, l, k, sifnificance_level, 0)
                if signif == True:
                    meaningful += 1
                    for maxSet in maxSets:
                        startingBits.append(maxSet[0])
            averageStartingBit = statistics.mean(startingBits)
            ls.append(averageStartingBit)
            print("n=", n, ",l=", l, ",k=", k, "average starting bit:",
                  averageStartingBit)
        df["l" + str(l)] = ls

print(df)

# if you want to save the df to a file, comment out the following line
# df.to_pickle("n="+str(n)+".pkl")
