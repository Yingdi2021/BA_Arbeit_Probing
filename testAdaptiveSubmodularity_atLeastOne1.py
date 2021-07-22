import logging

import numpy as np
import itertools

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.CRITICAL)
ALLOWED_ERROR = pow(10, -5)

def calculateConditionalProbability(inputData, partial_realization):
    if np.any(partial_realization==1): # if there's a 1 in the probed bits, then we are certain of our decision 100%
        return 1
    else: # otherwise we campare the probability that all unprobed bits are 0s with its counter-probability
        unprobed_bits_counter_probabilities = 1 - inputData[np.isnan(partial_realization)]
        p_all_unprobed_all_zeros = np.prod(unprobed_bits_counter_probabilities)
        return max(p_all_unprobed_all_zeros, 1-p_all_unprobed_all_zeros)

def calculateExpectedMarginBenefit(inputData, partial_realization, e):
    utility_without_e = calculateConditionalProbability(inputData, partial_realization)
    logging.info("utility of this partial realization=%s", np.round(utility_without_e, 5)) # rounding only in logging
    new_realizatiton = partial_realization.copy()
    new_realizatiton[e] = 0
    utility_e_being_0 = calculateConditionalProbability(inputData, new_realizatiton)
    probability_e_being_0 = 1 - inputData[e]
    # utility_e_being_1 = 1
    expected_utility = utility_e_being_0 * probability_e_being_0 + 1 * inputData[e]
    logging.info("expected utility after adding e (bit %s) = %s",e, np.round(expected_utility, 5)) # rounding only in
    # logging
    return expected_utility-utility_without_e

def testIfViolatesSubmodularity(inputData, smallerSet, biggerSet, e):
    n = len(inputData)
    phi_template = np.empty(n)
    phi_template[:] = np.NAN
    phi_1 = phi_template.copy()
    phi_1[list(smallerSet)] = 0 # for the smaller phi (smaller set) we do not consider those that have 1s
    differenceSet = set(biggerSet) - set(smallerSet)
    m = len(differenceSet)
    # consider all possibilities of the differenceSet!!!!!!
    possbilities = list(itertools.product([0, 1], repeat=m))
    for p in possbilities:
        phi_2 = phi_1.copy()
        phi_2[list(differenceSet)] = p
        logging.info("phi_small=%s, phi_big=%s", phi_1, phi_2)
        expectedMarginBenefit_e_for_phi_1 = calculateExpectedMarginBenefit(inputData, phi_1, e)
        if expectedMarginBenefit_e_for_phi_1 < -ALLOWED_ERROR:
            logging.critical("expected margin benefit < 0!!!!!!!!!")
        logging.info("expected Margin Benefit of e for phi_small=%s", round(expectedMarginBenefit_e_for_phi_1,3))
        expectedMarginBenefit_e_for_phi_2 = calculateExpectedMarginBenefit(inputData, phi_2, e)
        logging.info("expected Margin Benefit of e for phi_big=%s", round(expectedMarginBenefit_e_for_phi_2,3))
        logging.info("-----")
        if expectedMarginBenefit_e_for_phi_1-expectedMarginBenefit_e_for_phi_2 < -ALLOWED_ERROR:
            logging.error("--> at least one violation of adaptive submodularity found! phi1=%s, phi2=%s, e=%s", smallerSet,
                          biggerSet, e)
            return True # violation detected
    # if all possibilities are fine (no violation)
    logging.info("-------------------------------------------------------------")
    return False

def findsubsets(set, subset_size):
    return list(itertools.combinations(set, subset_size))

def testDistribution(inputData):
    n = len(inputData)
    for size_of_bigger_set in range(2, n):
        for biggerSet in findsubsets(set(range(n)), size_of_bigger_set):
            restSet = set(range(n))-set(biggerSet)
            for size_smaller_set in range(1,size_of_bigger_set):
                for smallerSet in findsubsets(biggerSet, size_smaller_set):
                    for e in restSet:
                        logging.info("test for combination: phi1=%s, phi2=%s, e=%s", smallerSet, biggerSet, e)
                        if testIfViolatesSubmodularity(inputData, smallerSet, biggerSet, e):
                            logging.info("violation!")
                            return True # violation detected
    return False # no violation detected

