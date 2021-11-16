# Let's test the weighted variant of the problem:
# suppose that the skills (items) are not equally important, but some of them are more valued than others.
# How does this weighting affect the results (for example, the consecutive conjecture)?

# of course, this only makes sense in the "threshold scenario".

import logging
import itertools
import numpy as np
from optimum import Optimum
SIGNIFICANCE_LEVEL = pow(10, -8)

# given a unprobed rest_set (a vector of probs and weights) and a threshold value l, calculate the probability that
# this restset has a weighted number of Eins > l
def calculProbOverWeightedThreshold(probs, weights, l):
    p_ok = 0 # probability that weighted number of Eins is over the treshold
    n = len(probs)
    for possibility in list(itertools.product({0,1}, repeat=n)):
        if np.dot(weights, possibility)>=l: # if this happens, is good,but what is the possibility that this happens?
            p = 1
            for i in range(n):
                p *= (((possibility[i] == 1)*probs[i])+(possibility[i]==0)*(1-probs[i]))
            p_ok += p
    return p_ok

# calculates the utility (probability of making the right decision)
# given input data, l(threshold), and S(the probe-set)
# for the normal case, ie. acceptance criteria is: number of 1s >= l.
def myUtilityForWeightedThresholdCases(inputData, weights, l, S):

    n = len(inputData)
    N = set(range(n))
    R = N - S
    probe_set_probs = inputData[list(S)]
    rest_set_probs = inputData[list(R)]
    probe_set_weights = weights[list(S)]
    rest_set_weights = weights[list(R)]

    n_probe = len(S)
    n_rest = n - n_probe

    utility = 0

    # loop through all possibilities in the probeset and calculate for each possiblity the weighted number of Eins.
    for possibility in list(itertools.product({0,1}, repeat=n_probe)):
        p_this_possibility = 1
        for i in range(n_probe):
            p_this_possibility *= (((possibility[i] == 1)*probe_set_probs[i])+(possibility[i]==0)*(1-probe_set_probs[i]))
        weighted_sum = np.dot(probe_set_weights, possibility)
        logging.debug("if it is %s (prob=%s) in the probe-set, then weighted_sum = %s, we need %s in rest_set ",
                      possibility, p_this_possibility, weighted_sum, l-weighted_sum)
        if l-weighted_sum > 0:
            p_rest_enough = calculProbOverWeightedThreshold(rest_set_probs, rest_set_weights, l-weighted_sum)
        else:
            p_rest_enough = 1
        if p_rest_enough>=0.5:
            u = p_this_possibility * p_rest_enough
            logging.debug("prob that rest_set has enough Eins is %s, good candidate, accept. u=%s", p_rest_enough, u)
        else:
            u = p_this_possibility * (1-p_rest_enough)
            logging.debug("prob that rest_set has enough Eins is %s, bad candidate, reject. u=%s", p_rest_enough, u)
        utility += u

    logging.debug("-------------\nResult:")
    logging.debug("utiliiy=%s when we select the probe-set: %s", utility, S)
    return round(utility,8)


def computeUforAllPossibleS_WeightedThreshold_case(inputData, weights, l, k):
    n = len(inputData)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    secondBestUpdated = False
    for probe_set in list(itertools.combinations(set(range(n)), k)):
        logging.debug("*****************************************************************")
        logging.debug("S=%s", probe_set)
        counter += 1
        u = myUtilityForWeightedThresholdCases(inputData, weights, l, set(probe_set))
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
        logging.info("when probe-set=%s ,u=%s",set(probe_set), u)

    logging.info("*****************************************************************")
    logging.info("Utility is maximum (%s) when probeset is (one of) the following:", maxU)
    for bestSet in maxSets:
        logging.info("%s corresponding prob: %s", bestSet, inputData[list(bestSet)])
    allSubsets = list(itertools.combinations(set(range(n)), k))
    if len(maxSets) == len(allSubsets):
        optimumType = Optimum.ANY
    elif not secondBestUpdated: # if secondBest is never updated, it means the first set is the best or one of the best
        optimumType = Optimum.TRUE
    else:
        abstand = maxU - secondBestU
        if abstand > SIGNIFICANCE_LEVEL:
            optimumType = Optimum.TRUE
        else:
            optimumType = Optimum.PSEUDO
    logging.info("secondBestU: %s, diff=%s, is there an optimal?: %s", secondBestU, maxU - secondBestU, optimumType)
    return maxSets, maxU, secondBestU, optimumType

#################
logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

inputData = np.array([ 0.3,  0.4,  0.6,  0.8,  0.9])
weights = np.array([ 1.1,  0.3,  2.6,  0.1,  0.9])
weighted_inputdata = weights * inputData
print(weighted_inputdata)
threshold = 4
k = 2

computeUforAllPossibleS_WeightedThreshold_case(inputData, weights,threshold,k)