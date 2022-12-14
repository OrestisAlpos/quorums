import json
import itertools
import functools 
from ..stellar.stellarQuorumParser import getIntegerIdsForPubKeys

def parseSetsFromDescription(description):
    if (len(description) == 1) & (type(description[0]) == dict):
        return parseSetsFromThresholdDescription(description[0])
    else:
        size = len(description)
        return parseSetsFromThresholdDescription({'select':size, 'out-of':description})

def parseSetsFromThresholdDescription(thresholdDict, universe = {}): #returns a frozenset of frozensets satisfying a choose-k-out-of-tot threshold
    k = thresholdDict['select']
    elements = thresholdDict['out-of']
    elementsParsed = [] #Contains frozensets of frozensets (all the sets recursively parsed from nested threshold descriptions).
    for element in elements:
        if type(element) == dict:
            elementsParsed.append(parseSetsFromThresholdDescription(element, universe))
        else:
            if element in universe:
                elementsParsed.append(frozenset({frozenset({universe[element]})}))
            else:
                elementsParsed.append(frozenset({frozenset({element})}))
    allCombinations = list((getSetOfCartesianCombinationsOfSets(comb) for comb in itertools.combinations(elementsParsed, k)))
    return frozenset().union(*allCombinations)

def getSetOfCartesianCombinationsOfSets(inSets): #inSets is an iterable (list or tuple) of frozensets of frozensets. Returns a frozenSet of frozenSets
    cartesianCombinations = list((frozenset().union(*d) for d in itertools.product(*inSets)))
    return frozenset(cartesianCombinations)

def parseArraysFromThresholdDescription(thresholdArray, universe = {}):
    res = []
    for elem in thresholdArray:
        res.append(frozenset(elem))
    return frozenset(res)

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
    return list(frozenset(universe.difference(s)) for s in setSystem)

def getComplementAsym(universe, setSystems): #setSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    res = {}
    for key, value in setSystems.items():
        res[key] = frozenset(frozenset(universe.difference(s)) for s in value)
    return res

def setIntegerIdsForPubKeys(confFile, confTitle = ''):
    systemDescription = ""
    with open(confFile, 'r') as conf:
        jsonString = json.loads(conf.read())
    if confTitle == "":
        systemDescription = jsonString
    else:
        systemDescription = jsonString[confTitle]
    res = {}
    counter = 1
    for processDescription in systemDescription:
        res[processDescription['PubKey']] = counter
        counter += 1

    return res
    