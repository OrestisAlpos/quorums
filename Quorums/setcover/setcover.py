def set_cover_fixed_param_algorithm(elementsToCover, candidateSets, k): #elementsToCover is a set. candidateSets is a list of frozensets
    # See "Fixed parameter Tractability" lecture for this idea. What exactly is the complexity? Sth like r^k * O(n), where r is the 
    # branching factor, i.e. the number of candidate sets in every step. What is this number? I think r = O(n), which is not
    # correct according to the lecture :(  ).
    if len(elementsToCover) == 0:
        return (True, [])
    if k == 0:
        return (False, [])
    # Extension: You can sort the elements by the number of sets they appear in and take first the one with the smallest number.
    
    elementsToCover = sortByOccurences(elementsToCover, candidateSets)
    elementSelected = elementsToCover.pop()
    elementsToCover = set(elementsToCover)
    setsCoveringSelectedElement = list(filter(lambda s: s.intersection(set({elementSelected})) != set(), candidateSets)) # n
    for candidateSet in setsCoveringSelectedElement: # n
        elementsLeft = elementsToCover.difference(candidateSet)
        candidateSetsLeft = candidateSets[:]; candidateSetsLeft.remove(candidateSet)
        (found, solutionSets) = set_cover_fixed_param_algorithm(elementsLeft, candidateSetsLeft, k-1)
        if found == True:
            solutionSets.append(candidateSet)
            return (True, solutionSets)
    return (False, [])

def sortByOccurences(elementsToCover, candidateSets):
    numberOfOccurences = []
    for element in elementsToCover:
        numberOfOccurences.append({"name": element, "number" : 0})
        for candidateSet in candidateSets:
            if element in candidateSet:
                elemInList = next(item for item in numberOfOccurences if item["name"] == element)
                elemInList["number"] += 1
    
    sortedOccurences = sorted(numberOfOccurences, key=takeNumber, reverse=True)
    return [d["name"] for d in sortedOccurences]

def takeNumber(elem):
    return elem["number"]

def set_cover_fixed_param_asym_algorithm(elementsToCover, system1, system2, system3): 
    """ IDEA: Take first element to cover, get all sets in s1 and s2 that include that element and go from there
        ==> take next element that hasn't been covered yet, choose all sets from the respective other system
        ==> in the end check the remaining sets of both systems for the missing processes
    """

    if len(elementsToCover) == 0:
        return (False, [])
    if system1 is None and system2 is None and system3 is None:
        return (True, [])
    
    elementSelected = elementsToCover.pop()
    elementsToCover = set(elementsToCover)
    if system1 is not None:
        setsCoveringSelectedElement = list(filter(lambda s: elementSelected in s, system1)) 
        for candidateSet in setsCoveringSelectedElement: # n
            elementsLeft = elementsToCover.difference(candidateSet)
            # print(elementsLeft)
            (checksB3, solutionSets) = set_cover_fixed_param_asym_algorithm(elementsLeft, None, system2, system3)
            if not checksB3:
                solutionSets.append(candidateSet)
                return (False, solutionSets)

    if system2 is not None:
        setsCoveringSelectedElement = list(filter(lambda s: elementSelected in s, system2)) 
        for candidateSet in setsCoveringSelectedElement: # m
            elementsLeft = elementsToCover.difference(candidateSet)
            # print(elementsLeft)
            (checksB3, solutionSets) = set_cover_fixed_param_asym_algorithm(elementsLeft, system1, None, system3)
            if not checksB3:
                solutionSets.append(candidateSet)
                return (False, solutionSets)

    if system3 is not None:
        setsCoveringSelectedElement = list(filter(lambda s: elementSelected in s, system3)) 
        for candidateSet in setsCoveringSelectedElement: # n*m
            elementsLeft = elementsToCover.difference(candidateSet)
            # print(elementsLeft)
            (checksB3, solutionSets) = set_cover_fixed_param_asym_algorithm(elementsLeft, system1, system2, None)
            if not checksB3:
                solutionSets.append(candidateSet)
                return (False, solutionSets)
    return (True, [])