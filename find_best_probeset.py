import numpy as np
import itertools
import sys
import os

#################### Helper-functions #########################
# a frequently used operation
def multiplyPand1MinusP(input, setP, set1MinusP):
    result = 1
    for i in setP:
        result *= input[i]
    for j in set1MinusP:
        result *= (1 - input[j])
    return result

# return all subsets (having a given size)
# of a given Set, as a list.
def findsubsets(set, subset_size):
    return list(itertools.combinations(set, subset_size))
################################################################

# calculates the utility (probability of making the right decision)
# given input data, l(threshold), k(probe-set size) and S(the probe-set)
# for the normal case, ie. acceptance criteria is: number of 1s >= l.
def myUtilityForThresholdCases(input, l, k, S):

    n = len(input)
    N = set(range(n))
    R = N - S

    utility = 0
    for d in range(k + 1):
        print("Calculating probability of having excatly",d,"Eins in the probe-set")
        subsets_for_this_d = findsubsets(S, d)
        print("there are in total", len(subsets_for_this_d), "subsets: ",
              subsets_for_this_d, "for d=", d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            #probability that this subset happens. For example:
            # {} means no Eins. {0, 1} means that the first two skills are Eins.
            p_subset = multiplyPand1MinusP(input, set(subset), remaining_nulls)
            print("subset:",set(subset), "R=", remaining_nulls, "p=",p_subset)
            ps += p_subset
        print("probability, that there are exactly", d, "Eins in probe-set is:",ps)

        print("---------------")
        print("Calculating C (P that there are enough Eins in R) for d=", d)
        if d >= l:
            print("there are already enough Eins in probe-set. Therefore C=1.")
            utility += ps
        else:
            c = 0
            for m in range(l-d, n-k+1):
                subsets_for_this_m = findsubsets(R, m)
                print("there are", len(subsets_for_this_m), "subsets for m=", m)
                for subset in subsets_for_this_m:
                    remaining_nulls = R - set(subset)
                    #probability that this subset happens:
                    p_subset = multiplyPand1MinusP(input, set(subset), remaining_nulls)
                    # print("subset=", subset, ",remain=", remaining_nulls, ",p=", p_subset)
                    c += p_subset
            print("probability, that at least", l - d,"Eins in Rest-Set is:", c)
            print("choose the more likely! \nWhen there are",d,"Eins in probe-set: ")
            if c>= 0.5:
                print("it's more likely (p= ",c, ") that this is a good candidate")
                print("--> probability, that d=",d,"AND we make the right decision is",ps*c)
                utility += ps*c
            else:
                print("it's more likely (p= ",(1-c), ") that this is a bad candidate")
                print("--> probability, that d=",d,"AND we make the right decision is",ps*(1-c))
                utility += ps*(1-c)

    print("-------------\nResult:")
    print("utiliiy=", utility, "when we select the probe-set:", S)
    return utility

# calculates the utility (probability of making the right decision)
# given input data, m (how many 1s EXACTLY), k(probe-set size) and S(the probe-set)
# for the exactX case, ie. acceptance criteria is: number of 1s == m
def myUtilityForExactXCases(input, m, k, S):

    n = len(input)
    N = set(range(n))
    R = N - S

    utility = 0

    # if there are no more than m 1s in the probe-set:
    for d in range(m + 1):
        print("*********************")
        print("Calculating probability of having excatly",d,"Eins in the probe-set")
        subsets_for_this_d = findsubsets(S, d)
        print("there are in total", len(subsets_for_this_d), "subsets: ", subsets_for_this_d, "for d=", d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            p_subset = multiplyPand1MinusP(input, set(subset), remaining_nulls)
            print("subset:",set(subset), "R=", remaining_nulls, "p=",p_subset)
            ps += p_subset
        print("probability, that there are exactly", d, "Eins in probe-set is:",ps)

        r = m - d
        print("---------------")
        print("Calculating C (Prob that there are excatly", r, "1s in R) for d=", d)

        c = 0
        if r <= n-k:
            subsets_for_this_m = findsubsets(R, r)
            for subset in subsets_for_this_m:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(input, set(subset), remaining_nulls)
                c += p_subset
        print("probability, that exactly", r, "Eins in Rest-Set is:", c)
        print("choose the more likely! \nWhen there are",d,"Eins in probe-set: ")
        if c>= 0.5:
            print("it's more likely (p= ",c, ") that this is a good candidate")
            print("--> probability, that d=",d,"AND we make the right decision is",ps*c)
            utility += ps*c
        else:
            print("it's more likely (p= ",(1-c), ") that this is a bad candidate")
            print("--> probability, that d=",d,"AND we make the right decision is",ps*(1-c))
            utility += ps*(1-c)

    # if there are more than m 1s in probe-set, we always make the right decision: reject
    if k > m:
        for d in range(m+1,k+1):
            print("*********************")
            print("Calculating probability of having excatly",d,"Eins in the probe-set")
            subsets_for_this_d = findsubsets(S, d)
            print("there are in total", len(subsets_for_this_d), "subsets: ", subsets_for_this_d, "for d=", d)
            ps = 0
            for subset in subsets_for_this_d:
                remaining_nulls = S - set(subset)
                p_subset = multiplyPand1MinusP(input, set(subset), remaining_nulls)
                print("subset:",set(subset), "R=", remaining_nulls, "p=",p_subset)
                ps += p_subset
            print("probability, that there are exactly", d, "Eins in probe-set AND we make the right decision is:", ps)
            utility += ps

    print("-------------\nResult:")
    print("utiliiy=", utility, "when we select the probe-set:", S)
    return utility


# calculates the utility (probability of making the right decision)
# given input data, x, y (x OR y 1s exactly), k(probe-set size) and S(the probe-set)
# for the X or Y case, ie. acceptance criteria is: number of 1s == x || y
def myUtilityForXorYcases(input, x, y, k, S):

    if x == y:
        return myUtilityForExactXCases(input, x, k, S)

    # make sure that x, y are in ascending order.
    if x > y:
        x,y = y,x

    n = len(input)
    N = set(range(n))
    R = N - S

    utility = 0
    for d in range(y + 1):
        print("*********************")
        print("Calculating probability of having excatly", d, "Eins in the probe-set")
        subsets_for_this_d = findsubsets(S, d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            p_subset = multiplyPand1MinusP(input, set(subset), remaining_nulls)
            print("subset:", set(subset), "R=", remaining_nulls, "p=",p_subset)
            ps += p_subset
        print("probability, that there are exactly", d, "Eins in probe-set is:", ps)

        r1 = x - d
        r2 = y - d
        print("---------------")
        print("Calculating C (Prob that there are excatly", r1, "or", r2, "1s in R) for d=", d)

        c = 0
        if r1 <= n - k and r1 >= 0:
            subsets_for_this_r = findsubsets(R, r1)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(input, set(subset),remaining_nulls)
                c += p_subset
        if r2 <= n - k and r2 >= 0:
            subsets_for_this_r = findsubsets(R, r2)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(input, set(subset),remaining_nulls)
                c += p_subset
        print("probability, that exactly", r1, "or", r2, "Eins in Rest-Set is:", c)
        print("choose the more likely! \nWhen there are", d, "Eins in probe-set: ")
        if c >= 0.5:
            print("it's more likely (p= ", c,") that this is a good candidate")
            print("--> probability, that d=", d, "AND we make the right decision is", ps * c)
            utility += ps * c
        else:
            print("it's more likely (p= ", (1 - c), ") that this is a bad candidate")
            print("--> probability, that d=", d, "AND we make the right decision is", ps * (1 - c))
            utility += ps * (1 - c)

    print("-------------\nResult:")
    print("utiliiy=", utility, "when we select the probe-set:", S)
    return utility

# given an input (a vector of n probabilities/the groundset), parameters l, k
# calculate utility for all possible probe-sets (of size k)
# returns the optimal probe-set(s) and the corresponding utility score.
# set the last parameter (logOn) to true if you want a detailed output of what happened.
def computeUforAllPossibleS_threshold_case(input, l, k, s, loggingLevel):
    n = len(input)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    for probe_set in findsubsets(set(range(n)), k):
        if loggingLevel <= 1:
            sys.stdout = open(os.devnull, 'w')
        print("*****************************************************************")
        print("S=", probe_set)
        counter += 1
        u = myUtilityForThresholdCases(input, l, k, set(probe_set))
        if loggingLevel == 1:
            sys.stdout = sys.__stdout__
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
        print("when probe-set=",set(probe_set),",u=",u)

    print("*****************************************************************")
    print("Utility is maximum (", maxU,") when probeset is (one of) the following: ")
    for bestSet in maxSets:
        print(bestSet, "corresponding prob:", input[list(bestSet)])
    abstand = maxU-secondBestU
    signif = abstand > s
    print("secondBestU:", secondBestU, "diff=", maxU-secondBestU,
          "significant diff?: ", signif)
    if loggingLevel == 0:
        sys.stdout = sys.__stdout__

    return maxSets, maxU, secondBestU, signif

# same function as above, but for the exactX case. Duplicated Code, yes. But for the sake of computing speed,
# I don't want to introduce yet another if condition (which will be repeatedly assessed)
def computeUforAllPossibleS_ExactX_case(input, m, k, s, loggingLevel):
    n = len(input)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    for probe_set in findsubsets(set(range(n)), k):
        if loggingLevel <= 1:
            sys.stdout = open(os.devnull, 'w')
        print("*****************************************************************")
        print("S=", probe_set)
        counter += 1
        u = myUtilityForExactXCases(input, m, k, set(probe_set))
        if loggingLevel == 1:
            sys.stdout = sys.__stdout__
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
        print("when probe-set=",set(probe_set),",u=",u)

    print("*****************************************************************")
    print("Utility is maximum (", maxU,") when probeset is (one of) the following: ")
    for bestSet in maxSets:
        print(bestSet, "corresponding prob:", input[list(bestSet)])
    abstand = maxU-secondBestU
    signif = abstand > s
    print("secondBestU:", secondBestU, "diff=", maxU-secondBestU,
          "significant diff?: ", signif)
    if loggingLevel == 0:
        sys.stdout = sys.__stdout__

    return maxSets, maxU, secondBestU, signif

# same function as above, but for the X or Y case. Duplicated Code, yes. But for the sake of computing speed,
# I don't want to introduce yet another if condition (which will be repeatedly assessed)
def computeUforAllPossibleS_XorY_case(input, x, y, k, s, loggingLevel):
    n = len(input)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    for probe_set in findsubsets(set(range(n)), k):
        if loggingLevel <= 1:
            sys.stdout = open(os.devnull, 'w')
        counter += 1
        print(
            "*****************************************************************")
        print("possible probeset", counter, ": S=", probe_set)
        u = myUtilityForXorYcases(input, x, y, k, set(probe_set))
        if loggingLevel == 1:
            sys.stdout = sys.__stdout__
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
        print("when probe-set=", set(probe_set), ",u=", u)

    print("*****************************************************************")
    print("Utility is maximum (", maxU,
          ") when probeset is (one of) the following: ")
    for bestSet in maxSets:
        print(bestSet, "corresponding prob:", input[list(bestSet)])
    abstand = maxU - secondBestU
    signif = abstand > s
    print("secondBestU:", secondBestU, "diff=", maxU - secondBestU,
          "significant diff?: ", signif)
    if loggingLevel == 0:
        sys.stdout = sys.__stdout__

    return maxSets, maxU, secondBestU, signif

############################# Example #################################

####### threshold case ########
# input = np.array( [0.081, 0.745, 0.954, 0.954])
# l = 3
# k = 2
# loggingLevel = 0 # 0 for no logging at all # 1 for end-result, # 2 for detailed
# sifnificance_level = pow(10, -8)
# maxSets, maxU, secondBestU, signif= computeUforAllPossibleS_threshold_case(input, l, k, sifnificance_level, loggingLevel)

####### exactX case ########
# input = np.array( [0.1, 0.2, 0.5, 0.8])
# m = 3
# k = 2
# loggingLevel = 1 # 0 for no logging at all # 1 for end-result, # 2 for detailed
# significance_level = pow(10, -8)
# computeUforAllPossibleS_ExactX_case(input, m, k, significance_level, loggingLevel)

####### XorY case ########
# input = np.array( [0.1, 0.2, 0.5, 0.8])
# x = 0
# y = 4
# k = 3
# loggingLevel = 1 # 0 for no logging at all # 1 for end-result, # 2 for detailed
# significance_level = pow(10, -8)
# computeUforAllPossibleS_XorY_case(input, x, y, k, significance_level, loggingLevel)
