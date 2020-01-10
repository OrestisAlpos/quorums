


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
