import json
import itertools
import functools 

def parseThresholdDescription(confTitle):  #Returns frozenset of frozensets
    jsonString = ""
    with open('config.json', 'r') as conf:
        jsonString = json.loads(conf.read())
    systemDescription = jsonString[confTitle]
    return systemDescription[0][0]

def parseJson(confTitle):  #Returns frozenset of frozensets
    jsonString = ""
    with open('config.json', 'r') as conf:
        jsonString = json.loads(conf.read())
    systemDescription = jsonString[confTitle]
    #systemDescription is a list of lists: each systemDescription[i] describes Fi in F.
    setsParsed = list()
    for description in systemDescription:
        setsParsed.append(parseSetsFromDescription(description))
    return frozenset().union(*setsParsed)    

def parseJsonAsym(confTitle):  #Returns a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    jsonString = ""
    with open('config.json', 'r') as conf:
        jsonString = json.loads(conf.read())
    systemDescription = jsonString[confTitle]
    #systemDescription is a list of lists: each systemDescription[i] describes Fi, whic is the FailProneSystem of process i
    setsParsed = list()
    for description in systemDescription:
        setsParsed.append(parseSetsFromDescription(description))
    res = {}
    for i in range(len(setsParsed)):
        res[str(i + 1)] = setsParsed[i]
    return res  

def parseSetsFromDescription(description):
    if (len(description) == 1) & (type(description[0]) == dict):
        return parseSetsFromThresholdDescription(description[0])
    else:
        size = len(description)
        return parseSetsFromThresholdDescription({'select':size, 'out-of':description})

def parseSetsFromThresholdDescription(thresholdDict): #returns a frozenset of frozensets satisfying a choose-k-out-of-tot threshold
    k = thresholdDict['select']
    elements = thresholdDict['out-of']
    elementsParsed = [] #Contains frozensets of frozensets (all the sets recursively parsed from nested threshold descriptions).
    for element in elements:
        if type(element) == dict:
            elementsParsed.append(parseSetsFromThresholdDescription(element))
        else:
            elementsParsed.append(frozenset({frozenset({element})}))
    allCombinations = list((getSetOfCartesianCombinationsOfSets(comb) for comb in itertools.combinations(elementsParsed, k)))
    return frozenset().union(*allCombinations)

def getSetOfCartesianCombinationsOfSets(inSets): #inSets is an iterable (list or tuple) of frozensets of frozensets. Returns a frozenSet of frozenSets
    cartesianCombinations = list((frozenset().union(*d) for d in itertools.product(*inSets)))
    return frozenset(cartesianCombinations)

def getUniverse(setSystem):
    nodes = set()
    for everySet in setSystem:
        for everyNode in everySet:
            nodes.add(everyNode)
    return nodes

def getUniverseAsym(setSystems): #setSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    nodes = set()
    for setSystem in setSystems.values():
        for everySet in setSystem:
            for everyNode in everySet:
                nodes.add(everyNode)
    return nodes

def getComplement(universe, setSystem):
    return frozenset([frozenset(universe.difference(s)) for s in setSystem])

def getComplementAsym(universe, setSystems): #setSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    res = {}
    for key, value in setSystems.items():
        res[key] = frozenset([frozenset(universe.difference(s)) for s in value])
    return res
    