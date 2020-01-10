import BSC.checker.checker as checker
import itertools
from pyroaring import BitMap
import time
from ..parser.jsonparser import parseJson, parseJsonAsym, parseJsonAsymToBitmap, parseAsymFailProneSystem, parseAsymFailProneSystemAsBitmap

universe1 = {1,2,3,4}
sets1a = [{1}, {2}, {3}]
sets1b = [{1}, {2}, {4}]
sets1c = [{1}, {2}, {3, 4}]
sets1d = [{1,2}, {2,3}, {3, 4}]
sets1e = [{1,2,3}, {4}]
sets1f = [{1, 2, 3, 4}]

universe2 = {1,2,3,4,5,6}
sets2a = [{1,3}, {2,4}, {1,3,4}]
sets2b = [{1,3}, {2,4}, {1,5,4}]
sets2c = [{1,2, 3}, {2, 3, 4}, {5,6}]
sets2d = [{1,3}, {2,4}, {1,5,6}]
sets2e = [{1,2}, {2,3,4}, {1,3}, {3,6}, {5}]
sets2f = [{1,2}, {2,3,4}, {1,3}, {3,6}, {1,5}]

def test_PowersetOfFailProneSystem():
    assert(checker.getPowerSetsOfFailProneSystem(sets2a) == {frozenset({3, 4}), frozenset({2}), frozenset({1, 4}), frozenset({3}), frozenset({2, 4}), frozenset({1}), frozenset(), frozenset({1, 3}), frozenset({1, 3, 4}), frozenset({4})})
    assert(checker.getPowerSetsOfFailProneSystem(sets2b) == {frozenset({2}), frozenset({1, 4}), frozenset({4, 5}), frozenset({3}), frozenset({2, 4}), frozenset({1}), frozenset({1, 5}), frozenset({1, 4, 5}), frozenset(), frozenset({1, 3}), frozenset({4}), frozenset({5})})
    return True

def test_CheckB3Brute():
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example1")
    assert(checker.checkB3brute(set(universe.values()), failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2")
    assert(checker.checkB3brute(set(universe.values()), failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2SBAdaptation")
    assert(checker.checkB3brute(set(universe.values()), failProneSystem) == True)
    return True

def test_CheckB3():
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example1")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2")
    assert(checker.checkB3(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2SBAdaptation")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19PresentationExample")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19PresentationExampleV2")
    assert(checker.checkB3(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystem("ZanoliniPaperExample")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2Version2")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("SBExample1")
    assert(checker.checkB3(universe, failProneSystem) == False)
    return True

def test_CheckB3BitMap():
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example1")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2")
    assert(checker.checkB3(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2SBAdaptation")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2Version2")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2Version2Explicit")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19PresentationExample")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19PresentationExampleV2")
    assert(checker.checkB3(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("ZanoliniPaperExample")
    assert(checker.checkB3(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("SBExample1")
    assert(checker.checkB3(universe, failProneSystem) == False)
    return True

def test_CheckB3WithSetCover():
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example1")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2SBAdaptation")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2Version2")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19Example2Version2Explicit")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19PresentationExample")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("CT19PresentationExampleV2")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystem("ZanoliniPaperExample")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystem("SBExample1")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == False)
    return True


def test_CheckB3BitMapWithSetCover():
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example1")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2SBAdaptation")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2Version2")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19Example2Version2Explicit")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19PresentationExample")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("CT19PresentationExampleV2")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == False)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("ZanoliniPaperExample")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == True)
    (universe, failProneSystem) = parseAsymFailProneSystemAsBitmap("SBExample1")
    assert(checker.checkB3withSetCover(universe, failProneSystem) == False)
    return True


def runAll():
    return test_PowersetOfFailProneSystem() | test_CheckB3Brute() \
         | test_CheckB3() | test_CheckB3BitMap() \
         | test_CheckB3WithSetCover() | test_CheckB3BitMapWithSetCover()