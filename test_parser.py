from parserutil import parseSetsFromThresholdDescription, parseSetsFromDescription
from parser import parseJson
from math import factorial

def cc(n, r):
    return factorial(n) // factorial(r) // factorial(n-r)

thresSet0 = dict({"select": 1, "out-of":[2]})
thresSet1 = dict({"select": 1, "out-of":[2,3]})
thresSet1b = dict({"select": 1, "out-of":[4,5]})
thresSet1c = dict({"select": 1, "out-of":[6,7]})
thresSet2 = dict({"select": 1, "out-of":[2,3,4,5]})
thresSet3 = dict({"select": 2, "out-of":[2,4]})
thresSet4 = dict({"select": 2, "out-of":[2,4,5]})
thresSet4b = dict({"select": 2, "out-of":[6,7,8]})
thresSet5 = dict({"select": 2, "out-of":[2,4,5,6]})
thresSet6 = dict({"select": 3, "out-of":[1,2,3]})
thresSet7 = dict({"select": 3, "out-of":[1,2,3,4]})
thresSet8 = dict({"select": 4, "out-of":[1,2,3,4,5,6,7,8,9,10]})

thresSetN0 = {"select": 1, "out-of":[1, 2, 3, {"select": 1, "out-of":[5,6]}]}
thresSetN1 = {'select': 2, 'out-of': [1, 2, 3]}
thresSetN2 = {'select': 1, 'out-of': [5, 6]}
thresSetN3 = {'select': 2, 'out-of': [5, 6]}
thresSetN4 = {'select': 1, 'out-of': [1, 2, 3, {'select': 2, 'out-of': [5, 6]}]}
thresSetN5 = {'select': 2, 'out-of': [1, 2, 3, {'select': 2, 'out-of': [5, 6]}]}
thresSetN6 = {'select': 1, 'out-of': [{'select': 1, 'out-of': [1, 2]}, {'select': 1, 'out-of': [3,4]}] }
thresSetN7 = {'select': 2, 'out-of': [{'select': 1, 'out-of': [1, 2]}, {'select': 1, 'out-of': [3,4]}] }
thresSetN8 = {'select': 2, 'out-of': [{'select': 2, 'out-of': [1, 2, 3]}, {'select': 2, 'out-of': ['A','B','C']}] }
thresSetN9 = {'select': 2, 'out-of': [{'select': 2, 'out-of': [1, 2, 3]}, {'select': 2, 'out-of': ['A','B','C']}, {'select': 2, 'out-of': ['a', 'b', 'c']}] }
thresSetN10 = {'select': 1, 'out-of': [{'select': 2, 'out-of': [1, 2, {'select': 2, 'out-of': ['a','b','c']}]}, {'select': 2, 'out-of': [3,4, {'select': 2, 'out-of': ['A','B','C'] }] }]}

descSet0 = [thresSet0, 6]
descSet1 = [thresSet1, 6, 7]
descSet2 = [thresSet2, 6]
descSet3 = [thresSet3, 6]
descSet4 = [thresSet4, 6, 7]
descSet5 = [thresSet5]
descSet6 = [6, thresSet6]
descSet7 = [6, 7, thresSet7]

descSet8 = [thresSet0, thresSet0]
descSet9 = [thresSet1, thresSet1b]
descSet10 = [thresSet4, thresSet4b]
descSet11 = [thresSet1, thresSet3]
descSet12 = [thresSet1, thresSet1b, thresSet1c]
descSet13 = [7, thresSet1, thresSet1b, 8, 9]
descSet14 = [1,2,3]


