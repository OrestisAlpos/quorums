import BSC.checker.checker as checker
from pyroaring import BitMap
import time
import itertools
import timeit
import BSC.parser.jsonparser as jsonparser
import BSC.parser.parserutil as parserutil
import BSC.parser.bitmapparserutil as bitmapparserutil
import os
import json
from BSC.setcover.setcover import set_cover_fixed_param_asym_algorithm
import copy

"""
Bitmap:
twoSetUnion
1.3028550148010254
includesMissingProcesses one
1.3772728443145752
2.935894012451172   
includesMissingProcesses full
399.40345525741577

frozenset:
twoSetUnion
8.52665638923645
includesMissingProcesses one
0.33464860916137695
7.8000664710998535
includesMissingProcesses full
97.28007292747498
"""

"""
def test_bitmapTime():
    print('Bitmap:')
    universe = BitMap(set(range(1,89)))
    quorumSystem = jsonparser.parseAdaptedAsymQuorumSystemAsBitmap()[1]

    system1 = quorumSystem[1]
    system2 = quorumSystem[5]

    print('twoSetUnion')
    t0 = time.time()
    twoSetUnion = checker.twoUnionDiffSets(list(system1), list(system2)) # 1347921
    t1 = time.time()
    total = t1-t0
    print(total)

    print('includesMissingProcesses one')
    missingProcesses = universe.difference(twoSetUnion[0])
    t0 = time.time()
    for _ in itertools.repeat(None, 5000):
        for i in system1:
            if(missingProcesses.issubset(i)):
                return True
    t1 = time.time()
    total = t1-t0
    print(total)

    for i in range(100):
        t0 = time.time()
        for _ in itertools.repeat(None, 50000):
            if missingProcesses.issubset(list(system1)[i]):
                return True
        t1 = time.time()
        total = t1-t0
        print(total)

    return True

def test_frozensetTime():
    print('frozenset:')
    universe = set(range(1,89))
    quorumSystem = jsonparser.parseAdaptedAsymQuorumSystem()[1]

    system1 = list(quorumSystem[1])
    system2 = quorumSystem[5]

    print('twoSetUnion')
    t0 = time.time()
    twoSetUnion = checker.twoUnionDiffSets(list(system1), list(system2)) # 1347921
    t1 = time.time()
    total = t1-t0
    print(total)

    print('includesMissingProcesses one')
    missingProcesses = universe.difference(twoSetUnion[0])
    t0 = time.time()
    for _ in itertools.repeat(None, 5000):
        for i in system1:
            if(missingProcesses.issubset(i)):
                return True
    t1 = time.time()
    total = t1-t0
    print(total)

    for i in range(100):
        t0 = time.time()
        for _ in itertools.repeat(None, 50000):
            if missingProcesses.issubset(list(system1)[i]):
                return True
        t1 = time.time()
        total = t1-t0
        print(total)

    return True

def test_Timer(): # see results with: pytest test_checker.py -s
    
    parsedData = {
        1: [{2, 4, 6},
            {4, 5, 6},
            {2, 5, 6}],
        2: [{3, 4, 6},
            {4, 5, 6},
            {3, 5, 6}],
        3: [{4, 5, 6},
            {1, 5, 6},
            {1, 4, 6}],
        4: [{1, 6},
            {5, 6},
            {3, 6},
            {2, 6}],
        5: [{1, 6},
            {3, 6},
            {4, 6},
            {2, 6}],
        6: [{1, 4},
            {1, 3},
            {1, 2},
            {1, 5}]
        }
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3({1,2,3,4,5,6}, parsedData)
    t1 = time.time()
    total = t1-t0
    print('time for list sets (CT19Example2):')
    print(total)

    parsedData = jsonparser.parseAsymFailProneSystem('CT19Example2')[1]
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3({1,2,3,4,5,6}, parsedData)
    t1 = time.time()
    total = t1-t0
    print('time for frozenset frozensets (CT19Example2):')
    print(total)

    parsedData = jsonparser.parseAsymFailProneSystemAsBitmap('CT19Example2')[1]
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3(BitMap([1,2,3,4,5,6]), parsedData)    
    t1 = time.time()
    total = t1-t0
    print('time for list of bitmaps (CT19Example2):')
    print(total)

    parsedData = {
        1: [{3},
            {2},
            {4},
            {5}],
        2: [{3},
            {1},
            {4},
            {5}],
        3: [{2, 4},
            {1, 4},
            {1, 5},
            {2, 5}],
        4: [{3},
            {2},
            {1},
            {5}],
        5: [{2, 4}]
        }
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3({1,2,3,4,5}, parsedData)
    t1 = time.time()
    total = t1-t0
    print('time for list of sets (CT19Example1):')
    print(total)

    parsedData = jsonparser.parseAsymFailProneSystem('CT19Example1')[1]
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3({1,2,3,4,5}, parsedData)
    t1 = time.time()
    total = t1-t0
    print('time for frozenset frozensets (CT19Example1):')
    print(total)

    parsedData = jsonparser.parseAsymFailProneSystemAsBitmap('CT19Example1')[1]
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3(BitMap([1,2,3,4,5]), parsedData)    
    t1 = time.time()
    total = t1-t0
    print('time for list of bitmaps (CT19Example1):')
    print(total)
"""
"""
def test_timeit():

    configNames = [
    'CT19Example1',
    'CT19Example1Explicit',
    'CT19Example1Mixed',
    'CT19Example2',
    'CT19Example2SBAdaptation',
    'CT19Example2Version2',
    'CT19Example2Version2Explicit',
    'SBExample1',
    'CT19PresentationExample',
    'CT19PresentationExampleV2',
    'ZanoliniPaperExample'
    ]

    for key in configNames:
        print("Testing " + key + " with frozenset:")
        print(timeit.timeit(
            setup ='import BSC.parser.jsonparser as jsonparser \nfrom pyroaring import BitMap \nimport BSC.checker.checker as checker \n(universe, fps) = jsonparser.parseAsymFailProneSystem("' + key + '")', 
            stmt = 'checker.checkB3(universe, fps)', 
            number=5000))

        print("Testing " + key + " with BitMap:")
        print(timeit.timeit(
            setup ='import BSC.parser.jsonparser as jsonparser \nfrom pyroaring import BitMap \nimport BSC.checker.checker as checker \n(universe, fps) = jsonparser.parseAsymFailProneSystemAsBitmap("' + key + '")', 
            stmt = 'checker.checkB3(universe, fps)', 
            number=5000))
        
        print("Testing " + key + " with setcover:")
        print(timeit.timeit(
            setup ='import BSC.parser.jsonparser as jsonparser \nfrom pyroaring import BitMap \nimport BSC.checker.checker as checker \n(universe, fps) = jsonparser.parseAsymFailProneSystem("' + key + '")', 
            stmt = 'checker.checkB3withSetCover(universe, fps)', 
            number=5000))

        print("Testing " + key + " with BitMap setcover:")
        print(timeit.timeit(
            setup ='import BSC.parser.jsonparser as jsonparser \nfrom pyroaring import BitMap \nimport BSC.checker.checker as checker \n(universe, fps) = jsonparser.parseAsymFailProneSystemAsBitmap("' + key + '")', 
            stmt = 'checker.checkB3withSetCover(universe, fps)', 
            number=5000))
"""
"""
def test_stellar():
    print(timeit.timeit(
        setup ='import BSC.parser.jsonparser as jsonparser \nimport BSC.parser.parserutil as parserutil \nfrom pyroaring import BitMap \nimport BSC.checker.checker as checker \n(universe,parsedData) = jsonparser.parseAsymQuorumSystem() \n', 
        stmt = 'checker.checkB3withSetCover(universe, parsedData)',
        number=1))
"""


