def set_cover_fixed_param_algorithm(elementsToCover, candidateSets, k): #elementsToCover is a set. candidateSets is a list of frozensets
    # See "Fixed parameter Tractability" lecture for this idea. What exactly is the complexity? Sth like r^k * O(n), where r is the 
    # branching factor, i.e. the number of candidate sets in every step. What is this number? I think r = O(n), which is not
    # correct according to the lecture :(  ).
    if len(elementsToCover) == 0:
        return (True, [])
    if k == 0:
        return (False, [])
    # Extension: You can sort the elements by the number of sets they appear in and take first the one with the smallest number.
    elementSelected = elementsToCover.pop()
    setsCoveringSelectedElement = list(filter(lambda s: s.intersection(set({elementSelected})) != set(), candidateSets))
    for candidateSet in setsCoveringSelectedElement:
        elementsLeft = elementsToCover.difference(candidateSet)
        candidateSetsLeft = candidateSets[:]; candidateSetsLeft.remove(candidateSet)
        (found, solutionSets) = set_cover_fixed_param_algorithm(elementsLeft, candidateSetsLeft, k-1)
        if found == True:
            solutionSets.append(candidateSet)
            return (True, solutionSets)
    return (False, [])