def test_ParseSetsFromThresholdDescription():    
    assert(parseSetsFromThresholdDescription(thresSet0) == { frozenset([2]) }   ) 
    assert(parseSetsFromThresholdDescription(thresSet1) == { frozenset([2]), frozenset([3]) })
    assert(parseSetsFromThresholdDescription(thresSet2) == { frozenset([2]), frozenset([3]), frozenset([4]), frozenset([5]) })
    assert(parseSetsFromThresholdDescription(thresSet3) == { frozenset([2,4]) })
    assert(parseSetsFromThresholdDescription(thresSet4) == { frozenset([2,4]), frozenset([2,5]), frozenset([4,5]) })    
    assert(parseSetsFromThresholdDescription(thresSet5) == { frozenset([2,4]), frozenset([2,5]), frozenset([2,6]), frozenset([4,5]), frozenset([4,6]), frozenset([5,6]) })
    assert(parseSetsFromThresholdDescription(thresSet6) == { frozenset([1,2,3]) })
    assert(parseSetsFromThresholdDescription(thresSet7) == { frozenset([1,2,3]), frozenset([1,2,4]), frozenset([1,3,4]), frozenset([2,3,4]) })
    assert(len(parseSetsFromThresholdDescription(thresSet8)) == cc(10,4))
    return True

def test_ParseSetsFromThresholdDescriptionWithNested():
    assert(parseSetsFromThresholdDescription(thresSetN0) == frozenset({frozenset({3}), frozenset({2}), frozenset({1}), frozenset({6}), frozenset({5})}))
    assert(parseSetsFromThresholdDescription(thresSetN1) == frozenset({frozenset({1, 3}), frozenset({2, 3}), frozenset({1, 2})}))
    assert(parseSetsFromThresholdDescription(thresSetN2) == frozenset({frozenset({5}), frozenset({6})}))
    assert(parseSetsFromThresholdDescription(thresSetN3) == frozenset({frozenset({5, 6})}))
    assert(parseSetsFromThresholdDescription(thresSetN4) == frozenset({frozenset({3}), frozenset({2}), frozenset({1}), frozenset({5, 6})}))
    assert(parseSetsFromThresholdDescription(thresSetN5) == frozenset({frozenset({2, 3}), frozenset({2, 5, 6}), frozenset({1, 2}), frozenset({1, 3}), frozenset({3, 5, 6}), frozenset({1, 5, 6})}))
    assert(parseSetsFromThresholdDescription(thresSetN6) == frozenset({frozenset({3}), frozenset({2}), frozenset({1}), frozenset({4})}))
    assert(parseSetsFromThresholdDescription(thresSetN7) == frozenset({frozenset({2, 4}), frozenset({1, 4}), frozenset({1, 3}), frozenset({2, 3})}))
    assert(parseSetsFromThresholdDescription(thresSetN8) == frozenset({frozenset({'B', 2, 3, 'C'}), frozenset({2, 3, 'A', 'B'}), frozenset({1, 2, 'A', 'C'}), frozenset({2, 3, 'A', 'C'}), frozenset({1, 'A', 3, 'C'}), frozenset({1, 2, 'A', 'B'}), frozenset({1, 2, 'C', 'B'}), frozenset({'B', 1, 3, 'C'}), frozenset({1, 'A', 3, 'B'})}))
    assert( len(parseSetsFromThresholdDescription(thresSetN9)) == 27)
    assert(parseSetsFromThresholdDescription(thresSetN10) == frozenset({frozenset({3, 4}), frozenset({'A', 3, 'C'}), frozenset({1, 2}), frozenset({2, 'b', 'c'}), frozenset({1, 'b', 'c'}), frozenset({1, 'b', 'a'}), frozenset({2, 'a', 'c'}), frozenset({'B', 3, 'C'}), frozenset({'A', 3, 'B'}), frozenset({2, 'b', 'a'}), frozenset({1, 'a', 'c'}), frozenset({'A', 4, 'C'}), frozenset({'A', 4, 'B'}), frozenset({'C', 4, 'B'})}))
    return True

