import numpy as np
import sss.linearAlgebraUtil as lautil

def test_PLU(confTitle):
    mspM, mspL = lautil.getMSP(confTitle)
    P, L, U = lautil.getPLU(mspM.T) # P MT = L U
    return np.allclose(np.matmul(P, mspM.T) , np.matmul(L, U))

def test_PLU_onSubgroup(confTitle, accessGroup):
    mspM, mspL = lautil.getMSP(confTitle)
    P, L, U = lautil.getPLU(mspM.T) # P MT = L U
    MTA = lautil.getColumnsIndexedByThisGroup(mspM.T, mspL, accessGroup)
    UA = lautil.getColumnsIndexedByThisGroup(U, mspL, accessGroup) # P MTA = L UA
    return np.allclose(np.matmul(P, MTA) , np.matmul(L, UA))

def runAll():
    return test_PLU('LcwExample') | test_PLU_onSubgroup('LcwExample', ['A', 'B', 'D', 'E'])


#  M S P   R E L A T E D   F U N C T I O N S

#performs the example from LCW paper
def test_performInsertion():
    #1
    M1 = np.array([[1]])
    #2
    M2 = lautil.getVandermonde(2,3)
    M1 = lautil.performMspInsertion(M1,M2,0)
    assert(np.array_equal(M1, np.array([[1,1], [1,2], [1,3]])))
    #3
    M1 = lautil.performMspInsertion(M1,M2,0)
    assert(np.array_equal(M1, np.array([[1,1,1], [1,1,2], [1,1,3], [1,2,0], [1,3,0]])))
    #4
    M1 = lautil.performMspInsertion(M1,M2,3)
    assert(np.array_equal(M1, np.array([[1,1,1,0], [1,1,2,0], [1,1,3,0], [1,2,0,1], [1,2,0,2], [1,2,0,3], [1,3,0,0]])))
    #5
    M1 = lautil.performMspInsertion(M1,M2,6)
    assert(np.array_equal(M1, np.array([[1,1,1,0,0], [1,1,2,0,0], [1,1,3,0,0], [1,2,0,1,0], [1,2,0,2,0], [1,2,0,3,0], [1,3,0,0,1], [1,3,0,0,2], [1,3,0,0,3]])))
    #5
    M2 = lautil.getVandermonde(3,4)
    M1 = lautil.performMspInsertion(M1,M2,8)
    assert(np.array_equal(M1, np.array([[1,1,1,0,0,0,0], [1,1,2,0,0,0,0], [1,1,3,0,0,0,0], [1,2,0,1,0,0,0], [1,2,0,2,0,0,0], [1,2,0,3,0,0,0], [1,3,0,0,1,0,0], [1,3,0,0,2,0,0], [1,3,0,0,3,1,1], [1,3,0,0,3,2,4], [1,3,0,0,3,3,9], [1,3,0,0,3,4,16]])))
    return True

def test_getMSP(confTitle):
    M, L = lautil.getMSP(confTitle)
    res = np.array([[ 1,  1,  1,  0,  0,  0,  0],
   [ 1,  1,  2,  0,  0,  0,  0],
   [ 1,  1,  3,  0,  0,  0,  0],
   [ 1,  2,  0,  1,  0,  0,  0],
   [ 1,  2,  0,  2,  0,  0,  0],
   [ 1,  2,  0,  3,  0,  0,  0],
   [ 1,  3,  0,  0,  1,  0,  0],
   [ 1,  3,  0,  0,  2,  0,  0],
   [ 1,  3,  0,  0,  3,  1,  1],
   [ 1,  3,  0,  0,  3,  2,  4],
   [ 1,  3,  0,  0,  3,  3,  9],
   [ 1,  3,  0,  0,  3,  4, 16]])
    assert(np.array_equal(M, res))
    assert(L == ['A','B','C','D','E','F','G','H','I','J','K','L'])
    return True

def runAllMsp():
    return test_performInsertion() | test_getMSP('LcwExample')