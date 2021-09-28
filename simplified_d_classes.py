#----------------------------Problem description------------------------
# The All 1s and XOR scenarios do not need to be simplified (already has polynomial-time algo)
# we focus on the 1) exactly one 1 scenario; 2) at least one 1 (or more generally, at least l 1s); 3) all 1s or all 0s

# Description of this variant:
# instad of having all n boxes independently drawn from (possibly) *n* different distributions, we now have only *d*
# different classes (each associated with a particular distribution) available. So the n boxes consist of: n_1 boxes
# from class 1 (probability of being 1=p_1), n_2 boxes from class 2 (probability of being 1=p_2), .... and n_d boxes
# from class d (probability of being 1=p_d)

# Now we don't have to go through all possible subsets (of size k) to find the optimal probeset. We only have to
# enumerate all possible vectors [k_1, k_2,...k_d] that has a sum of k. i.e., combinations of how many type 1/2/.../d
# boxes we want to probe.
#----------------------------END Problem description------------------------

import numpy as np
import logging
from optimum import Optimum
import itertools
SIGNIFICANCE_LEVEL = pow(10, -8)


#---------------------- Helper Methods------------------------------------
def findsubsets(set, subset_size):
    return list(itertools.combinations(set, subset_size))

def generateInputVector(p1, p2, n1, n2):
    n = n1 + n2
    inputV = np.zeros(n)
    inputV[0:n1]=p1
    inputV[n1::]=p2
    return inputV

def multiplyPand1MinusP(inputData, setP, set1MinusP):
    result = 1
    for i in setP:
        result *= inputData[i]
    for j in set1MinusP:
        result *= (1 - inputData[j])
    return result

def findAllCombinations(n1, n2, k):
    n = n1+n2
    result = list()
    for test1 in range(n1+1):
        for test2 in range(n2+1):
            if test1+test2 == k:
                # one combination found! We will test test1 class1 items and test2 class2 items
                subset_list = []
                for i in range(test1):
                    subset_list.append(i)
                for j in range(n1, n1+test2):
                    subset_list.append(j)
                subset = tuple(subset_list)
                result.append(subset)
    return result



