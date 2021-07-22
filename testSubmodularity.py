import logging
import numpy as np
import itertools
from find_best_probeset import myUtilityForXorYcases_silent, myUtilityForXORcases, myUtilityForExactXCases
from scenario import Scenario

def findsubsets(set, subset_size):
    return list(itertools.combinations(set, subset_size))


###################################################
# scenario = Scenario.NONE
# scenario = Scenario.EXACT1
scenario = Scenario.ALL
# scenario = Scenario.NONEORALL
# scenario = Scenario.XOR
###################################################


inputData = np.array([0.1, 0.2, 0.4, 0.8, 0.9])
n = len(inputData)
N = set(range(n))

violation = False

# |A| = 1, 2, 3, ... (n-2)
for a_size in range(1, n-1):

    for a in findsubsets(set(range(n)), a_size):
        R1 = N - set(a)
        # logging.debug("A=%s, R1=%s", set(a), R1)

        # |A| + 1 = |B|
        for BminusA in R1:
            A = set(a)
            B = A.copy()
            B.add(BminusA)
            logging.debug("A=%s, B=%s", A, B)

            # i is a single bit from N-B
            R2 = N - B
            for i in R2:
                logging.debug("i=%s", i)
                # logging.debug("compare u(A+i)-u(A) and u(B+i)-u(B):")
                ai = A.copy()
                ai.add(i)
                bi = B.copy()
                bi.add(i)
                logging.debug("ai=%s, bi=%s", ai, bi)

                if scenario == Scenario.NONE:
                    utility_a = myUtilityForExactXCases(inputData, 0, len(A),A)
                    utility_ai = myUtilityForExactXCases(inputData, 0, len(ai),ai)
                    utility_b = myUtilityForExactXCases(inputData, 0, len(B),B)
                    utility_bi = myUtilityForExactXCases(inputData, 0, len(bi),bi)
                elif scenario == Scenario.EXACT1:
                    utility_a = myUtilityForExactXCases(inputData, 1, len(A),A)
                    utility_ai = myUtilityForExactXCases(inputData, 1, len(ai),ai)
                    utility_b = myUtilityForExactXCases(inputData, 1, len(B),B)
                    utility_bi = myUtilityForExactXCases(inputData, 1, len(bi),bi)
                elif scenario == Scenario.ALL:
                    utility_a = myUtilityForExactXCases(inputData, n, len(A),A)
                    utility_ai = myUtilityForExactXCases(inputData, n, len(ai),ai)
                    utility_b = myUtilityForExactXCases(inputData, n, len(B),B)
                    utility_bi = myUtilityForExactXCases(inputData, n, len(bi),bi)
                elif scenario == Scenario.NONEORALL:
                    utility_a = myUtilityForXorYcases_silent(inputData,0,n,len(A),A)
                    utility_ai = myUtilityForXorYcases_silent(inputData,0,n,len(ai),ai)
                    utility_b = myUtilityForXorYcases_silent(inputData,0,n,len(B),B)
                    utility_bi = myUtilityForXorYcases_silent(inputData,0,n,len(bi),bi)
                elif scenario == Scenario.XOR:
                    utility_a = myUtilityForXORcases(inputData, A)
                    utility_ai = myUtilityForXORcases(inputData, ai)
                    utility_b = myUtilityForXORcases(inputData, B)
                    utility_bi = myUtilityForXORcases(inputData, bi)

                delta_a = utility_ai - utility_a
                delta_b = utility_bi - utility_b

                logging.debug("u_a=%s, u_ai=%s, delta_a=%s, u_b=%s, u_bi=%s, delta_b=%s", utility_a, utility_ai,
                              round(delta_a,3), utility_b, utility_bi, round(delta_b,3))
                if delta_a < delta_b:
                    violation = True
                    logging.error("Voilation!! inputdata=%s, A=%s, B=%s, i=%s: delta_a=%s, delta_b=%s", inputData,A,
                                  B,i, delta_a, delta_b)





