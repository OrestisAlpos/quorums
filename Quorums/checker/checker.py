from functools import reduce
from itertools import chain, combinations
import sortedcontainers
from Quorums.setcover.setcover import set_cover_fixed_param_algorithm, set_cover_fixed_param_asym_algorithm
import copy


def checkQ3(universe, failProneSystem): #universe is a set. failProneSystem is a list of sets
    (threeSetsExist, solutionSets) = set_cover_fixed_param_algorithm(set(universe), failProneSystem, 3) 
    return (not threeSetsExist, solutionSets)

def checkQ3brute(universe, failProneSystem): #universe is a set. failProneSystem is a list of sets
    threeSetUnion = threeUnion(failProneSystem)
    for f in threeSetUnion:
        if f == universe:
            print(f)
    return not any(f == universe for f in threeSetUnion)
 
def checkB3withSetCover(universe, asymmetricFailProneSystemOriginal, optionalKey = {}):
    asymmetricFailProneSystem = copy.copy(asymmetricFailProneSystemOriginal)

    if isinstance(universe,dict):
        keys = list(universe.values())
    else: 
        keys = list(universe)
    
    # to inverse dict : inv = {v: k for k, v in d.items()}
    if len(keys) == 0:
        return True
    
    for i in keys:
        if optionalKey != {}:
            keyLength = optionalKey
        else:
            keyLength = len(keys)
        firstsystem = asymmetricFailProneSystem[i]
        for j in range(i, keyLength):
            key = keys[j]
            chosensystem = asymmetricFailProneSystem[key]
            twoIntersection = twoIntersectionDiffSets(firstsystem, chosensystem) # n * m
            (checksB3, solutionSets) = set_cover_fixed_param_asym_algorithm(keys[:], firstsystem, chosensystem, twoIntersection) # 3*(n^2m^2)
            if not checksB3:
                # print(solutionSets)
                return False
    return True

""" 
check every fail prone system combination where every two sets are unified and tested against the universe. 
if there are missing processes in the union, search in the remaining sets of both systems for the processes subset.
if it is included in sets of both systems, return true, else false
"""
def checkB3(universe, asymmetricFailProneSystemOriginal):
    asymmetricFailProneSystem = copy.copy(asymmetricFailProneSystemOriginal)

    if isinstance(universe,dict):
        keys = list(universe.values())
    else: 
        keys = list(universe)
        
    # to inverse dict : inv = {v: k for k, v in d.items()}
    if len(keys) == 0:
        return True
    
    for i in keys:
        firstsystem = asymmetricFailProneSystem[i]
        for j in range(i, len(keys)):
            key = keys[j]
            chosensystem = asymmetricFailProneSystem[key]
            twoSetUnion = twoUnionDiffSets(list(firstsystem), list(chosensystem)) # n * m
            for f in twoSetUnion: # n * m
                if isinstance(universe,dict):
                    missingProcesses = set(universe.values()).difference(f)
                else: 
                    missingProcesses = universe.difference(f)
                if(includesMissingProcesses(missingProcesses, list(firstsystem), list(chosensystem))): # n + m
                    #print('Found combination that is equal to the universe for systems ' + str(key) + ' and ' + str(j) + '. Sad!')
                    return False
    return True

def checkB3brute(universe, asymmetricFailProneSystem, i=1):
    if i >= len(asymmetricFailProneSystem):
        #print('No combination found. Great!')
        return True
    firstsystem = asymmetricFailProneSystem[i]
    firstsetPowerset = getPowerSetsOfFailProneSystem(firstsystem)
    for j in range(i + 1, len(asymmetricFailProneSystem) + 1):
        chosensystem = asymmetricFailProneSystem[j]
        chosensystemPowerset = getPowerSetsOfFailProneSystem(chosensystem)
        intersection = getIntersectionOfPowersets(firstsetPowerset, chosensystemPowerset)
        threeSetUnion = threeUnionDiffSets(list(firstsystem), list(chosensystem), list(intersection))
        for f in threeSetUnion:
            if f == universe:
                #print('Found combination that is equal to the universe for systems ' + str(i) + ' and ' + str(j) + '. Sad!')
                return False
    checkB3brute(universe, asymmetricFailProneSystem, i+1)
    return True

def getGuild(universe, failProneSystems, actualFailedSet): #failProneSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    # First, make a pass of the universe to find the correct processes
    correct = universe.difference(actualFailedSet)
    # Second, make a pass of the universe and the failProneSystem of each process to find the correct and wise processes.
    correctWise = list(filter(lambda p: failProneSystemContaisActualFailedSet(failProneSystems[str(p)], actualFailedSet), correct))
    # Third, we have the set of correct and wise procs. Keep only those that have a quorum in this set.
    # Maybe you can find a better algorithm for this than taking the Quorums of every proc and checking if at least one is in the set of correct and wise
    # Maybe you could use the threshold definition, first check top layer, there might be an early stop there, etc...

    # TODO: Find the guild
    # IDEA: Define Naive processes recursively (closure):
    # pk is i-Naive if every Q in Qk contains at least one (i-1)-Naive, Where 0-Naive are the failed processes
    # Then, the correct processes will be the Universe minus all the i-Naive. In this set of correct processes one has to search for a guild      
    return correctWise