def test_ParseSetsFromDescription():
    assert(parseSetsFromDescription(descSet0) == frozenset({ frozenset([2,6]) }) )    
    assert(parseSetsFromDescription(descSet1) == frozenset({ frozenset([2, 6, 7]), frozenset([3, 6, 7]) }) )
    assert(parseSetsFromDescription(descSet2) == frozenset({ frozenset([2, 6]), frozenset([3, 6]), frozenset([4, 6]), frozenset([5, 6]) }) )
    assert(parseSetsFromDescription(descSet3) == frozenset({ frozenset([2,4, 6]) }) )
    assert(parseSetsFromDescription(descSet4) == frozenset({ frozenset([2,4, 6, 7]), frozenset([2,5, 6, 7]), frozenset([4,5, 6 ,7]) }) )    
    assert(parseSetsFromDescription(descSet5) == frozenset({ frozenset([2,4]), frozenset([2,5]), frozenset([2,6]), frozenset([4,5]), frozenset([4,6]), frozenset([5,6]) }) )
    assert(parseSetsFromDescription(descSet6) == frozenset({ frozenset([1,2,3,6]) }) )
    assert(parseSetsFromDescription(descSet7) == frozenset({ frozenset([1,2,3,6,7]), frozenset([1,2,4,6,7]), frozenset([1,3,4,6,7]), frozenset([2,3,4,6,7]) }) )
    assert(parseSetsFromDescription(descSet8) == frozenset({ frozenset([2]) }) )
    assert(parseSetsFromDescription(descSet9) == frozenset({ frozenset([2,4]), frozenset([2,5]), frozenset([3,4]), frozenset([3,5]) }) )
    assert(parseSetsFromDescription(descSet10) ==frozenset({  frozenset([2,4,6,7]), frozenset([2,4,6,8]), frozenset([2,4,7,8]), frozenset([2,5,6,7]), frozenset([2,5,6,8]), frozenset([2,5,7,8]), frozenset([4,5,6,7]), frozenset([4,5,6,8]), frozenset([4,5,7,8]) }) )
    assert(parseSetsFromDescription(descSet11) ==frozenset({  frozenset([2,4]), frozenset([2,3,4]) }) )
    assert(parseSetsFromDescription(descSet12) ==frozenset({  frozenset([2,4,6]), frozenset([2,4,7]), frozenset([2,5,6]), frozenset([2,5,7]), frozenset([3,4,6]), frozenset([3,4,7]), frozenset([3,5,6]), frozenset([3,5,7]) }) )
    assert(parseSetsFromDescription(descSet13) ==frozenset({  frozenset([2,4,7,8,9]), frozenset([2,5,7,8,9]), frozenset([3,4,7,8,9]), frozenset([3,5,7,8,9]) }) )
    assert(parseSetsFromDescription(descSet14) ==frozenset({  frozenset([1,2,3]) }) )
    return True

def test_parseJson():
    assert(parseJson("F1") == frozenset({ frozenset({1, 2}), frozenset({2, 3}), frozenset({3, 4}) }) )
    assert(parseJson("F2") == frozenset({ frozenset({6}), frozenset({7}) }) )
    assert(parseJson("F3") == frozenset({ frozenset({2, 4}), frozenset({2, 5}), frozenset({4, 5}) }) )
    assert(parseJson("F4") == frozenset({ frozenset({1, 6}), frozenset({1, 7}) }) )
    assert(parseJson("F5") == frozenset({ frozenset({2, 4, 6}), frozenset({2, 5, 6}), frozenset({4, 5, 6}) }) )
    assert(parseJson("F6") == frozenset({ frozenset({2, 4}), frozenset({2, 5}), frozenset({3, 4}), frozenset({3, 5}) }) )
    assert(parseJson("F7") == frozenset({ frozenset({1, 2, 4}), frozenset({1, 2, 5}), frozenset({1, 3, 4}), frozenset({1, 3, 5}) }) )
    assert(parseJson("F8") == frozenset({ frozenset({2, 4}), frozenset({2, 5}), frozenset({3, 4}), frozenset({3, 5}), frozenset({10, 12}), frozenset({10, 13}), frozenset({11, 12}), frozenset({11, 13}) }) )
    assert(parseJson("F9") == frozenset({frozenset({2, 4}), frozenset({1, 4}), frozenset({1, 3}), frozenset({2, 3})}))
    return True

def runAll():
    return test_ParseSetsFromThresholdDescription() | test_ParseSetsFromDescription() | test_parseJson() | test_ParseSetsFromThresholdDescriptionWithNested()