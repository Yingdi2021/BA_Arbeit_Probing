import numpy as np
import itertools
import logging
from optimum import Optimum

#################### Helper-functions #########################
# a frequently used operation
def multiplyPand1MinusP(inputData, setP, set1MinusP):
    result = 1
    for i in setP:
        result *= inputData[i]
    for j in set1MinusP:
        result *= (1 - inputData[j])
    return result

# return all subsets (having a given size)
# of a given Set, as a list.
def findsubsets(set, subset_size):
    return list(itertools.combinations(set, subset_size))

# given a n-vector of probabilities p1, p2,...pn corresponding the prob that event 1, event 2, .. event n happens
# and a constant m <= n
# return the prob that in total m events happen
def calculateProbCertainNumberOfEventsHappen(ps, m):
    n = len(ps)
    assert m <= n
    pss = np.subtract(1, ps)
    result = 0
    for setThatHappens in findsubsets(set(range(n)), m):
        setThatDoesNotHappen = set(range(n)) - set(setThatHappens)
        temp = 1
        for i in setThatHappens:
            temp *= ps[i]
        for j in setThatDoesNotHappen:
            temp *= pss[j]
        result += temp
    return result

# given a n-vector of probabilities p1, p2,...pn corresponding the prob that event 1, event 2, .. event n happens
# return the prob that in total an even number of events happen
def calculateProbEvenNumberOfEventsHappen(ps):
    n = len(ps)
    result = 0
    for num in np.arange(0, n+1, 2):
        result += calculateProbCertainNumberOfEventsHappen(ps, num)
        logging.debug("----p(have %s)=%s", num, calculateProbCertainNumberOfEventsHappen(ps, num))
    return result

################################################################

