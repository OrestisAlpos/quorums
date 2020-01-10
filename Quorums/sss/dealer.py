import sss.linearAlgebraUtil as lautil
import numpy as np

# M,rho describe the MSP, such as: M,rho = msputil.getMSP(accessStructureTitle)
# M: m x d, rho: m x 1 (0,1, ...,m-1)
def share(secret, M, rho):
        m,d = M.shape
        r = lautil.createCoefficientVector(secret, d - 1)
        s = lautil.createShares(M, r)
        for i in range(m):
                print('Player ' + str(rho[i]) + '  gets share:  ' + str(s[i]))
        shares = list(zip(s, range(m)))
        return shares # Each share is a tuple (si, i). That is to cover the case where one party gets multiple shares.

# M,rho describe the MSP, such as: M,rho = msputil.getMSP(accessStructureTitle)
# accesGroup is a list that describes the players that try to reconstruct the secret, such as: accessGroup = ['A', 'B', 'D', 'E']
def reconstruct(shares, M, rho, accessGroup):
        m,d = M.shape
        shares_a = [share for share in shares if rho[share[1]] in accessGroup]
        l_a = lautil.findRecombinationVector(M, rho, accessGroup)
        print('Reconstruction from the following group:')
        for (_,i) in shares_a:
                print('Player ' + str(rho[i]))
        if np.array_equal(l_a, np.array([])):
                print('IMPOSSIBLE')
                return 0
        for l_i in l_a:
                if l_i[0] == 0:
                        print('Share of party', str(rho[l_i[1]]), 'ignored.')
        secret = lautil.recombineShares(m, shares_a, l_a)
        if secret == 0:
                print('IMPOSSIBLE')
                return 0
        return secret

