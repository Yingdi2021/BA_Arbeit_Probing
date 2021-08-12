import logging

import numpy as np
import itertools

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.CRITICAL)
ALLOWED_ERROR = pow(10, -5)

def calculateProbExactlyOneEin(probabilities):
    counter_prob = 1 - probabilities
    result = 0
    for i in range(len(probabilities)):
        pp = counter_prob.copy()
        pp[i] = probabilities[i]
        result += np.prod(pp)
    return result

def calculateConditionalProbability(inputData, referenceVector, partial_realization):
    if noConsistentRealisationCanBeGreaterThanReferenceVector(partial_realization, referenceVector):
        # if this partial realisation is already "smaller" than ref, then we are certain of our decision 100%
        return 1
    else:
        # if all probed-bits are fine then compare the probability that all unprobed bits >= ref with its
        # counter-probability (i.e. all the bits where ref==1, we have also 1)
        all_unprobed_bits_that_must_be_1s = np.where((referenceVector==1) & (np.isnan(partial_realization)))
        prob_satisfy =  np.prod(inputData[all_unprobed_bits_that_must_be_1s])
        return max(prob_satisfy, 1-prob_satisfy)

def calculateExpectedMarginBenefit(inputData, referenceVector, partial_realization, e):
    utility_without_e = calculateConditionalProbability(inputData, referenceVector, partial_realization)
    logging.info("utility of this partial realization=%s", np.round(utility_without_e, 5)) # rounding only in logging

    realisation_e_being_0 = partial_realization.copy()
    realisation_e_being_0[e] = 0
    utility_e_being_0 = calculateConditionalProbability(inputData, referenceVector, realisation_e_being_0)
    probability_e_being_0 = 1 - inputData[e]

    realisation_e_being_1 = partial_realization.copy()
    realisation_e_being_1[e] = 1
    utility_e_being_1 = calculateConditionalProbability(inputData, referenceVector, realisation_e_being_1)
    probability_e_being_1 = inputData[e]

    expected_utility = utility_e_being_0 * probability_e_being_0 + utility_e_being_1 * probability_e_being_1

    logging.info("expected utility after adding e (bit %s) = %s",e, np.round(expected_utility, 5))
    return expected_utility-utility_without_e

def noConsistentRealisationCanBeGreaterThanReferenceVector(phi, referenceVector):
    for i in range(len(phi)):
        if phi[i] < referenceVector[i]:
            return True
    return False

def testIfViolatesSubmodularity(inputData, referenceVector, smallerSet, biggerSet, e):
    n = len(inputData)
    phi_template = np.empty(n)
    phi_template[:] = np.NAN

    small_possibilities = list(itertools.product([0, 1], repeat=len(smallerSet)))
    for small_possbility in small_possibilities:
        if not noConsistentRealisationCanBeGreaterThanReferenceVector(small_possbility, referenceVector):
            phi_1 = phi_template.copy()
            phi_1[list(smallerSet)] = small_possbility
            differenceSet = set(biggerSet) - set(smallerSet)
            # consider all possibilities of the differenceSet!!!!!!
            possbilities = list(itertools.product([0, 1], repeat=len(differenceSet)))
            for possibility in possbilities:
                phi_2 = phi_1.copy()
                phi_2[list(differenceSet)] = possibility
                logging.info("phi_small=%s, phi_big=%s", phi_1, phi_2)
                expectedMarginBenefit_e_for_phi_1 = calculateExpectedMarginBenefit(inputData, referenceVector, phi_1, e)
                if expectedMarginBenefit_e_for_phi_1 < -ALLOWED_ERROR:
                    logging.critical("warning: expected margin benefit < 0!!!!!!!!!")
                logging.info("expected Margin Benefit of e for phi_small=%s", round(expectedMarginBenefit_e_for_phi_1,3))
                expectedMarginBenefit_e_for_phi_2 = calculateExpectedMarginBenefit(inputData, referenceVector, phi_2, e)
                logging.info("expected Margin Benefit of e for phi_big=%s", round(expectedMarginBenefit_e_for_phi_2,3))
                logging.info("-----")
                if expectedMarginBenefit_e_for_phi_1-expectedMarginBenefit_e_for_phi_2 < -ALLOWED_ERROR:
                    logging.error("--> at least one violation of adaptive submodularity found! phi1=%s, phi2=%s, e=%s", smallerSet,
                                  biggerSet, e)
                    return True # violation detected
    # if all possibilities are fine (no violation)
    logging.info("no violation for this combination of phi_small & phi_big")
    logging.info("-------------------------------------------------------------")
    return False

def findsubsets(set, subset_size):
    return list(itertools.combinations(set, subset_size))