# calculates the utility (probability of making the right decision)
# given input data, l(threshold), k(probe-set size) and S(the probe-set)
# for the normal case, ie. acceptance criteria is: number of 1s >= l.
def myUtilityForThresholdCases(inputData, l, k, S):

    n = len(inputData)
    N = set(range(n))
    R = N - S

    utility = 0
    for d in range(k + 1):
        logging.debug("Calculating probability of having excatly %s Eins in the probe-set",d)
        subsets_for_this_d = findsubsets(S, d)
        logging.debug("there are in total %s subsets: %s for d=%s", len(subsets_for_this_d), subsets_for_this_d, d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            #probability that this subset happens. For example:
            # {} means no Eins. {0, 1} means that the first two skills are Eins.
            p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
            logging.debug("subset: %s, R=%s, p=%s",set(subset),remaining_nulls, p_subset)
            ps += p_subset
        logging.debug("probability, that there are exactly %s Eins in probe-set is: %s", d,ps)

        logging.debug("---------------\nCalculating C (P that there are enough Eins in R) for d= %s", d)
        if d >= l:
            logging.debug("there are already enough Eins in probe-set. Therefore C=1.")
            utility += ps
        else:
            c = 0
            for m in range(l-d, n-k+1):
                subsets_for_this_m = findsubsets(R, m)
                logging.debug("there are %s subsets for m=%s", len(subsets_for_this_m), m)
                for subset in subsets_for_this_m:
                    remaining_nulls = R - set(subset)
                    #probability that this subset happens:
                    p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
                    c += p_subset
            logging.debug("probability, that at least %s Eins in Rest-Set is:%s", l - d, c)
            logging.debug("choose the more likely! \nWhen there are %s Eins in probe-set: ",d)
            if c>= 0.5:
                logging.debug("it's more likely (p=%s) that this is a good candidate",c)
                logging.debug("--> probability, that d=%s AND we make the right decision is %s",d,ps*c)
                utility += ps*c
            else:
                logging.debug("it's more likely (p=%s ) that this is a bad candidate ",(1-c))
                logging.debug("--> probability, that d=%s AND we make the right decision is %s",d, ps*(1-c))
                utility += ps*(1-c)

    logging.debug("-------------\nResult:")
    logging.debug("utiliiy=%s when we select the probe-set: %s", utility, S)
    return round(utility,8)

################################################################

# same function as above, just without loggings
def myUtilityForThresholdCases_silent(inputData, l, k, S):

    n = len(inputData)
    N = set(range(n))
    R = N - S

    utility = 0
    for d in range(k + 1):
        subsets_for_this_d = findsubsets(S, d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            #probability that this subset happens. For example:
            # {} means no Eins. {0, 1} means that the first two skills are Eins.
            p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
            ps += p_subset

        if d >= l:
            utility += ps
        else:
            c = 0
            for m in range(l-d, n-k+1):
                subsets_for_this_m = findsubsets(R, m)
                for subset in subsets_for_this_m:
                    remaining_nulls = R - set(subset)
                    #probability that this subset happens:
                    p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
                    c += p_subset
            if c>= 0.5:
                utility += ps*c
            else:
                utility += ps*(1-c)

    return round(utility,8)

# calculates the utility (probability of making the right decision)
# given input data, m (how many 1s EXACTLY), k(probe-set size) and S(the probe-set)
# for the exactX case, ie. acceptance criteria is: number of 1s == m
def myUtilityForExactXCases(inputData, m, k, S):

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
            logging.debug("*********************\nCalculating probability of having excatly %s Eins in the probe-set",d)
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
    logging.debug("utiliiy=%s when we select the probe-set: %s", utility, S)
    return round(utility,8)


# calculates the utility (probability of making the right decision)
# given input data, x, y (x OR y 1s exactly), k(probe-set size) and S(the probe-set)
# for the X or Y case, ie. acceptance criteria is: number of 1s == x || y
def myUtilityForXorYcases(inputData, x, y, k, S):

    if x == y:
        return myUtilityForExactXCases(inputData, x, k, S)

    # make sure that x, y are in ascending order.
    if x > y:
        x,y = y,x

    n = len(inputData)
    N = set(range(n))
    R = N - S

    utility = 0
    for d in range(k + 1):
        logging.debug("*********************\nCalculating probability of having excatly %s Eins in the probe-set", d)
        subsets_for_this_d = findsubsets(S, d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
            logging.debug("subset: %s, R=%s, p=%s", set(subset), remaining_nulls, p_subset)
            ps += p_subset
        logging.debug("probability, that there are exactly %s Eins in probe-set is: %s",  d, ps)

        r1 = x - d
        r2 = y - d
        logging.debug("---------------\nCalculating C (Prob that there are excatly %s or %s 1s in R) for d=%s", r1, r2, d)

        c = 0
        if r1 <= n - k and r1 >= 0:
            subsets_for_this_r = findsubsets(R, r1)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset),remaining_nulls)
                c += p_subset
        if r2 <= n - k and r2 >= 0:
            subsets_for_this_r = findsubsets(R, r2)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset),remaining_nulls)
                c += p_subset
        logging.debug("probability, that exactly %s or %s Eins in Rest-Set is: %s", r1,  r2, c)
        logging.debug("choose the more likely! \nWhen there are %s Eins in probe-set: ", d)
        if c >= 0.5:
            logging.debug("it's more likely (p= %s) that this is a good candidate", c)
            logging.debug("--> probability, that d= %s AND we make the right decision is %s", d, ps * c)
            utility += ps * c
        else:
            logging.debug("it's more likely (p= %s) that this is a bad candidate", (1 - c))
            logging.debug("--> probability, that d=%s AND we make the right decision is %s", d, ps * (1 - c))
            utility += ps * (1 - c)

    logging.debug("-------------\nResult:")
    logging.debug("utiliiy=%s when we select the probe-set: %s", utility, S)
    return round(utility,8)