def test_misc_BitMap():
    print('parsing quorum system to BitMap...')
    (universe, quorumSystem) = jsonparser.parseAdaptedAsymQuorumSystemAsBitmap()

    system1 = quorumSystem[1] #1161
    system2 = quorumSystem[5] #1161
    keys = list(universe.values())

    print('union')
    t0 = time.time()
    twoSetUnion = checker.twoUnionDiffSets(list(system1), list(system2)) # 1347921
    t1 = time.time()
    total = t1-t0
    print(total)

    print('intersection')
    t0 = time.time()
    twoSetIntersection = checker.twoIntersectionDiffSets(list(system1), list(system2)) # 1347921
    t1 = time.time()
    total = t1-t0
    print(total)

    print('check setcover')
    t0 = time.time()
    (checksB3, solutionSets) = set_cover_fixed_param_asym_algorithm(keys[:], system1, system2, twoSetIntersection) # 3*(n^2m^2)
    if not checksB3:
        print(solutionSets)
        return False
    t1 = time.time()
    total = t1-t0
    print(total)

    print('test full')
    t0 = time.time()
    checker.checkB3withSetCover(universe, quorumSystem, 12)
    t1 = time.time()
    total = t1-t0
    print(total)

    """
    print('check for missing processes')
    t0 = time.time()
    for f in twoSetUnion: # n * m
        missingProcesses = set(universe.values()).difference(f)
        if(checker.includesMissingProcesses(missingProcesses, list(system1), list(system2))): # n + m
            return False
    t1 = time.time()
    total = t1-t0
    print(total)
    
    print("check setup:")
    t0 = time.time()
    asymmetricFailProneSystem = copy.copy(quorumSystem)

    if isinstance(universe,dict):
        keys = list(universe.values())
    else: 
        keys = list(universe)
    
    # to inverse dict : inv = {v: k for k, v in d.items()}
    if len(keys) == 0:
        return True
    t1 = time.time()
    total = t1-t0
    print(total)
    
    print("check loop:")
    # 3828
    t0 = time.time()
    for i in keys:
        firstsystem = asymmetricFailProneSystem[i]
        for j in range(i, len(keys)):
            key = keys[j]
            chosensystem = asymmetricFailProneSystem[key]
            # twoIntersection = checker.twoIntersectionDiffSets(firstsystem, chosensystem) # n * m
    t1 = time.time()
    total = t1-t0
    print(total) """
    