def failProneSystemContaisActualFailedSet(failProneSystem, actualFailedSet): # failProneSystem is frozenset of frozensets 
    for failProneSet in failProneSystem:
        if failProneSet.issuperset(actualFailedSet):
            return True
    return False

def threeUnion(setSystem): # returns all sets derived as the union of any three sets from the parameter list of sets
    for i in range(0, 3 - len(setSystem)): # make it work with less than 3 elements
        setSystem.append(frozenset())
    count = len(setSystem)
    res = list()
    for i in range(count):
        for j in range(i + 1, count):
            twoSetUnion = setSystem[i].union(setSystem[j])
            for k in range(j+1, count):
                res.append(twoSetUnion.union(setSystem[k]))
    return res

def threeUnionDiffSets(system1, system2, system3):
    res = list()
    for i in system1:
        for j in system2:
            twoSetUnion = i.union(j)
            for k in system3:
                res.append(twoSetUnion.union(k))
    return res

def twoUnionDiffSets(system1, system2):
    res = list()
    for i in system1:
        for j in system2:
            res.append(i.union(j))
    return res

def twoIntersectionDiffSets(system1, system2):
    res = list()
    for i in system1:
        for j in system2:
            intersection = i.intersection(j)
            #if intersection not in res and len(intersection) != 0:
            res.append(intersection)
            # resWithoutEntry = [x for x in res if x != intersection]
            # res[:]
            # res.remove(intersection)
            """for entry in resWithoutEntry:
                if entry.issubset(intersection):
                    res.remove(entry)"""
    # finalRes = list(filter(lambda f: not any(set(f) < set(g) for g in res), res))
    return res

def includesMissingProcesses(missingProcesses, system1, system2):
    for i in system1:
        if(missingProcesses.issubset(i)):
            for j in system2:
                if(missingProcesses.issubset(j)):
                    return True
            return False # since in all of system2 the missingprocesses couldnt be found
    return False

def unionIntersectionDiffSets(system1, system2):
    resIntersection = list()
    resUnion = list()
    for i in system1:
        # [i.intersection(j) for j in system2 if i.intersection(j) not in res]
        for j in system2:
            union = i.union(j)
            if union not in resUnion:
                resUnion.append(union)
            intersection = i.intersection(j)
            if intersection not in resIntersection:
                resIntersection.append(intersection)
    return (resUnion, resIntersection)

def constructStellarExample():
    aQS = {'select':2, 'out-of':['A1', 'A2', 'A3']}
    bQS = {'select':2, 'out-of':['B1', 'B2', 'B3']}
    kQS = {'select':2, 'out-of':['K1', 'K2', 'K3']}
    cQS = {'select':2, 'out-of':['C1', 'C2']}
    dQS = {'select':2, 'out-of':['D1', 'D2']}
    jQS = {'select':1, 'out-of':['J1']}
    eQS = {'select':1, 'out-of':['E1']}
    fQS = {'select':2, 'out-of':['F1', 'F2', 'F3']}
    gQS = {'select':1, 'out-of':['G1']}
    hQS = {'select':1, 'out-of':['H1']}
    iQS = {'select':1, 'out-of':['I1']}
    llQS = {'select':3, 'out-of':[fQS, gQS, hQS, iQS]}
    mlQS = {'select':4, 'out-of':[cQS, dQS, jQS, eQS, llQS]}
    hlQS = {'select': 3, 'out-of':[aQS, bQS, kQS, mlQS]}
    return hlQS

def constructStellarExample_Orgs():
    aQS = {'select':1, 'out-of':['A']}
    bQS = {'select':1, 'out-of':['B']}
    kQS = {'select':1, 'out-of':['K']}
    cQS = {'select':1, 'out-of':['C']}
    dQS = {'select':1, 'out-of':['D']}
    jQS = {'select':1, 'out-of':['J']}
    eQS = {'select':1, 'out-of':['E']}
    fQS = {'select':1, 'out-of':['F']}
    gQS = {'select':1, 'out-of':['G']}
    hQS = {'select':1, 'out-of':['H']}
    iQS = {'select':1, 'out-of':['I']}
    llQS = {'select':3, 'out-of':[fQS, gQS, hQS, iQS]}
    mlQS = {'select':4, 'out-of':[cQS, dQS, jQS, eQS, llQS]}
    hlQS = {'select': 3, 'out-of':[aQS, bQS, kQS, mlQS]}
    return hlQS

def getMinMaxQuorumSizes(quorumSet):
    min = 10000
    max = 0
    for i in quorumSet:
        if len(i) > max:
            max = len(i)
        if len(i) < min:
            min = len(i)
    return (min, max)

