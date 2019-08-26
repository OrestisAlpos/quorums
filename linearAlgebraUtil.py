import numpy as np
from scipy import linalg
import sympy

# M,L describe the MSP, such as: M, L = msputil.getMSP(accessStructureTitle)
# accesGroup is a list that describes the players that try to reconstruct the secret, such as: accessGroup = ['A', 'B', 'D', 'E']
# returns l such us: x * Ma = e1, where e1 = (1,0,0,...)
def findRecombinationVector(M, L, accessGroup):
        accessGroupIndices = [i for i in range(len(L)) if L[i] in accessGroup]
        Ma = M[accessGroupIndices, :]
        e = np.array([1] + [0]*(Ma.shape[1]-1)).reshape((7,1))
        return solveLinearEquation(Ma.T, e) #TODO: Call getRecombinationVector() here

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

def getRowsIndexedByThisGroup(arr, L, accessGroup): #returns the rows of arr that are labeled in L by players in accessGroup
    accessGroupIndices = [i for i in range(len(L)) if L[i] in accessGroup]
    arr_A = arr[accessGroupIndices]
    return arr_A

def getColumnsIndexedByThisGroup(arr, L, accessGroup):
    accessGroupIndices = [i for i in range(len(L)) if L[i] in accessGroup]
    arr_A = arr[:, accessGroupIndices]
    return arr_A