def testDistribution(inputData, referenceVector):
    n = len(inputData)
    for size_of_bigger_set in range(1, n):
        for biggerSet in findsubsets(set(range(n)), size_of_bigger_set):
            restSet = set(range(n))-set(biggerSet)
            for size_smaller_set in range(size_of_bigger_set):
                for smallerSet in findsubsets(biggerSet, size_smaller_set):
                    for e in restSet:
                        logging.info("test for combination: inputdata=%s, ref_vector=%s, phi1=%s, phi2=%s, e=%s", inputData,
                                     referenceVector, smallerSet, biggerSet, e)
                        if testIfViolatesSubmodularity(inputData, referenceVector, smallerSet, biggerSet, e):
                            logging.info("violation!")
                            return True # violation detected
    return False # no violation detected

########################################################
####test individual distribution
# inputData = np.array([0.2, 0.4, 0.5, 0.8])
# referenceVector = np.array([1, 0, 0, 0])
# violation = testDistribution(inputData,referenceVector)
# print(violation)

# ########################################################
# # ## systematically test all possible distributions
referenceVector = np.array([0,0,0,0])
n = 4
possible_bits = np.round(np.linspace(0.1, 0.9, 9),1)
combinations = list(itertools.product(possible_bits, repeat=n))

# for combi in combinations:
#     print(combi)


for combi in combinations:
    inputData = np.array(combi)
    violation = testDistribution(inputData, referenceVector)
    if not violation:
        logging.critical("distribution %s satisfies adaptive submodularity", inputData)

# # ########################################################
# # ######### Test Hypothesis that no distribution is adaptive submodular  ###########
# # ####  test random distributions

SIMULATION_NR = 100
n = 4
combinations = list(itertools.product([0,1], repeat=n))
for combi in combinations:
    referenceVector = np.array(combi)
    bits_that_are_1 = np.where(referenceVector==1)
    logging.critical("testing for reference vector=%s...", referenceVector)
    hypothesis = True
    if sum(combi) > 1 and sum(combi)<n:
        for n in range(n, n+1):
            for simulation_num in range(SIMULATION_NR):
                x = sorted(np.random.randint(1, 1000, n))
                inputData = np.divide(x, 1000)
                inputData = np.round(inputData, 3) # round input data

                violation = testDistribution(inputData, referenceVector)

                if np.prod(inputData[bits_that_are_1])>=0.5:
                    # then we don't expect any violation of adaptive submodularity
                    if violation:
                        logging.critical("no violation expected, but occured. Hypothesis not true! distribution=%s", inputData)
                        hypothesis = False
                else:
                    # then we expect a violation
                    if not violation:
                        logging.critical("violation expected but did not occur. Hypoothesis not true. Distribution=%s", inputData)
                        hypothesis = False
        logging.critical("----------hypothesis=%s", hypothesis)
    elif sum(combi) == 1:
        for n in range(n, n+1):
            for simulation_num in range(SIMULATION_NR):
                x = sorted(np.random.randint(1, 1000, n))
                inputData = np.divide(x, 1000)
                inputData = np.round(inputData, 3) # round input data

                violation = testDistribution(inputData, referenceVector)

                if violation:
                    logging.critical("no violation expected, but occured. Hypothesis not true! distribution=%s", inputData)
                    hypothesis = False
        logging.critical("----------hypothesis=%s", hypothesis)
    elif sum(combi) == n: # d.h. all 1s.
        for n in range(n, n+1):
            for simulation_num in range(SIMULATION_NR):
                x = sorted(np.random.randint(1, 1000, n))
                inputData = np.divide(x, 1000)
                inputData = np.round(inputData, 3) # round input data

                violation = testDistribution(inputData, referenceVector)

                if np.prod(inputData)>=0.5:
                    # expect no violation
                    if violation:
                        logging.critical("no violation expected, but occured. Hypothesis not true! distribution=%s", inputData)
                        hypothesis = False
                else:
                    # expect violation
                    if not violation:
                        logging.critical("violation expected, but did not occur. Hypothesis not true! distribution=%s", inputData)
                        hypothesis = False
        logging.critical("----------hypothesis=%s", hypothesis)
    else: # at least one 1
        for n in range(n, n+1):
            for simulation_num in range(SIMULATION_NR):
                x = sorted(np.random.randint(1, 1000, n))
                inputData = np.divide(x, 1000)
                inputData = np.round(inputData, 3) # round input data

                violation = testDistribution(inputData, referenceVector)

                if np.prod(inputData)<=0.5:
                    # expect no violation
                    if violation:
                        logging.critical("no violation expected, but occured. Hypothesis not true! distribution=%s", inputData)
                        hypothesis = False
                else:
                    # expect violation
                    if not violation:
                        logging.critical("violation expected, but did not occur. Hypothesis not true! distribution=%s", inputData)
                        hypothesis = False
        logging.critical("----------hypothesis=%s", hypothesis)

############

