from functools import reduce
from setcover import set_cover_fixed_param_algorithm


def checkQ3(universe, failProneSystem): #universe is a set. failProneSystem is a list of sets
    (threeSetsExist, solutionSets) = set_cover_fixed_param_algorithm(set(universe), failProneSystem, 3) 
    return (not threeSetsExist, solutionSets)

def checkQ3brute(universe, failProneSystem): #universe is a set. failProneSystem is a list of sets
    threeSetUnion = threeUnion(failProneSystem)
    for f in threeSetUnion:
        if f == universe:
            print(f)
    return not any(f == universe for f in threeSetUnion)
 




def getGuild(universe, failProneSystems, actualFailedSet): #failProneSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    (kFaultyProcesses, allFaultyProcessess) = getAllRecursiveFaultyProcesses(universe, failProneSystems, actualFailedSet)
    return (kFaultyProcesses, allFaultyProcessess)
    #return universe.difference(allFaultyProcessess)

def getAllRecursiveFaultyProcesses(universe, failProneSystems, actualFailedSet):
    kFaultyProcesses = list() #Each faultyProcesses[k] is the set of all k-faulty processes
    allFaultyProcessess = frozenset()
    newFaultyProcesses = actualFailedSet
    while len(newFaultyProcesses) > 0:
        kFaultyProcesses.append(newFaultyProcesses)
        allFaultyProcessess = allFaultyProcessess.union(newFaultyProcesses)
        newFaultyProcesses = getRecursiveFaultyProcesses(universe, failProneSystems, allFaultyProcessess)
    return (kFaultyProcesses, allFaultyProcessess)

def getRecursiveFaultyProcesses(universe, failProneSystems, previousFaultyProcesses):
    correct = universe.difference(previousFaultyProcesses)
    return frozenset(filter(lambda p: not failProneSystemContainsSet(failProneSystems[str(p)], previousFaultyProcesses), correct))

def failProneSystemContainsSet(failProneSystem, setToFind): # failProneSystem is frozenset of frozensets 
    for failProneSet in failProneSystem:
        if failProneSet.issuperset(setToFind):
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