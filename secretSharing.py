import util
import msputil
import linearAlgebraUtil
import random
import numpy as np

# M,L describe the MSP, such as: M, L = msputil.getMSP(accessStructureTitle)
def share(secret, M, L):
        # M dimensions: m x d
        assert(M.shape[0] == len(L))
        R = [secret] + [random.randrange(1,100) for i in range(M.shape[1] - 1)]
        # R is a vector d x 1
        shares = np.matmul(M,R)
        for i in range(len(shares)):
                print('Player ' + str(L[i]) + '  gets share:  ' + str(shares[i]))
        return shares

# M,L describe the MSP, such as: M, L = msputil.getMSP(accessStructureTitle)
# accesGroup is a list that describes the players that try to reconstruct the secret, such as: accessGroup = ['A', 'B', 'D', 'E']
def reconstruct(shares, M, L, accessGroup):
        accessGroupIndices = [i for i in range(len(L)) if L[i] in accessGroup]
        sa = shares[accessGroupIndices]
        la = linearAlgebraUtil.findRecombinationVector(M, L, accessGroup)
        print('Reconstruction from the following group:')
        for i in accessGroupIndices:
                print('Player ' + str(L[i]))
        if np.array_equal(la, np.array([])):
                print('IMPOSSIBLE')
                return 0
        for i in range(la.shape[0]):
                if la[i] == 0:
                        print('Player', str(L[accessGroupIndices[i]]), 'ignored.')
        secret = np.matmul(sa, la)
        return secret

