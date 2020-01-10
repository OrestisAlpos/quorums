from pyroaring import BitMap
import time
import copy
import BSC.parser.parserutil as parserutil
import BSC.parser.bitmapparserutil as bitmapparserutil
import BSC.checker.checker as checker
import BSC.parser.jsonparser as jsonparser

def test_stellarWithBitMap():
    print('BitMap:')

    print('Parsing quorum system...')
    t0 = time.time()
    (universe, quorumSystem) = jsonparser.parseAdaptedAsymQuorumSystemAsBitmap()
    t1 = time.time()
    total = t1-t0
    print(total)

    print('Converting to fail prone system...')
    t0 = time.time()
    failProneSystem = bitmapparserutil.getComplementAsym(set(universe.values()), quorumSystem)
    t1 = time.time()
    total = t1-t0
    print(total)

    print('Checking B3 for BitMap...')
    t0 = time.time()
    checksB3 = checker.checkB3withSetCover(universe, failProneSystem)
    t1 = time.time()
    total = t1-t0
    print(total)

    assert(checksB3 == False)

def test_stellarWithFrozenset():
    print('frozenset:')

    print('Parsing quorum system...')
    t0 = time.time()
    (universe, quorumSystem) = jsonparser.parseAdaptedAsymQuorumSystem()
    t1 = time.time()
    total = t1-t0
    print(total)

    print('Converting to fail prone system...')
    t0 = time.time()
    failProneSystem = parserutil.getComplementAsym(set(universe.values()), quorumSystem)
    t1 = time.time()
    total = t1-t0
    print(total)

    print('Checking B3 for Frozenset...')
    t0 = time.time()
    checksB3 = checker.checkB3withSetCover(universe, failProneSystem)
    t1 = time.time()
    total = t1-t0
    print(total)

    assert(checksB3 == False)

def runAll():
    return test_stellarWithBitMap() | test_stellarWithFrozenset()