# same function as above, but without loggings
def myUtilityForXorYcases_silent(inputData, x, y, k, S):

    if x == y:
        return myUtilityForExactXCases(inputData, x, k, S)

    # make sure that x, y are in ascending order.
    if x > y:
        x,y = y,x

    n = len(inputData)
    N = set(range(n))
    R = N - S

    utility = 0
    for d in range(k + 1):
        subsets_for_this_d = findsubsets(S, d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
            ps += p_subset

        r1 = x - d
        r2 = y - d

        c = 0
        if r1 <= n - k and r1 >= 0:
            subsets_for_this_r = findsubsets(R, r1)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset),remaining_nulls)
                c += p_subset
        if r2 <= n - k and r2 >= 0:
            subsets_for_this_r = findsubsets(R, r2)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset),remaining_nulls)
                c += p_subset
        if c >= 0.5:
            utility += ps * c
        else:
            utility += ps * (1 - c)

    return round(utility,8)

# only for comparison purpose.
def myUtilityForXorYcasesNew(inputData, x, y, k, S):

    if x == y:
        return myUtilityForExactXCases(inputData, x, k, S)

    # make sure that x, y are in ascending order.
    if x > y:
        x,y = y,x

    n = len(inputData)
    N = set(range(n))
    R = N - S

    other_possibility = 1
    utility = 0
    for d in (0, k):
        logging.debug("*********************\nCalculating probability of having excatly %s Eins in the probe-set", d)
        subsets_for_this_d = findsubsets(S, d)
        ps = 0
        for subset in subsets_for_this_d:
            remaining_nulls = S - set(subset)
            p_subset = multiplyPand1MinusP(inputData, set(subset), remaining_nulls)
            logging.debug("subset: %s, R=%s, p=%s", set(subset), remaining_nulls, p_subset)
            ps += p_subset
        logging.debug("probability, that there are exactly %s Eins in probe-set is: %s",  d, ps)
        other_possibility = other_possibility - ps

        r1 = x - d
        r2 = y - d
        logging.debug("---------------\nCalculating C (Prob that there are excatly %s or %s 1s in R) for d=%s", r1, r2, d)

        c = 0
        if r1 == 0 or r1 == (n-k):
            subsets_for_this_r = findsubsets(R, r1)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset),remaining_nulls)
                c += p_subset
        if r2 == 0 or r2 == (n-k):
            subsets_for_this_r = findsubsets(R, r2)
            for subset in subsets_for_this_r:
                remaining_nulls = R - set(subset)
                p_subset = multiplyPand1MinusP(inputData, set(subset),remaining_nulls)
                c += p_subset
        logging.debug("probability, that exactly %s or %s Eins in Rest-Set is: %s", r1,  r2, c)
        logging.debug("choose the more likely! \nWhen there are %s Eins in probe-set: ", d)
        if c >= 0.5:
            logging.debug("it's more likely (p= %s) that this is a good candidate", c)
            logging.debug("--> probability, that d= %s AND we make the right decision is %s", d, ps * c)
            utility += ps * c
        else:
            logging.debug("it's more likely (p= %s) that this is a bad candidate", (1 - c))
            logging.debug("--> probability, that d=%s AND we make the right decision is %s", d, ps * (1 - c))
            utility += ps * (1 - c)

    utility += other_possibility*1
    logging.debug("if not 0 or not k, then it's 100% bad candidate. p=%s", other_possibility)

    logging.debug("-------------\nResult:")
    logging.debug("utiliiy=%s when we select the probe-set: %s", utility, S)
    return round(utility,8)

