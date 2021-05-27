import logging
import numpy as np
from find_best_probeset import computeUforAllPossibleS_ExactX_case
from find_best_probeset import computeUforAllPossibleS_XorY_case
from optimum import Optimum
import statistics
import pickle

sifnificance_level = pow(10, -8)
simulation_num = 1000


def runAllCombinationsExactOne():
    m = 1

    for n in range(5, 9):

        true_percentage = []
        any_percentage = []
        startingBit_average = []
        startingBit_std = []
        trueOptimalNum_average = []
        trueOptimalNum_std = []

        for k in range(2, n):
            any_instances = 0  # how many of the ${simulation_num} instances are those who are indifferent to probeset?
            true_instances = 0  # how many of ... are those which we are interested in: exists a real optimum!
            pseudo_instances = 0  # how many of ... are those, who have a max-probeset but rather shaky...
            startingBits = []
            true_optimal_nums = []
            while any_instances + true_instances < simulation_num:
                inputData = sorted(np.random.rand(n))
                inputData = np.round(inputData, 3)
                maxSets, maxU, secondBestU, signif = computeUforAllPossibleS_ExactX_case(inputData, m, k,
                                                                                         sifnificance_level)

                if signif == Optimum.ANY:
                    any_instances += 1
                elif signif == Optimum.TRUE:
                    true_instances += 1
                    true_optimal_nums.append(len(maxSets))
                    for maxSet in maxSets:
                        startingBits.append(maxSet[0])
                else:  # pseudo, ignore
                    pseudo_instances += 1
            # look at the result
            # print(true_optimal_nums)
            if true_instances > 0:
                averageStartingBit = round(statistics.mean(startingBits), 4)
                startingBit_average.append(averageStartingBit)
                trueOptimalNum = round(statistics.mean(true_optimal_nums),1)
                trueOptimalNum_average.append(trueOptimalNum)
                if len(startingBits) > 1:
                    starting_bit_std = round(statistics.stdev(startingBits), 3)
                    true_optimal_stdd = round(statistics.stdev(true_optimal_nums),3)
                else:
                    starting_bit_std = float("Nan")
                    true_optimal_stdd = float("Nan")
                startingBit_std.append(starting_bit_std)
                trueOptimalNum_std.append(true_optimal_stdd)
                logging.error("n=%s, k=%s, #true_instances=%s (out of %s), true_optimal_num: average=%s, std=%s, "
                              "average starting bit = %s, std=%s, ", n, k, true_instances, simulation_num,
                              trueOptimalNum, true_optimal_stdd, averageStartingBit, starting_bit_std)
            else:
                logging.error("n=%s, k=%s, #true_instances=%s, all %s instances are ANY.", n, k, true_instances,
                              simulation_num)
                startingBit_average.append(float("Nan"))
                startingBit_std.append(float("Nan"))
            true_percentage.append(true_instances * 100 / simulation_num)
            any_percentage.append(any_instances * 100 / simulation_num)

        print("true_percentage:", true_percentage)
        print("any_percentage:", any_percentage)
        print("startingBit_average:", startingBit_average)
        print("startingBit_std", startingBit_std)

        f = open("exact_one_n=" + str(n) + ".pkl", 'wb')
        pickle.dump([true_percentage, any_percentage, startingBit_average], f)
        f.close()

    # TODO save the data (for later visualisation purpose)
    # number of true optimal: average, std.
    # use dataframe!

def runAllCombinationsNoneOrAll():
    x = 0

    for n in range(5, 9):
        y = n

        true_percentage = []
        any_percentage = []
        startingBit_average = []
        startingBit_std = []
        trueOptimalNum_average = []
        trueOptimalNum_std = []

        for k in range(2, n):
            any_instances = 0 # how many of the ${simulation_num} instances are those who are indifferent to probeset?
            true_instances = 0 # how many of ... are those which we are interested in: exists a real optimum!
            pseudo_instances = 0 # how many of ... are those, who have a max-probeset but rather shaky...
            startingBits = []
            true_optimal_nums = []
            while any_instances+true_instances < simulation_num:
                inputData = sorted(np.random.rand(n))
                inputData = np.round(inputData, 3)
                maxSets, maxU, secondBestU, signif = computeUforAllPossibleS_XorY_case(inputData,x, y, k, sifnificance_level)

                if signif == Optimum.ANY:
                    any_instances += 1
                elif signif == Optimum.TRUE:
                    true_instances += 1
                    true_optimal_nums.append(len(maxSets))
                    for maxSet in maxSets:
                        startingBits.append(maxSet[0])
                else: # pseudo, ignore
                    pseudo_instances += 1
            # look at the result
            # print(true_optimal_nums)
            if true_instances > 0:
                averageStartingBit = round(statistics.mean(startingBits), 4)
                startingBit_average.append(averageStartingBit)
                trueOptimalNum = round(statistics.mean(true_optimal_nums),1)
                trueOptimalNum_average.append(trueOptimalNum)
                if len(startingBits) > 1:
                    starting_bit_std = round(statistics.stdev(startingBits), 3)
                    true_optimal_stdd = round(statistics.stdev(true_optimal_nums),3)
                else:
                    starting_bit_std = float("Nan")
                    true_optimal_stdd = float("Nan")
                startingBit_std.append(starting_bit_std)
                trueOptimalNum_std.append(true_optimal_stdd)
                logging.error("n=%s, k=%s, #true_instances=%s (out of %s), true_optimal_num: average=%s, std=%s, "
                              "average starting bit = %s, std=%s, ", n, k, true_instances, simulation_num,
                              trueOptimalNum, true_optimal_stdd, averageStartingBit, starting_bit_std)
            else:
                logging.error("n=%s, k=%s, #true_instances=%s, all %s instances are ANY.", n, k, true_instances,
                              simulation_num)
                startingBit_average.append(float("Nan"))
                startingBit_std.append(float("Nan"))
            true_percentage.append(true_instances*100/simulation_num)
            any_percentage.append(any_instances*100/simulation_num)

        print("true_percentage:", true_percentage)
        print("any_percentage:", any_percentage)
        print("startingBit_average:", startingBit_average)
        print("startingBit_std", startingBit_std)

        f = open("none_or_all_n="+str(n)+".pkl", 'wb')
        pickle.dump([true_percentage, any_percentage, startingBit_average], f)
        f.close()

runAllCombinationsExactOne()

runAllCombinationsNoneOrAll()

