import numpy as np
from scipy import linalg
import sympy
import random
import Quorums.parser.jsonparser as parser

# M,rho describe the MSP, such as: M, rho = msputil.getMSP(accessStructureTitle)
# accesGroup is a list that describes the players that try to reconstruct the secret, such as: accessGroup = ['A', 'B', 'D', 'E']
# returns l such us: x * Ma = e1, where e1 = (1,0,0,...)
def findRecombinationVector(M, rho, accessGroup):
    m,d = M.shape
    accessGroupIndices = [i for i in range(m) if rho[i] in accessGroup]
    M_a = M[accessGroupIndices, :]
    e = np.array([1] + [0]*(M_a.shape[1]-1)).reshape((7,1))
    sol = solveLinearEquation(M_a.T, e) #TODO: Call getRecombinationVector() here
    return list(zip(sol, accessGroupIndices))

def getRecombinationVector(mspM, mspL, accessGroup):
    U_rref, y_rref, pivots = getUMatrixInRref(mspM)
    U_rref_A = getColumnsIndexedByThisGroup(U_rref, mspL, accessGroup)
    recombinationVector = solveLinearEquation(U_rref_A, y_rref)
    return recombinationVector

def solveLinearEquation(A,b):
    augm = np.concatenate((A, b), axis = 1)
    augm_rref, pivots = sympy.Matrix(augm).rref()
    augm_rref = np.array(augm_rref, dtype=float)
    if not systemHasSolution(augm_rref):
        return np.array([])
    x = []
    A_rref = augm_rref[:,:-1]   #coef. matrix in rref
    b_rref = augm_rref[:,-1]    #constant matrix in rref
    for i in range(A.shape[1]): #for every column of the coef. matrix (this can be a pivot-variable column or a free-variable column)
        if i in pivots:                         
            index = np.where(A_rref[:,i] == 1)[0][0]
            x_i = b_rref[index]     # if it is a pivot-variable column (also called leading-variable)
            x.append(x_i)           # then the value of that variable is indicated by the constant term
        else:
            x.append(0)             # if it is a free-variable column, set its value to 0
    return np.array(x)
    
def systemHasSolution(augm_rref):
    for i in range(augm_rref.shape[0]):
        if np.all(augm_rref[i, :-1] == 0) and augm_rref[i, -1] != 0:
            return False
    return True

# This function takes as input the M matrix of the MSP.
# it calculates the PLU decomposition of M.T, so that P * M.T = L * U,
# it solves L * y = P * e for y,
# it transforms the augmented matrix U|y into rref, so that the eqation U * x = y can be easily solved.
# It returns the reduced coeficient matrix U_rref, the reduced constants matrix y_rref and a tuple with the pivot row indices (leading variables)
def getUMatrixInRref(mspM): 
    d = mspM.shape[1]
    e = np.array([1] + [0]*(d-1)) #target vector = (1, 0, 0, ...)
    P, L, U = getPLU(mspM.T) # P * msmM.T = L * U
    y = np.linalg.solve(L, np.matmul(P, e)).reshape(d,1) # Solve Ly = Pe for y
    augm = np.concatenate((U, y), axis = 1) # To solve Ux = y, create the augmented matrix U|y and bring it in reduced row echelon form
    Uy_rref, pivots = sympy.Matrix(augm).rref()
    Uy_rref = np.array(Uy_rref, dtype=float) 
    return Uy_rref[:,:-1], Uy_rref[:,-1], pivots

def getPLU(arr): # P * arr = L * U
    P, L, U = linalg.lu(arr, permute_l=False, overwrite_a=False, check_finite=False)
    Pinv = np.linalg.inv(P)
    return Pinv, L, U

def getRowsIndexedByThisGroup(arr, rho, accessGroup): #returns the rows of arr that are labeled in rho by players in accessGroup
    accessGroupIndices = [i for i in range(len(rho)) if rho[i] in accessGroup]
    arr_A = arr[accessGroupIndices]
    return arr_A

def getColumnsIndexedByThisGroup(arr, rho, accessGroup):
    accessGroupIndices = [i for i in range(len(rho)) if rho[i] in accessGroup]
    arr_A = arr[:, accessGroupIndices]
    return arr_A

def recombineShares(m, shares_a, l_a):
    shares_a_vector = np.zeros(m, dtype=float)
    l_a_vector = np.zeros(m, dtype=float)
    for share_a in shares_a:
        shares_a_vector[share_a[1]] = share_a[0]
    for l_i in l_a:
        l_a_vector[l_i[1]] = l_i[0]
    for i in range(m):
        if l_a_vector[i] != 0 and shares_a_vector[i] == 0:
            print ("Missing share at position ", str(i))
            return 0
    return np.matmul(shares_a_vector, l_a_vector)



#  M S P   R E L A T E D   F U N C T I O N S

#Proof of Concept implementation of the LCW algorithm.
#Input: The title of a 'nested threshold operator-based description string' in config.json
#Returns: An MSP tuple (MSP matrix and owner list, which maps each matrix row to a player)
def getMSP(confTitle):
    M = getVandermonde(1,1)
    L = parser.parseJsonAsString(confTitle)[0]
    nextInsertionIndex = 0
    while (nextInsertionIndex >= 0):
        nextInsertion = L.pop(nextInsertionIndex)
        nextInsertionThreshold = nextInsertion['select']
        nextInsertionMembers = nextInsertion['out-of']
        M2 = getVandermonde(nextInsertionThreshold, len(nextInsertionMembers))
        M = performMspInsertion(M, M2, nextInsertionIndex)
        for i in range(len(nextInsertionMembers)):
            L.insert(nextInsertionIndex + i, nextInsertionMembers[i])
        nextInsertionIndex = findFirstNestedThresholdDescription(L)
    return (M, L)

def getVandermonde(threshold, numberOfPoints):
    vander = np.vander(range(1, numberOfPoints+1), threshold, True)
    return vander

#insertion of matrix M2 (2D) in the row of matrix M1 (2D) specified by the index r, with r in [0, m1-1]
def performMspInsertion(M1, M2, r):
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

def findFirstNestedThresholdDescription(L):
    for i in range(len(L)):
        if type(L[i]) == dict:
            return i
    return -1

def createCoefficientVector(secret, coefficientsCount):
        return [secret] + [random.randrange(1,100) for i in range(coefficientsCount)]

def createShares(M, r):
        s = np.matmul(M,r)
        return s