# calculates the utility (probability of making the right decision)
# given input data and S (the probe-set)
# for the XOR case, ie. acceptance criteria is: number of 1s is even.
def myUtilityForXORcases(inputData, S):
    n = len(inputData)
    N = set(range(n))
    R = N - S
    restData = inputData[list(R)]
    utility = 0

    # # 1. in case there are even number of 1s in probeset
    # p_probeEven = calculateProbEvenNumberOfEventsHappen(probeData)
    # p_restEven = calculateProbEvenNumberOfEventsHappen(restData)
    # utility += p_probeEven * max(p_restEven, 1-p_restEven)
    # # 2. in case there are odd number of 1s in probeset:
    # p_probeOdd = 1-p_probeEven
    # p_restOdd = 1-p_restEven
    # utility += p_probeOdd * max(p_restOdd, 1-p_restOdd)
    p_restEven = calculateProbEvenNumberOfEventsHappen(restData)
    utility += max(p_restEven, 1-p_restEven)
    logging.debug("p_restEven=%s, p_restOdd=%s", round(p_restEven,3), round((1-p_restEven),3))
    return utility

# given an inputData (a vector of n probabilities/the groundset), parameters l, k
# calculate utility for all possible probe-sets (of size k)
# returns the optimal probe-set(s) and the corresponding utility score.
# set the last parameter (logOn) to true if you want a detailed output of what happened.
def computeUforAllPossibleS_threshold_case(inputData, l, k, s):
    n = len(inputData)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    secondBestUpdated = False
    for probe_set in findsubsets(set(range(n)), k):
        logging.debug("*****************************************************************")
        logging.debug("S=%s", probe_set)
        counter += 1
        u = myUtilityForThresholdCases(inputData, l, k, set(probe_set))
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
    if len(maxSets) == len(findsubsets(set(range(n)), k)):
        signif = Optimum.ANY
    elif not secondBestUpdated: # if secondBest is never updated, it means the first set is the best or one of the best
        signif = Optimum.TRUE
    else:
        abstand = maxU - secondBestU
        if abstand > s:
            signif = Optimum.TRUE
        else:
            signif = Optimum.PSEUDO
    logging.info("secondBestU: %s, diff=%s, is there an optimal?: %s", secondBestU, maxU - secondBestU, signif)
    return maxSets, maxU, secondBestU, signif

# same function as above, but for the exactX case. Duplicated Code, yes. But for the sake of computing speed,
# I don't want to introduce yet another if condition (which will be repeatedly assessed)
def computeUforAllPossibleS_ExactX_case(inputData, m, k, s):
    n = len(inputData)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    secondBestUpdated = False
    for probe_set in findsubsets(set(range(n)), k):
        logging.debug("*****************************************************************")
        logging.debug("possible probeset %s: S=%s", counter, probe_set)
        counter += 1
        u = myUtilityForExactXCases(inputData, m, k, set(probe_set))
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
        logging.info("when probe-set=%s, u=%s", set(probe_set), u)

    logging.info("*****************************************************************")
    logging.info("Utility is maximum (%s) when probeset is (one of) the following: ", maxU)
    for bestSet in maxSets:
        logging.info("%s corresponding prob: %s", bestSet, inputData[list(bestSet)])
    if len(maxSets) == len(findsubsets(set(range(n)), k)):
        signif = Optimum.ANY
    elif not secondBestUpdated: # if secondBest is never updated, it means the first set is the best or one of the best
        signif = Optimum.TRUE
    else:
        abstand = maxU - secondBestU
        if abstand > s:
            signif = Optimum.TRUE
        else:
            signif = Optimum.PSEUDO
    logging.info("secondBestU: %s, diff=%s, is there an optimal?: %s", secondBestU, maxU - secondBestU, signif)

    return maxSets, maxU, secondBestU, signif

