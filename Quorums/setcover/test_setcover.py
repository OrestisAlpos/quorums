import Quorums.setcover.setcover as setcover
from pyroaring import BitMap

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

sets3a = [{1, 2}, {1, 3}, {1, 4}, {1, 5}]
sets3b = [{2, 4, 6}, {2, 5, 6}, {4, 5, 6}]
sets3c = [{2}, {4}, {5}]

def test_FixedParamAlgorithm():
    assert(setcover.set_cover_fixed_param_algorithm(set(universe1), sets1a, 3)[0] ==  False)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe1), sets1b, 3)[0] ==  False)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe1), sets1c, 3)[0] ==  True)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe1), sets1d, 3)[0] ==  True)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe1), sets1e, 3)[0] ==  True)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe1), sets1f, 3)[0] ==  True)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe2), sets2a, 3)[0] ==  False)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe2), sets2b, 3)[0] ==  False)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe2), sets2c, 3)[0] ==  True)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe2), sets2d, 3)[0] ==  True)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe2), sets2e, 3)[0] ==  False)
    assert(setcover.set_cover_fixed_param_algorithm(set(universe2), sets2f, 3)[0] ==  True)
    return True

# def test_FixedParamWith3Systems():
   # assert(setcover.set_cover_fixed_param_asym_algorithm(universe2, 3, sets3a, sets3b, sets3c)[0] == True)

def runAll():
    return test_FixedParamAlgorithm()