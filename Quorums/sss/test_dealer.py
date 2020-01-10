import sss.linearAlgebraUtil as lautil
import sss.dealer as dealer
import parser, parserutil
import checker
import numpy as np
import random

def runAll():
    # Parse the threshold description of the Example 5, Lcw paper to get the AccessStructure and corresponding MSP
    accessStructure = parser.parseJson('LcwExample')
    M, L = lautil.getMSP('LcwExample')
    # Define a secret and share it.
    secret = 42
    shares = dealer.share(secret, M, L)
    assert len(shares) == M.shape[0] == len(L)
    universe = parserutil.getUniverse(accessStructure)
    # Try all possible authorized sets and their complements (which should not allow reconstruction)
    allAuthorized = set(accessStructure)
    for authorizedSet in allAuthorized:
        accessGroup = list(authorizedSet)
        secret_recons = dealer.reconstruct(shares, M, L, accessGroup)
        print('Finished Reconstruction from AUTHORIZED: ', accessGroup, ' Result: ', secret_recons)
        assert(abs(secret_recons - secret) < 1e-10)
        adversaryGroup = universe.difference(accessGroup)
        secret_recons = dealer.reconstruct(shares, M, L, adversaryGroup)
        print('Finished  Reconstruction from NON AUTHORIZED: ', adversaryGroup, ' Result: ', secret_recons)
        assert(abs(secret_recons < 1e-10))
    # Try some random sets to see if they can reconstruct
    for _ in range(100):
        wannabe = random.sample(universe, 4)
        secret_recons = dealer.reconstruct(shares, M, L, wannabe)
        if frozenset(wannabe) in allAuthorized:
            print('Finished Reconstruction from RANDOM AUTHORIZED: ', wannabe, ' Result: ', secret_recons)
            assert(abs(secret_recons - secret) < 1e-10)
        else:
            print('Finished Reconstruction from RANDOM NON AUTHORIZED: ', wannabe, ' Result: ', secret_recons)
            assert(abs(secret_recons < 1e-10))
    # Try some random AUTHORIZED sets WITH REDUNDANT shares to see if they can reconstruct
    for authorizedSet in allAuthorized:
        redundant = random.sample(universe, 1)
        accessGroup = list(authorizedSet.union(set(redundant)))
        secret_recons = dealer.reconstruct(shares, M, L, accessGroup)
        print('Finished Reconstruction from REDUNDANT AUTHORIZED: ', accessGroup, ' + ', redundant, ' Result: ', secret_recons)
        assert(abs(secret_recons - secret) < 1e-10)
    return True