#-------------------------------------Main Methods------------------------------------------------
# calculates the utility (probability of making the right decision)
# given input data, m (how many 1s EXACTLY), k(probe-set size) and S(the probe-set)
# for the exactX case, ie. acceptance criteria is: number of 1s == m
def myUtilityForExactXCases(inputData, m, S):
    k = len(S)
    n = len(inputData)
    N = set(range(n))
    R = N - S

    utility = 0

    # if there are no more than m 1s in the probe-set:
    for d in range(m + 1):
        logging.debug("*********************\nCalculating probability of having excatly %s Eins in the probe-set",d)
        subsets_for_this_d = findsubsets(S, d)
        logging.debug("there are in total %s subsets: %s for d=%s", len(subsets_for_this_d), subsets_for_this_d, d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
            logging.debug("subset:%s, R=%s, p=%s ",set(subset), remaining_nulls, p_subset)
            ps += p_subset
        logging.debug("probability, that there are exactly %s Eins in probe-set is:%s",d, ps)

        r = m - d
        logging.debug("---------------\nCalculating C (Prob that there are excatly %s 1s in R) for d=%s ",r, d)

        c = 0
        if r <= n-k:
            subsets_for_this_m = findsubsets(R, r)
            for subset in subsets_for_this_m:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
                c += p_subset
        logging.debug("probability, that exactly %s Eins in Rest-Set is: %s", r,c)
        logging.debug("choose the more likely! \nWhen there are %s Eins in probe-set: ", d)
        if c>= 0.5:
            logging.debug("it's more likely (p=%s) that this is a good candidate", c)
            logging.debug("--> probability, that d=%s AND we make the right decision is %s",d, ps*c)
            utility += ps*c
        else:
            logging.debug("it's more likely (p=%s) that this is a bad candidate", (1-c))
            logging.debug("--> probability, that d=%s AND we make the right decision is %s",d, ps*(1-c))
            utility += ps*(1-c)

    # if there are more than m 1s in probe-set, we always make the right decision: reject
    if k > m:
        for d in range(m+1,k+1):
            logging.debug("*********************\nif there are %s Eins (>m=%s) in probeset, we always make the right "
                          "decision: reject",d, m)
            subsets_for_this_d = findsubsets(S, d)
            logging.debug("there are in total %s subsets: %s for d=%s", len(subsets_for_this_d), subsets_for_this_d, d)
            ps = 0
            for subset in subsets_for_this_d:
                remaining_nulls = S - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
                logging.debug("subset: %s, R=%s, p=%s ",set(subset), remaining_nulls, p_subset)
                ps += p_subset
            logging.debug("probability, that there are exactly %s Eins in probe-set AND we make the right decision is:%s",d,ps)
            utility += ps

    logging.debug("-------------\nResult:")
    logging.debug("-------------utiliiy=%s when we select the probe-set: %s -----------", utility, S)
    return round(utility,8)


def computeUforAllCombinations_Exact1_case(p1, p2, n1, n2, m, k):

    inputData = generateInputVector(p1, p2, n1, n2)
    logging.debug("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    logging.info("InputData=%s", inputData)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    secondBestUpdated = False

    for probe_set in findAllCombinations(n1, n2, k):
        logging.debug("*****************************************************************")
        logging.debug("possible probeset %s: S=%s --> %s", counter, probe_set, inputData[list(probe_set)])
        counter += 1
        u = myUtilityForExactXCases(inputData, m, set(probe_set))
        # u = myUtilityForXorYcases(inputData, 0, n1+n2, k, S)
        if counter == 1:
            secondBestU = u
            maxU = u
            maxSets = set()
            maxSets.add(probe_set)
        else:
            if u > maxU:
                secondBestU = maxU
                secondBestUpdated = True
                maxU = u
                maxSets = set()
                maxSets.add(probe_set)
            elif u == maxU:
                maxSets.add(probe_set)
        logging.info("when probe-set=%s-->%s, u=%s", set(probe_set), inputData[list(probe_set)], u)

    logging.info("*****************************************************************")
    logging.info("Utility is maximum (%s) when probeset is (one of) the following: ", maxU)
    for bestSet in maxSets:
        logging.info("%s corresponding prob: %s", bestSet, inputData[list(bestSet)])
    if len(maxSets) == len(findAllCombinations(n1,n2, k)):
        optimumType = Optimum.ANY
    elif not secondBestUpdated: # if secondBest is never updated, it means the first set is the best or one of the best
        optimumType = Optimum.TRUE
    else:
        abstand = maxU - secondBestU
        if abstand > SIGNIFICANCE_LEVEL:
            optimumType = Optimum.TRUE
        else:
            optimumType = Optimum.PSEUDO
    logging.info("is there an optimal?: %s", optimumType)

    return maxSets, maxU, secondBestU, optimumType

#----------------------------------End Main Methods------------------------------------------------

#---------------------------------- Run simulations -----------------------------------------------
def runSimulationTestFullCoverage(simulation_num_per_nk):
    m = 1

    for n in range(5, 9):

        for n1 in range(1, n): # there must be at least one item of each class.
            n2 = n - n1

            for k in range(2, min(n1,n2)+1): # k must >1, otherwise doesn't make much sense (covers one class anyway)


                any_instances = 0  # how many of the ${simulation_num} instances are those who are indifferent to probeset?
                true_instances = 0  # how many of ... are those which we are interested in: exists a real optimum!
                pseudo_instances = 0  # how many of ... are those, who have a max-probeset but rather shaky...
                counter = 0

                while true_instances < simulation_num_per_nk:
                    [p1, p2] = sorted(np.random.choice(999, 2, False)/1000) # no repeating values
                    maxSets, maxU, secondBestU, optimumType = computeUforAllCombinations_Exact1_case(p1, p2, n1, n2, 1, k)

                    if optimumType == Optimum.ANY:
                        any_instances += 1
                    elif optimumType == Optimum.TRUE: # This is what we are interested in
                        true_instances += 1
                        optimalSet = np.array(list(maxSets)[0])
                        testedClass1 = len(sum(np.where(optimalSet<n1)))
                        testedClass2 = len(sum(np.where(optimalSet>=n1)))
                        # logging.critical("n1=%s, n2=%s, test1=%s, test2=%s", n1, n2, testedClass1, testedClass2 )
                        inputData = generateInputVector(p1, p2,n1,n2)
                        optimalProbeSet = inputData[optimalSet]
                        if (testedClass1>0 and testedClass1<n1 and testedClass2>0 and testedClass2!=n2) or (testedClass2>0 and testedClass2<n2 and testedClass1>0 and testedClass1!=n1):
                            logging.critical("hypothesis not true! input=%s, optimal set=%s, n1 = %s, tested = %s, "
                                             "n2 = %s, tested = %s",inputData,optimalProbeSet, n1, testedClass1, n2, testedClass2)


                    else:  # pseudo, ignore
                        pseudo_instances += 1
                    counter += 1
                # print("n={} n1={}, n2={}, k={}, true={}, any={}, pseudo={}".format(n,n1,n2,k,
                #                                                                    true_instances, any_instances, pseudo_instances))


#-------------------------End Simulaitons---------------------------------


#---------------------------------------------------------------------------------
# Lets start with a simple example
# 1. exactly 1 Eins scenario
# 2. the simplest case: d=2, i.e.,only two classes available, p1 and p2.

logging.basicConfig(level=logging.CRITICAL)

# Hypothesis: InputData=[a, a, b, b, b], k=2 --> then either [a, a] or [b, b] and never [a, b]
# p1 = 0.017
# p2 = 0.95
# n1 = 1
# n2 = 4


p1 = 0.1
p2 = 0.9
n1 = 2
n2 = 3

k = 3

# computeUforAllCombinations_Exact1_case(p1, p2, n1, n2, 1, k)
#---------------------End simple example demonstration-----------------------------------------


#-------------------- verify my hypothesis of "full coverage of best item"--------------------

simulation_num_per_nk = 1000
runSimulationTestFullCoverage(simulation_num_per_nk)


