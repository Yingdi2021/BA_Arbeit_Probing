import logging

import numpy as np
import itertools

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.CRITICAL)
ALLOWED_ERROR = pow(10, -5)

def calculateConditionalProbability(inputData, partial_realization):
    if not partial_realization.all(): # if there's a 0, then we are certain of our decision: 100% correct.
        return 1
    else: # otherwise we campare the probability that all unprobed bits are 1s with its counter-probability and
        # choose the greater one
        unprobed_bits = inputData[np.isnan(partial_realization)]
        p_all_unprobed_all_ones = np.prod(unprobed_bits)
        return max(p_all_unprobed_all_ones, 1-p_all_unprobed_all_ones)

def calculateExpectedMarginBenefit(inputData, partial_realization, e):
    utility_without_e = calculateConditionalProbability(inputData, partial_realization)
    logging.info("utility of this partial realization(%s)=%s", partial_realization, np.round(utility_without_e, 5)) # rounding only in logging
    new_realizatiton = partial_realization.copy()
    new_realizatiton[e] = 1
    utility_e_being_1 = calculateConditionalProbability(inputData, new_realizatiton)
    probability_e_being_1 = inputData[e]
    # utility_e_being_0 = 1
    expected_utility = utility_e_being_1 * probability_e_being_1 + 1 * (1-probability_e_being_1)
    logging.info("expected utility after adding e (bit %s) = %s", e, np.round(expected_utility, 5)) # rounding only in
    # logging
    return expected_utility-utility_without_e

def testIfViolatesSubmodularity(inputData, smallerSet, biggerSet, e):
    n = len(inputData)
    phi_template = np.empty(n)
    phi_template[:] = np.NAN
    phi_1 = phi_template.copy()
    phi_1[list(smallerSet)] = 1
    restSet = set(biggerSet) - set(smallerSet)
    m = len(restSet)
    # consider all possibilities of the restSet!!!!!!
    possbilities = list(itertools.product([0, 1], repeat=m))
    for p in possbilities:
        phi_2 = phi_1.copy()
        phi_2[list(restSet)] = p
        expectedMarginBenefit_e_for_phi_1 = calculateExpectedMarginBenefit(inputData, phi_1, e)
        if expectedMarginBenefit_e_for_phi_1 < -ALLOWED_ERROR:
            logging.critical("expected margin benefit < 0!!!!!!!!!")
        logging.info("expected Margin Benefit of e for phi_1 (%s)=%s", phi_1, round(expectedMarginBenefit_e_for_phi_1,3))
        expectedMarginBenefit_e_for_phi_2 = calculateExpectedMarginBenefit(inputData, phi_2, e)
        logging.info("expected Margin Benefit of e for phi_2 (%s)=%s", phi_2, round(expectedMarginBenefit_e_for_phi_2,3))
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
    for size_bigger_set in range(1, n):
        for biggerSet in findsubsets(set(range(n)), size_bigger_set):
            # print("big set=", biggerSet)
            restSet = set(range(n))-set(biggerSet)
            # print("rest set=", restSet)
            for size_smaller_set in range(0,size_bigger_set):
                for smallerSet in findsubsets(biggerSet, size_smaller_set):
                    # print("small set=", smallerSet)
                    for e in restSet:
                        logging.info("test for combination: phi1=%s, phi2=%s, e=%s", smallerSet, biggerSet, e)
                        if testIfViolatesSubmodularity(inputData, smallerSet, biggerSet, e):
                            logging.info("violation!")
                            return True # violation detected
    return False # no violation detected

########################################################
# test individual distribution
inputData = np.array([0.79, 0.8, 0.81, 0.82])
violation = testDistribution(inputData)
print(violation)

########################################################
# ## systematically test all possible distributions
# n = 3
# possible_bits = np.round(np.linspace(0.1, 0.9, 9),1)
# # possible_bits = np.round(np.linspace(0.1, 1, 10),1)
# combinations = list(itertools.product(possible_bits, repeat=n))
# combinations_without_repetition = set()
# for combi in combinations:
#     sorted_combi = tuple(sorted(combi))
#     if sorted_combi not in combinations_without_repetition:
#         combinations_without_repetition.add(sorted_combi)
#
# combinations_without_repetition_sorted = sorted(combinations_without_repetition)
#
# # for combi in combinations_without_repetition_sorted:
# #     print(combi)
#
# for combi in combinations_without_repetition_sorted:
#     inputData = np.array(combi)
#     violation = testDistribution(inputData)
#     if not violation:
#         logging.critical("distribution %s satisfies adaptive submodularity", inputData)

######################################
## gefundenen

# n=4
# CRITICAL:root:distribution [0.7 0.8 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.7 0.9 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.8 0.8 0.8 0.8] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.8 0.8 0.8 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.8 0.8 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.8 0.9 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.9 0.9 0.9 0.9] satisfies adaptive submodularity

# n = 5
# CRITICAL:root:distribution [0.7 0.9 0.9 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.8 0.8 0.9 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.8 0.9 0.9 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.9 0.9 0.9 0.9 0.9] satisfies adaptive submodularity

# n=6
# CRITICAL:root:distribution [0.8 0.9 0.9 0.9 0.9 0.9] satisfies adaptive submodularity
# CRITICAL:root:distribution [0.9 0.9 0.9 0.9 0.9 0.9] satisfies adaptive submodularity

########################################################
######### Test Hypothesis ###########

# test random distributions
# for n in range(4, 5):
#     for simulation_num in range(500000):
#         x = sorted(np.random.randint(1, 1000, n)) # To change
#         inputData = np.divide(x, 1000)
#         inputData = np.round(inputData, 3) # round input data
#         violation = testDistribution(inputData)
#         if violation:
#             if np.prod(inputData[:]) >= 0.5:
#             # if np.prod(inputData[:-1]) > 0.5:
#                 logging.critical("Violation, Hypothesis not true!")
#                 logging.critical("inputdata=%s, product=%s", inputData, np.prod(inputData[:]))
#                 # logging.critical("inputdata=%s, product=%s", inputData, np.prod(inputData[:-1]))
#         else: # no violation
#             if np.prod(inputData[:]) < 0.5:
#             # if np.prod(inputData[:-1]) < 0.5:
#                 logging.critical("Kein Violation, Hypothesis not true!")
#                 logging.critical("inputdata=%s, product=%s", inputData, np.prod(inputData[:]))
#                 # logging.critical("inputdata=%s, product=%s", inputData, np.prod(inputData[:-1]))

