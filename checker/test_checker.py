import checker
import bitmapchecker
from jsonparser import parseJson, parseJsonAsym, parseJsonAsymToBitmap
import time
import itertools
from pyroaring import BitMap
import timeit


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

def test_CheckB3Brute():
    assert(checker.checkB3brute({1,2,3,4,5}, parseJsonAsym("CT19Example1")) == False)
    assert(checker.checkB3brute({1,2,3,4,5,6}, parseJsonAsym("CT19Example2")) == True)
    assert(checker.checkB3brute({1,2,3,4,5,6}, parseJsonAsym("CT19Example2Adapted")) == False)

def test_CheckB3():
    t0 = time.time()

    assert(checker.checkB3({1,2,3,4,5}, parseJsonAsym("CT19Example1")) == False)
    assert(checker.checkB3({1,2,3,4,5,6}, parseJsonAsym("CT19Example2")) == True)
    assert(checker.checkB3({1,2,3,4,5,6}, parseJsonAsym("CT19Example2Adapted")) == False)
    t1 = time.time()

    total = t1-t0
    print(total)

def test_CheckB3BitMap():
    t0 = time.time()

    assert(checker.checkB3(BitMap([1,2,3,4,5]), parseJsonAsymToBitmap("CT19Example1")) == False)
    assert(checker.checkB3(BitMap([1,2,3,4,5,6]), parseJsonAsymToBitmap("CT19Example2")) == True)
    assert(checker.checkB3(BitMap([1,2,3,4,5,6]), parseJsonAsymToBitmap("CT19Example2Adapted")) == False)
    t1 = time.time()

    total = t1-t0
    print(total)

def test_Timer(): # see results with: pytest test_checker.py -s
    
    parsedData = {
        '1': [{2, 4, 6},
            {4, 5, 6},
            {2, 5, 6}],
        '2': [{3, 4, 6},
            {4, 5, 6},
            {3, 5, 6}],
        '3': [{4, 5, 6},
            {1, 5, 6},
            {1, 4, 6}],
        '4': [{1, 6},
            {5, 6},
            {3, 6},
            {2, 6}],
        '5': [{1, 6},
            {3, 6},
            {4, 6},
            {2, 6}],
        '6': [{1, 4},
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

    parsedData = parseJsonAsym('CT19Example2')
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3({1,2,3,4,5,6}, parsedData)
    t1 = time.time()
    total = t1-t0
    print('time for frozenset frozensets (CT19Example2):')
    print(total)

    parsedData = parseJsonAsymToBitmap('CT19Example2')
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3(BitMap([1,2,3,4,5,6]), parsedData)    
    t1 = time.time()
    total = t1-t0
    print('time for list of bitmaps (CT19Example2):')
    print(total)

    parsedData = {
        '1': [{3},
            {2},
            {4},
            {5}],
        '2': [{3},
            {1},
            {4},
            {5}],
        '3': [{2, 4},
            {1, 4},
            {1, 5},
            {2, 5}],
        '4': [{3},
            {2},
            {1},
            {5}],
        '5': [{2, 4}]
        }
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3({1,2,3,4,5}, parsedData)
    t1 = time.time()
    total = t1-t0
    print('time for list of sets (CT19Example1):')
    print(total)

    parsedData = parseJsonAsym('CT19Example1')
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3({1,2,3,4,5}, parsedData)
    t1 = time.time()
    total = t1-t0
    print('time for frozenset frozensets (CT19Example1):')
    print(total)

    parsedData = parseJsonAsymToBitmap('CT19Example1')
    t0 = time.time()
    for _ in itertools.repeat(None, 2000):
        checker.checkB3(BitMap([1,2,3,4,5]), parsedData)    
    t1 = time.time()
    total = t1-t0
    print('time for list of bitmaps (CT19Example1):')
    print(total)

    print('\ntimeit list of sets')
    print(timeit.timeit(
        setup ='import jsonparser \nfrom pyroaring import BitMap \nimport checker \nparsedData = parsedData = {\'1\': [{3},{2},{4},{5}],\'2\': [{3},{1},{4},{5}],\'3\': [{2, 4},{1, 4},{1, 5},{2, 5}],\'4\': [{3},{2},{1},{5}],\'5\': [{2, 4}]}', 
        stmt = 'checker.checkB3({1,2,3,4,5}, parsedData)', 
        number=2000))
    print('timeit frozenset')
    print(timeit.timeit(
        setup ='import jsonparser \nfrom pyroaring import BitMap \nimport checker \nparsedData = {\'1\': frozenset({frozenset({3}),frozenset({2}),frozenset({4}),frozenset({5})}),\'2\': frozenset({frozenset({3}),frozenset({1}),frozenset({4}),frozenset({5})}),\'3\': frozenset({frozenset({2, 4}),frozenset({1, 4}),frozenset({1, 5}),frozenset({2, 5})}),\'4\': frozenset({frozenset({3}),frozenset({2}),frozenset({1}),frozenset({5})}),\'5\': frozenset({frozenset({2, 4})})}', 
        stmt = 'checker.checkB3({1,2,3,4,5}, parsedData)', 
        number=2000))
    print('timeit bitmap')
    print(timeit.timeit(
        setup ='import jsonparser \nfrom pyroaring import BitMap \nimport checker \nparsedData = {\'1\':[BitMap([2]),BitMap([3]),BitMap([4]),BitMap([5])],\'2\':[BitMap([1]),BitMap([3]),BitMap([4]),BitMap([5])],\'3\':[BitMap([1, 4]),BitMap([1, 5]),BitMap([2, 4]),BitMap([2, 5])],\'4\':[BitMap([1]),BitMap([2]),BitMap([3]),BitMap([5])],\'5\':[BitMap([2, 4])]}', 
        stmt = 'checker.checkB3(BitMap([1,2,3,4,5]), parsedData)', 
        number=2000))

def runAll():
    return test_PowersetOfFailProneSystem() | test_CheckB3Brute() | test_CheckB3() | test_CheckB3BitMap()