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

def calculateConditionalProbability(inputData, partial_realization):
    if np.sum(partial_realization==1)>1:
        # if there are  more than one 1 in the probed bits, then we are certain of our decision 100%
        return 1
    elif np.sum(partial_realization==1)==1:
        # if there's already one 1 in the probed bits, then compare the probability that there are no 1s in the
        # unprobedd bits with its counter prob.
        unprobed_bits_counter_probabilities = 1 - inputData[np.isnan(partial_realization)]
        p_all_unprobed_all_zeros = np.prod(unprobed_bits_counter_probabilities)
        return max(p_all_unprobed_all_zeros, 1-p_all_unprobed_all_zeros)
    else:
        # if there's no 1 in the probed bits, then compare the  probability that  there are exactly one 1 in the
        # unprobed bits with its counter prob.
        unprobed_bits_probabilities =  inputData[np.isnan(partial_realization)]
        p_exactly_one_1_in_unprobed = calculateProbExactlyOneEin(unprobed_bits_probabilities)
        return max(p_exactly_one_1_in_unprobed, 1-p_exactly_one_1_in_unprobed)

def calculateExpectedMarginBenefit(inputData, partial_realization, e):
    utility_without_e = calculateConditionalProbability(inputData, partial_realization)
    logging.info("utility of this partial realization=%s", np.round(utility_without_e, 5)) # rounding only in logging

    realisation_e_being_0 = partial_realization.copy()
    realisation_e_being_0[e] = 0
    utility_e_being_0 = calculateConditionalProbability(inputData, realisation_e_being_0)
    probability_e_being_0 = 1 - inputData[e]

    realisation_e_being_1 = partial_realization.copy()
    realisation_e_being_1[e] = 1
    utility_e_being_1 = calculateConditionalProbability(inputData, realisation_e_being_1)
    probability_e_being_1 = inputData[e]

    expected_utility = utility_e_being_0 * probability_e_being_0 + utility_e_being_1 * probability_e_being_1

    logging.info("expected utility after adding e (bit %s) = %s",e, np.round(expected_utility, 5))
    return expected_utility-utility_without_e

def testIfViolatesSubmodularity(inputData, smallerSet, biggerSet, e):
    n = len(inputData)
    phi_template = np.empty(n)
    phi_template[:] = np.NAN

    small_possibilities = list(itertools.product([0, 1], repeat=len(smallerSet)))
    for small_possbility in small_possibilities:
        if sum(small_possbility) <= 1: # for the smaller phi (smaller set) we do not consider those that have more than one 1s
            phi_1 = phi_template.copy()
            phi_1[list(smallerSet)] = small_possbility
            differenceSet = set(biggerSet) - set(smallerSet)
            # consider all possibilities of the differenceSet!!!!!!
            possbilities = list(itertools.product([0, 1], repeat=len(differenceSet)))
            for possibility in possbilities:
                phi_2 = phi_1.copy()
                phi_2[list(differenceSet)] = possibility
                logging.info("phi_small=%s, phi_big=%s", phi_1, phi_2)
                expectedMarginBenefit_e_for_phi_1 = calculateExpectedMarginBenefit(inputData, phi_1, e)
                if expectedMarginBenefit_e_for_phi_1 < -ALLOWED_ERROR:
                    logging.critical("warning: expected margin benefit < 0!!!!!!!!!")
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
                        logging.info("test for combination: inputdata=%s, phi1=%s, phi2=%s, e=%s", inputData, smallerSet, biggerSet, e)
                        if testIfViolatesSubmodularity(inputData, smallerSet, biggerSet, e):
                            logging.info("violation!")
                            return True # violation detected
    return False # no violation detected

########################################################
####test individual distribution
# inputData = np.array([0.9, 0.9, 0.9, 0.9])
# violation = testDistribution(inputData)
# print(violation)

########################################################
# ## systematically test all possible distributions
n = 5
possible_bits = np.round(np.linspace(0.1, 0.9, 9),1)
# possible_bits = np.round(np.linspace(0.1, 1, 10),1)
combinations = list(itertools.product(possible_bits, repeat=n))
combinations_without_repetition = set()
for combi in combinations:
    sorted_combi = tuple(sorted(combi))
    if sorted_combi not in combinations_without_repetition:
        combinations_without_repetition.add(sorted_combi)

# # for combi in combinations_without_repetition_sorted:
# #     print(combi)
#
# for combi in combinations_without_repetition_sorted:
#     inputData = np.array(combi)
#     violation = testDistribution(inputData)
#     if not violation:
#         logging.critical("distribution %s satisfies adaptive submodularity", inputData)
#
# ########################################################
# ######### Test Hypothesis that no distribution is adaptive submodular  ###########
#
# ####  test random distributions
for n in range(4, 5):
    for simulation_num in range(1000):
        x = sorted(np.random.randint(1, 1000, n))
        inputData = np.divide(x, 1000)
        inputData = np.round(inputData, 3) # round input data

        # we don't expect any distribution that is adaptive submodular
        violation = testDistribution(inputData)
        if not violation:
            logging.critical("this distribution %d is adaptive submodular!. Hypothesis not true!", inputData)