def test_misc_frozenset():

    print('parsing quorum system to frozenset...')
    (universe, quorumSystem) = jsonparser.parseAdaptedAsymQuorumSystem()

    system1 = quorumSystem[1]
    system2 = quorumSystem[5]
    keys = list(universe.values())

    print('union')
    t0 = time.time()
    twoSetUnion = checker.twoUnionDiffSets(list(system1), list(system2)) # 1347921
    t1 = time.time()
    total = t1-t0
    print(total)

    print('intersection')
    t0 = time.time()
    twoSetIntersection = checker.twoIntersectionDiffSets(list(system1), list(system2)) # 1347921
    t1 = time.time()
    total = t1-t0
    print(total)

    print('check setcover')
    t0 = time.time()
    (checksB3, solutionSets) = set_cover_fixed_param_asym_algorithm(keys[:], system1, system2, twoSetIntersection) # 3*(n^2m^2)
    if not checksB3:
        print(solutionSets)
        return False
    t1 = time.time()
    total = t1-t0
    print(total)

    print('test full')
    t0 = time.time()
    checker.checkB3withSetCover(universe, quorumSystem, 12)
    t1 = time.time()
    total = t1-t0
    print(total)

    """
    print('check for missing processes')
    t0 = time.time()
    for f in twoSetUnion: # n * m
        missingProcesses = set(universe.values()).difference(f)
        if(checker.includesMissingProcesses(missingProcesses, list(system1), list(system2))): # n + m
            return False
    t1 = time.time()
    total = t1-t0
    print(total)

    print("check setup:")
    t0 = time.time()
    asymmetricFailProneSystem = copy.copy(quorumSystem)

    if isinstance(universe,dict):
        keys = list(universe.values())
    else: 
        keys = list(universe)
    
    # to inverse dict : inv = {v: k for k, v in d.items()}
    if len(keys) == 0:
        return True
    t1 = time.time()
    total = t1-t0
    print(total)

    print("check loop:")
    t0 = time.time()
    for i in keys:
        firstsystem = asymmetricFailProneSystem[i]
        for j in range(i, len(keys)):
            key = keys[j]
            chosensystem = asymmetricFailProneSystem[key]
            # twoIntersection = checker.twoIntersectionDiffSets(firstsystem, chosensystem) # n * m
    t1 = time.time()
    total = t1-t0
    print(total)
    """

def runAll():
    return test_bitmapTime() | test_frozensetTime() | test_Timer() | test_timeit()