#### Weights Variant.
# Given a vector of n bits (0 or 1), drawn from a known distribution
# and a vector of n weights, and a threshold,
# find the optimal probe-set(s) (of a given size).

import logging
import numpy as np
import itertools


def findsubsets(set, subset_size):
    return list(itertools.combinations(set, subset_size))


def generateAllPossibleBinary(n):
    return list(itertools.product([0, 1], repeat=n))


def calculateProbOfAnOutcome(ps, outcome):
    result = 1
    n = len(ps)
    for i in range(n):
        result *= (1 - outcome[i]) * (1 - ps[i]) + ps[i] * outcome[i]
    return result


def myUtilityForThresholdCases_weights(input, weights, l, k, S):
    n = len(input)
    N = set(range(n))
    ps_probeset = input[list(S)]
    logging.debug("probabilities in Probeset=%s", ps_probeset)
    ws = weights[list(S)]
    logging.debug("weights for Probeset=%s", ws)
    R = N - S
    ps_restset = input[list(R)]
    logging.debug("probabilities in Rest-set=%s", ps_restset)
    ws_rest = weights[list(R)]
    logging.debug("weights for Rest-set=%s", ws_rest)

    utility = 0
    for i in generateAllPossibleBinary(k):
        possibleOutcome_probeset = np.array(i)
        valueInProbeset = np.inner(possibleOutcome_probeset, ws)
        p = calculateProbOfAnOutcome(ps_probeset, possibleOutcome_probeset)
        logging.debug(
            "####################################################\nif the probe-set turns out to be: %s,-->value in probe-set=%s. Prob=%s",
            possibleOutcome_probeset, valueInProbeset, round(p, 4))
        if valueInProbeset >= l:
            u = p * 1
            utility += u
            logging.debug("-------> threshold(=%s) reached. doesn't matter how it looks like in rest-set. "
                          "\nutility+=%s", l, round(u, 4))
        else:
            missing_value = l - valueInProbeset
            logging.debug("-------> threshold(=%s) not reached. let's look at the rest-set: ", l)
            c = 0  # c is the prob that the rest-set has enough Eins
            for j in generateAllPossibleBinary(n - k):
                possibleOutcome_restset = np.array(j)
                valueInRestset = np.inner(possibleOutcome_restset, ws_rest)
                if valueInRestset >= missing_value:
                    c += calculateProbOfAnOutcome(ps_restset, possibleOutcome_restset)
            if c >= 0.5:
                utility += p * c
                logging.debug("         it's more likely (p=%s) that the value in rest-set is big enough--accept. "
                              "\nu= %s*%s=%s, utility += %s", c, round(p, 4), c, round(p * c, 4), round(p * c, 4))
            else:
                utility += p * (1 - c)
                logging.debug(
                    "         it's more likely (p=%s) that the value in rest-set is not big enough--reject. \n"
                    "u =%s*%s=%s, utility += %s", 1 - c, round(p, 4), 1 - c, round(p * (1 - c), 4),
                    round(p * (1 - c), 4))
    logging.debug("overall, utility = %s", round(utility, 4))
    return utility


def computeUforAllPossibleS_threshold_weights(input, l, k, s):
    n = len(input)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    for probe_set in findsubsets(set(range(n)), k):
        logging.debug("*****************************************************************\nS = %s", probe_set)
        counter += 1
        u = myUtilityForThresholdCases_weights(input, weights, l, k, set(probe_set))
        if counter == 1:
            secondBestU = u
            maxU = u
            maxSets = set()
            maxSets.add(probe_set)
        else:
            if u > maxU:
                secondBestU = maxU
                maxU = u
                maxSets = set()
                maxSets.add(probe_set)
            elif u == maxU:
                maxSets.add(probe_set)
        logging.info("when probe-set=%s ,u=%s", set(probe_set), u)

    logging.info("*****************************************************************")
    logging.info("Utility is maximum (%s) when probeset is (one of) the following:", maxU)
    for bestSet in maxSets:
        logging.info("%s corresponding prob: %s", bestSet, input[list(bestSet)])
    abstand = maxU - secondBestU
    signif = abstand > s
    logging.info("secondBestU: %s, diff=%s, significant diff?: %s", round(secondBestU, 4), round(maxU - secondBestU, 4),
                 signif)

    return maxSets, maxU, secondBestU, signif


############################# Example #################################

logging.basicConfig(level=logging.DEBUG)

input = np.array([0.1, 0.2, 0.3, 0.4])
weights = np.array([1, 2, 3, 4])
l = 3
k = 2
sifnificance_level = pow(10, -8)
computeUforAllPossibleS_threshold_weights(input, l, k, sifnificance_level)
