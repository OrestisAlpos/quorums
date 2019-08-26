import numpy as np
import util

#Simple Proof of Concept implementation of the LCW algorithm.

def getMSP(confTitle):
    M = getVandermonde(1,1)
    L = [util.parseThresholdDescription(confTitle)]
    r = 0
    while (r >= 0):
        nextIns = L.pop(r)
        M2 = getVandermonde(nextIns['select'], len(nextIns['out-of']))
        M = performInsertion(M, M2, r)
        for i in range(len(nextIns['out-of'])):
            L.insert(r + i, nextIns['out-of'][i])
        r = findFirstNestedThres(L)
    return (M,L)

def getVandermonde(thres, ntot):
    return np.array([[n ** t for t in range(thres)] for n in range(1, ntot + 1)])

#insertion of matrix M2 (2D) in the row of matrix M1 (2D) specified by the index r, with r in [0, m1-1]
def performInsertion(M1, M2, r):
    (m1, _) = M1.shape
    (m2, d2) = M2.shape 
    M11 = M1[:r, :]
    v1 = M1[r,:]
    v1rep = np.array([v1,] * m2)
    M12 = M1[r+1:, :]
    z1 = np.zeros((r, d2 - 1), dtype = int)
    M22 = M2[:,1:]
    z2 = np.zeros((m1 - 1 - r, d2 - 1), dtype = int)
    # M11   z1
    # v1rep M22
    # M12   z2
    assert(M11.shape[0] == z1.shape[0])
    assert(M12.shape[0] == z2.shape[0])
    res1 = np.concatenate((M11, v1rep, M12), axis = 0)
    res2 = np.concatenate((z1,M22,z2), axis = 0)
    return np.concatenate((res1, res2), axis = 1)

def findFirstNestedThres(ownersList):
    for i in range(len(ownersList)):
        if type(ownersList[i]) == dict:
            return i
    return -1