########################################################
####test individual distribution
inputData = np.array([0.2, 0.2, 0.2, 0.2])
violation = testDistribution(inputData)
print(violation)

########################################################
# ## systematically test all possible distributions
n = 6
possible_bits = np.round(np.linspace(0.1, 0.9, 9),1)
# possible_bits = np.round(np.linspace(0.1, 1, 10),1)
combinations = list(itertools.product(possible_bits, repeat=n))
combinations_without_repetition = set()
for combi in combinations:
    sorted_combi = tuple(sorted(combi))
    if sorted_combi not in combinations_without_repetition:
        combinations_without_repetition.add(sorted_combi)

combinations_without_repetition_sorted = sorted(combinations_without_repetition)

# for combi in combinations_without_repetition_sorted:
#     print(combi)

for combi in combinations_without_repetition_sorted:
    inputData = np.array(combi)
    violation = testDistribution(inputData)
    if not violation:
        logging.critical("distribution %s satisfies adaptive submodularity, counter prob=%s", inputData, 1-inputData)

######################################
## gefundenen

# n=4
# CRITICAL:root:distribution [0.1 0.1 0.1 0.1] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.9]
# CRITICAL:root:distribution [0.1 0.1 0.1 0.2] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.8]
# CRITICAL:root:distribution [0.1 0.1 0.1 0.3] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.7]
# CRITICAL:root:distribution [0.1 0.1 0.2 0.2] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.8 0.8]
# CRITICAL:root:distribution [0.1 0.1 0.2 0.3] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.8 0.7]
# CRITICAL:root:distribution [0.1 0.2 0.2 0.2] satisfies adaptive submodularity, counter prob=[0.9 0.8 0.8 0.8]
# CRITICAL:root:distribution [0.2 0.2 0.2 0.2] satisfies adaptive submodularity, counter prob=[0.8 0.8 0.8 0.8]

# n=5
# CRITICAL:root:distribution [0.1 0.1 0.1 0.1 0.1] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.9 0.9]
# CRITICAL:root:distribution [0.1 0.1 0.1 0.1 0.2] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.9 0.8]
# CRITICAL:root:distribution [0.1 0.1 0.1 0.1 0.3] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.9 0.7]
# CRITICAL:root:distribution [0.1 0.1 0.1 0.2 0.2] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.8 0.8]

# n=6
# CRITICAL:root:distribution [0.1 0.1 0.1 0.1 0.1 0.1] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.9 0.9 0.9]
# CRITICAL:root:distribution [0.1 0.1 0.1 0.1 0.1 0.2] satisfies adaptive submodularity, counter prob=[0.9 0.9 0.9 0.9 0.9 0.8]

########################################################
######### Test Hypothesis ###########

####  test random distributions
for n in range(4, 5):
    for simulation_num in range(1000):
        x = sorted(np.random.randint(1, 1000, n)) # To change
        inputData = np.divide(x, 1000)
        inputData = np.round(inputData, 3) # round input data

        # do we expect a violation for this distribution?
        violation = testDistribution(inputData)
        counter_inputData = sorted(1 - inputData)
        if np.prod(counter_inputData[:-1]) > 0.5:
            logging.info("utility function for this distribution should be adaptive submodular. no violation expected.")
            if violation:
                logging.critical("Violation not expected but occured. Hypothesis not true! %s", inputData)

        if np.prod(counter_inputData[:-1]) < 0.5:
            logging.info("utility function for this distribution should NOT be adaptive submodular. violation expected.")
            if not violation:
                logging.critical("violation expected but did not occur. Hypothesis not true!")