# same function as above, but for the X or Y case. Duplicated Code, yes. But for the sake of computing speed,
# I don't want to introduce yet another if condition (which will be repeatedly assessed)
def computeUforAllPossibleS_XorY_case(inputData, x, y, k, s):
    n = len(inputData)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    secondBestUpdated = False
    for probe_set in findsubsets(set(range(n)), k):
        counter += 1
        logging.debug("*****************************************************************")
        logging.debug("possible probeset %s: S=%s", counter, probe_set)
        u = myUtilityForXorYcases(inputData, x, y, k, set(probe_set))
        # u = myUtilityForXorYcasesNew(inputData, x, y, k, set(probe_set))
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
        logging.info("when probe-set=%s, u=%s", set(probe_set), u)

    logging.info("*****************************************************************")
    logging.info("Utility is maximum (%s) when probeset is (one of) the following: ", maxU)
    for bestSet in maxSets:
        logging.info("%s corresponding prob: %s", bestSet, inputData[list(bestSet)])
    if len(maxSets) == len(findsubsets(set(range(n)), k)):
        signif = Optimum.ANY
    elif not secondBestUpdated: # if secondBest is never updated, it means the first set is the best or one of the best
        signif = Optimum.TRUE
    else:
        abstand = maxU - secondBestU
        if abstand > s:
            signif = Optimum.TRUE
        else:
            signif = Optimum.PSEUDO
    logging.info("secondBestU: %s, diff=%s, is there an optimal?: %s", secondBestU, maxU - secondBestU, signif)

    return maxSets, maxU, secondBestU, signif

# same function as above, but for the XOR case. Duplicated Code, yes. But for the sake of computing speed,
# I don't want to introduce yet another if condition (which will be repeatedly assessed)
def computeUforAllPossibleS_XOR_case(inputData, k, s):
    n = len(inputData)
    maxU = 0
    secondBestU = 0
    maxSets = set()
    counter = 0
    secondBestUpdated = False
    for probe_set in findsubsets(set(range(n)), k):
        counter += 1
        logging.debug("*****************************************************************")
        logging.debug("possible probeset %s: S=%s", counter, probe_set)
        u = myUtilityForXORcases(inputData, set(probe_set))
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
        logging.info("when probe-set=%s, u=%s", set(probe_set), u)

    logging.info("*****************************************************************")
    logging.info("Utility is maximum (%s) when probeset is (one of) the following: ", maxU)
    for bestSet in maxSets:
        logging.info("%s corresponding prob: %s", bestSet, inputData[list(bestSet)])
    if len(maxSets) == len(findsubsets(set(range(n)), k)):
        signif = Optimum.ANY
    elif not secondBestUpdated: # if secondBest is never updated, it means the first set is the best or one of the best
        signif = Optimum.TRUE
    else:
        abstand = maxU - secondBestU
        if abstand > s:
            signif = Optimum.TRUE
        else:
            signif = Optimum.PSEUDO
    logging.info("secondBestU: %s, diff=%s, is there an optimal?: %s", secondBestU, maxU - secondBestU, signif)

    return maxSets, maxU, secondBestU, signif

############################# Example #################################

# configure the level of logging here: DEBUG (detailed output), INFO (limited output), ERROR(no output)
logging.basicConfig(level=logging.DEBUG)

####### threshold case ########
# inputData = np.array( [0.081, 0.745, 0.954, 0.954])
# l = 3
# k = 2
# sifnificance_level = pow(10, -8)
# maxSets, maxU, secondBestU, signif= computeUforAllPossibleS_threshold_case(inputData, l, k, sifnificance_level)

####### exactX case ########
inputData = np.array( [0.1, 0.2, 0.4, 0.8, 0.9])
m = 5
k = 5
significance_level = pow(10, -8)
computeUforAllPossibleS_ExactX_case(inputData, m, k, significance_level)

####### XorY case ########
# inputData = np.array([0.1, 0.2, 0.4, 0.8, 0.9])
# x = 0
# y = len(inputData)
# k = 3
# significance_level = pow(10, -8)
# computeUforAllPossibleS_XorY_case(inputData, x, y, k, significance_level)

####### XOR case ########
# inputData = np.array([0.1, 0.2, 0.4, 0.8, 0.9])
# k = 5
# significance_level = pow(10, -8)
# computeUforAllPossibleS_XOR_case(inputData, k, significance_level)