def getMinQuorums(quorumSet):
    (min, _) = getMinMaxQuorumSizes(quorumSet)
    for i in quorumSet:
        if len(i) == min:
            print(i)

def getMaxQuorums(quorumSet):
    (_, max) = getMinMaxQuorumSizes(quorumSet)
    for i in quorumSet:
        if len(i) == max:
            print(i)

"helper methods to get powersets"

def getPowerSetsOfFailProneSystem(failProneSystem): #failProneSystem is a list of sets
    allPowerSets = []
    for failProneSet in failProneSystem:
        ps = powerset(failProneSet)
        for singleSet in ps:
            allPowerSets.append(singleSet)

    # print(set(allPowerSets))
    return set(allPowerSets)

def powerset(iterable):
    s = list(iterable)
    return map(frozenset, chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def getIntersectionOfPowersets(powerset1: frozenset, powerset2: frozenset):
    return powerset1.intersection(powerset2)



# def checkQ3(universe, failProneSystem): #universe is a set. failProneSystem is a list of sets
#     (threeSetsExist, solutionSets) = set_cover_fixed_param_algorithm(set(universe), failProneSystem, 3) 
#     return (not threeSetsExist, solutionSets)

# def checkQ3brute(universe, failProneSystem): #universe is a set. failProneSystem is a list of sets
#     threeSetUnion = threeUnion(failProneSystem)
#     for f in threeSetUnion:
#         if f == universe:
#             print(f)
#     return not any(f == universe for f in threeSetUnion)
 
# def threeUnion(setSystem): # returns all sets derived as the union of any three sets from the parameter list of sets
#     for i in range(0, 3 - len(setSystem)): # make it work with less than 3 elements
#         setSystem.append(frozenset())
#     count = len(setSystem)
#     res = list()
#     for i in range(count):
#         for j in range(i + 1, count):
#             twoSetUnion = setSystem[i].union(setSystem[j])
#             for k in range(j+1, count):
#                 res.append(twoSetUnion.union(setSystem[k]))
#     return res

# def constructStellarExample():
#     aQS = {'select':2, 'out-of':['A1', 'A2', 'A3']}
#     bQS = {'select':2, 'out-of':['B1', 'B2', 'B3']}
#     kQS = {'select':2, 'out-of':['K1', 'K2', 'K3']}
#     cQS = {'select':2, 'out-of':['C1', 'C2']}
#     dQS = {'select':2, 'out-of':['D1', 'D2']}
#     jQS = {'select':1, 'out-of':['J1']}
#     eQS = {'select':1, 'out-of':['E1']}
#     fQS = {'select':2, 'out-of':['F1', 'F2', 'F3']}
#     gQS = {'select':1, 'out-of':['G1']}
#     hQS = {'select':1, 'out-of':['H1']}
#     iQS = {'select':1, 'out-of':['I1']}
#     llQS = {'select':3, 'out-of':[fQS, gQS, hQS, iQS]}
#     mlQS = {'select':4, 'out-of':[cQS, dQS, jQS, eQS, llQS]}
#     hlQS = {'select': 3, 'out-of':[aQS, bQS, kQS, mlQS]}
#     return hlQS

# def constructStellarExample_Orgs():
#     aQS = {'select':1, 'out-of':['A']}
#     bQS = {'select':1, 'out-of':['B']}
#     kQS = {'select':1, 'out-of':['K']}
#     cQS = {'select':1, 'out-of':['C']}
#     dQS = {'select':1, 'out-of':['D']}
#     jQS = {'select':1, 'out-of':['J']}
#     eQS = {'select':1, 'out-of':['E']}
#     fQS = {'select':1, 'out-of':['F']}
#     gQS = {'select':1, 'out-of':['G']}
#     hQS = {'select':1, 'out-of':['H']}
#     iQS = {'select':1, 'out-of':['I']}
#     llQS = {'select':3, 'out-of':[fQS, gQS, hQS, iQS]}
#     mlQS = {'select':4, 'out-of':[cQS, dQS, jQS, eQS, llQS]}
#     hlQS = {'select': 3, 'out-of':[aQS, bQS, kQS, mlQS]}
#     return hlQS

# def getMinMaxQuorumSizes(quorumSet):
#     min = 10000
#     max = 0
#     for i in quorumSet:
#         if len(i) > max:
#             max = len(i)
#         if len(i) < min:
#             min = len(i)
#     return (min, max)

# def getMinQuorums(quorumSet):
#     (min, _) = getMinMaxQuorumSizes(quorumSet)
#     for i in quorumSet:
#         if len(i) == min:
#             print(i)

# def getMaxQuorums(quorumSet):
#     (_, max) = getMinMaxQuorumSizes(quorumSet)
#     for i in quorumSet:
#         if len(i) == max:
#             print(i)