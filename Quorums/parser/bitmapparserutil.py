import json
import itertools
import functools 
from pyroaring import BitMap

def parseSetsFromDescription(description):
    if (len(description) == 1) & (type(description[0]) == dict):
        return parseBitMapSetsFromThresholdDescription(description[0])
    else:
        size = len(description)
        return parseBitMapSetsFromThresholdDescription({'select':size, 'out-of':description})

def parseBitMapSetsFromThresholdDescription(thresholdDict, universe = {}): #returns a frozenset of frozensets satisfying a choose-k-out-of-tot threshold
    k = thresholdDict['select']
    elements = thresholdDict['out-of']
    elementsParsed = [] #Contains frozensets of frozensets (all the sets recursively parsed from nested threshold descriptions).
    for element in elements:
        if type(element) == dict:
            elementsParsed.append(parseBitMapSetsFromThresholdDescription(element, universe))
        else:
            if element in universe:
                elementsParsed.append([BitMap([universe[element]])])
            else:
                elementsParsed.append([BitMap([element])])
    allCombinations = list((getBitMapSetOfCartesianCombinationsOfSets(comb) for comb in itertools.combinations(elementsParsed, k)))
    result = [j for sub in allCombinations for j in sub]
    return result

def getBitMapSetOfCartesianCombinationsOfSets(inSets): #inSets is an iterable (list or tuple) of frozensets of frozensets. Returns a frozenSet of frozenSets
    cartesianCombinations = list(BitMap([]).union(*d) for d in itertools.product(*inSets))   
    return cartesianCombinations

def parseArraysFromThresholdDescription(thresholdArray, universe = {}):
    res = []
    for elem in thresholdArray:
        res.append(BitMap(elem))
    return res

def getUniverse(setSystem):
    nodes = BitMap()
    for everySet in setSystem:
        for everyNode in everySet:
            nodes.add(everyNode)
    return nodes

def getUniverseAsym(setSystems): #setSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    nodes = BitMap()
    for setSystem in setSystems.values():
        for everySet in setSystem:
            for everyNode in everySet:
                nodes.add(everyNode)
    return nodes

def getComplement(universe, setSystem):
    return list(BitMap(universe.difference(s)) for s in setSystem)

def getComplementAsym(universe, setSystems): #setSystems is a dict str (name of process) -> frozenset of frozensets (failProneSet of process)
    res = {}
    for key, value in setSystems.items():
        res[key] = list(BitMap(universe.difference(s)) for s in value)
    return res