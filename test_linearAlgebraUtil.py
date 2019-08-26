import numpy as np
import msputil
import linearAlgebraUtil

def test_PLU(confTitle):
    mspM, mspL = msputil.getMSP(confTitle)
    P, L, U = linearAlgebraUtil.getPLU(mspM.T) # P MT = L U
    return np.allclose(np.matmul(P, mspM.T) , np.matmul(L, U))

def test_PLU_onSubgroup(confTitle, accessGroup):
    mspM, mspL = msputil.getMSP(confTitle)
    P, L, U = linearAlgebraUtil.getPLU(mspM.T) # P MT = L U
    MTA = linearAlgebraUtil.getColumnsIndexedByThisGroup(mspM.T, mspL, accessGroup)
    UA = linearAlgebraUtil.getColumnsIndexedByThisGroup(U, mspL, accessGroup) # P MTA = L UA
    return np.allclose(np.matmul(P, MTA) , np.matmul(L, UA))

def runAll():
    return test_PLU('LcwExample') | test_PLU_onSubgroup('LcwExample', ['A', 'B', 'D', 'E'])