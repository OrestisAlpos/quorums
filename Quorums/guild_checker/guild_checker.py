import Quorums.checker.checker as checker


def getAllGuilds(universe, failProneSystems):
    guilds = dict()
    for s in checker.powerset(universe):
        g = getGuild(universe, failProneSystems, s)
        if g != set():
            guilds[s] = g
    print(guilds)

def getToleratedSystem(universe, failProneSystems): # When tolerated set is defined as U \ G, where G is a guild. In this case, and assuminc canonical, the whole tolerated set can fail, and its complement will be a guild.
    toleratedSystem = set()
    for b in checker.powerset(universe):
        g = getGuild(universe, failProneSystems, b)
        if g != set():
            toleratedSet = frozenset(universe.difference(g))
            toleratedSystem.add(toleratedSet)
    print(toleratedSystem)

def getGuild(universe, failProneSystems, actualFailedSet): #failProneSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    (kFaultyProcesses, allFaultyProcessess) = getAllRecursiveFaultyProcesses(universe, failProneSystems, actualFailedSet)
    #return (kFaultyProcesses, allFaultyProcessess)
    return universe.difference(allFaultyProcessess)

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
    return frozenset(filter(lambda p: not failProneSystemContainsSet(failProneSystems[p], previousFaultyProcesses), correct))

def failProneSystemContainsSet(failProneSystem, setToFind): # failProneSystem is frozenset of frozensets 
    for failProneSet in failProneSystem:
        if failProneSet.issuperset(setToFind):
            return True
    return False
